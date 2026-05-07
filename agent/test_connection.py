import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Bağlantı test ediliyor...")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Merhaba! Kısaca kendini tanıt."}]
)

print("[BAŞARILI]")
print(response.choices[0].message.content)