import os
import json
from dotenv import load_dotenv
from groq import Groq

from agent.prompts import get_system_prompt
from agent.memory import Memory
from tools.tool_definitions import TOOL_DEFINITIONS
from tools.tool_dispatcher import run_tool

load_dotenv()

# Groq tool calling için definitions'ı doğru formata çevir
GROQ_TOOLS = [{"type": "function", "function": tool} for tool in TOOL_DEFINITIONS]


class PlanningAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.memory = Memory()
        self.model = "llama-3.3-70b-versatile"

    def run(self, user_message: str) -> dict:
        """
        Kullanıcı mesajını işle ve plan döndür.
        Dönen dict: {success, summary, markdown, project_name}
        """
        # Kullanıcı mesajını geçmişe ekle
        self.memory.add("user", user_message)

        # Her turda güncel mesaj listesini oluştur
        # [system prompt] + [konuşma geçmişi]
        messages = [
            {"role": "system", "content": get_system_prompt()}
        ] + self.memory.get_history()

        # ReAct döngüsü — en fazla 5 tur (sonsuz döngüye karşı koruma)
        for tur in range(5):

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=GROQ_TOOLS,
                tool_choice="auto",
                max_tokens=2048
            )

            mesaj = response.choices[0].message

            # Araç çağrısı yok → model nihai yanıtı verdi
            if not mesaj.tool_calls:
                final_text = mesaj.content or ""
                self.memory.add("assistant", final_text)
                return {
                    "success": True,
                    "summary": final_text,
                    "markdown": final_text,
                    "project_name": self._proje_adini_cikar(user_message)
                }

            # Araç çağrısı var → her aracı çalıştır, sonucu messages'a ekle
            messages.append({
                "role": "assistant",
                "content": mesaj.content or "",
                "tool_calls": mesaj.tool_calls
            })

            for tool_call in mesaj.tool_calls:
                arac_adi = tool_call.function.name
                parametreler = json.loads(tool_call.function.arguments)

                print(f"  → Araç çalışıyor: {arac_adi} | Parametreler: {parametreler}")

                sonuc = run_tool(arac_adi, parametreler)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(sonuc, ensure_ascii=False)
                })

        # 5 tur doldu, yanıt gelmedi
        return {
            "success": False,
            "summary": "Plan oluşturulamadı, lütfen tekrar deneyin.",
            "markdown": "",
            "project_name": "Plan"
        }

    def reset(self):
        """Konuşmayı sıfırla."""
        self.memory.reset()

    def _proje_adini_cikar(self, metin: str) -> str:
        """Kullanıcı mesajından kısa proje adı üret."""
        kelimeler = metin.strip().split()
        return " ".join(kelimeler[:5]) if kelimeler else "Proje"