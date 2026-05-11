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
        # 1. Kullanıcı mesajını hafızaya ekle
        self.memory.add("user", user_message)

        # ReAct döngüsü — en fazla 5 tur (sonsuz döngüye karşı koruma)
        for tur in range(5):
            # Her turda güncel mesaj listesini oluştur: [system prompt] + [konuşma geçmişi]
            messages = [
                {"role": "system", "content": get_system_prompt()}
            ] + self.memory.get_history()

            try:
                # Groq API çağrısı
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=GROQ_TOOLS,
                    tool_choice="auto",
                    max_tokens=2048
                )
            except Exception as e:
                # API veya bağlantı hatası durumunda çökmemek için hata dön
                return {
                    "success": False,
                    "error": f"Yapay zeka modeline bağlanırken hata oluştu: {str(e)}",
                    "project_name": "Hata"
                }

            mesaj = response.choices[0].message

            # DURUM A: Araç çağrısı yok → Model nihai yanıtı verdi
            if not mesaj.tool_calls:
                final_text = mesaj.content or ""
                # Nihai yanıtı hafızaya ekle
                self.memory.add("assistant", final_text)
                return {
                    "success": True,
                    "summary": final_text,
                    "markdown": final_text,
                    "project_name": self._proje_adini_cikar(user_message)
                }

            # DURUM B: Araç çağrısı var → Her aracı çalıştır
            # ÖNEMLİ: Önce asistanın "araç çağırma" niyetini hafızaya işle (API kuralıdır)
            self.memory.add(
                role="assistant",
                content=mesaj.content or "",
                tool_calls=mesaj.tool_calls
            )

            # Model birden fazla aracı aynı anda çağırmak isteyebilir
            for tool_call in mesaj.tool_calls:
                arac_adi = tool_call.function.name
                
                try:
                    # Argümanları JSON olarak çözümle
                    parametreler = json.loads(tool_call.function.arguments)
                except Exception:
                    # JSON formatı bozuksa boş parametre gönder
                    parametreler = {}

                print(f"  → [{tur+1}. Tur] Araç çalışıyor: {arac_adi} | Parametreler: {parametreler}")

                # Gerçek Python fonksiyonunu çalıştır (date_calc, task_break vb.)
                sonuc = run_tool(arac_adi, parametreler)

                # Aracın sonucunu hafızaya ekle (tool_call_id ile eşleştirerek)
                self.memory.add(
                    role="tool",
                    tool_call_id=tool_call.id,
                    content=json.dumps(sonuc, ensure_ascii=False)
                )
            
            # Burada döngü başa döner. Bir sonraki turda 'messages' listesi artık 
            # asistanın çağrısını ve araçların sonuçlarını da içerdiği için 
            # LLM bu verilere bakarak nihai planı oluşturur.

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