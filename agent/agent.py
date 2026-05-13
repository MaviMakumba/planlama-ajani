import os
import json
from dotenv import load_dotenv
from groq import Groq

from agent.prompts import get_system_prompt
from agent.memory import Memory
from tools.tool_definitions import TOOL_DEFINITIONS
from tools.tool_dispatcher import run_tool

load_dotenv()

GROQ_TOOLS = [{"type": "function", "function": tool} for tool in TOOL_DEFINITIONS]


class PlanningAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.memory = Memory()
        self.model = "llama-3.3-70b-versatile"

    def run(self, user_message: str) -> dict:
        # Kullanıcı mesajını hafızaya ekle
        self.memory.add("user", user_message)

        # messages listesi döngü başında bir kez oluşturulur ve
        # araç sonuçları her turda bu listeye EKLENİR — sıfırlanmaz.
        # Böylece önceki tur araç sonuçları kaybolmaz.
        messages = [
            {"role": "system", "content": get_system_prompt()}
        ] + self.memory.get_history()

        for tur in range(5):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,  # type: ignore
                    tools=GROQ_TOOLS,   # type: ignore
                    tool_choice="auto",
                    parallel_tool_calls=False,
                    max_tokens=2048
                )
            except Exception as e:
                if "tool_use_failed" in str(e) and tur < 4:
                    print(f"  → Bozuk araç formatı, yeniden deneniyor (tur {tur+1})...")
                    continue  # hata döndürme, döngüyü başa al
                return {
                    "success": False,
                    "error": f"Yapay zeka modeline bağlanırken hata oluştu: {str(e)}",
                    "project_name": "Hata"
                }

            mesaj = response.choices[0].message

            # Groq bazen araç çağrısını yanlış formatlarsa atla ve tekrar dene
            if mesaj.content and "tool_use_failed" in mesaj.content:
                print(f"  → Araç çağrısı başarısız (tur {tur+1}), yeniden deneniyor...")
                continue

            # DURUM A: Araç çağrısı yok → nihai yanıt geldi
            if not mesaj.tool_calls:
                final_text = mesaj.content or ""
                self.memory.add("assistant", final_text)
                return {
                    "success": True,
                    "summary": final_text,
                    "markdown": final_text,
                    "project_name": self._proje_adini_cikar(user_message)
                }

            # DURUM B: Araç çağrısı var → çalıştır, sonucu messages'a ekle
            # Asistanın "araç çağırıyorum" mesajını listeye ekle
            messages.append({
                "role": "assistant",
                "content": mesaj.content or "",
                "tool_calls": mesaj.tool_calls
            })

            # Her aracı çalıştır ve sonucunu listeye ekle
            for tool_call in mesaj.tool_calls:
                arac_adi = tool_call.function.name
                try:
                    parametreler = json.loads(tool_call.function.arguments)
                except Exception:
                    parametreler = {}

                print(f"  → [{tur+1}. Tur] Araç: {arac_adi} | Parametreler: {parametreler}")

                sonuc = run_tool(arac_adi, parametreler)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(sonuc, ensure_ascii=False)
                })
            # Döngü başa döner. Bir sonraki turda messages hem araç çağrısını
            # hem sonuçlarını içerdiği için LLM artık planı oluşturabilir.

        return {
            "success": False,
            "summary": "Plan oluşturulamadı, lütfen tekrar deneyin.",
            "markdown": "",
            "project_name": "Plan"
        }

    def reset(self):
        self.memory.reset()

    def _proje_adini_cikar(self, metin: str) -> str:
        kelimeler = metin.strip().split()
        return " ".join(kelimeler[:5]) if kelimeler else "Proje"