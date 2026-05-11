import streamlit as st
import sys
import os

# ui klasöründen bir üst dizine çıkıp tools klasörünü bulabilmesi için path ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.agent import PlanningAgent
from tools.demo_scenarios import get_demo_scenarios

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI Görev Planlayıcı", page_icon="🎯", layout="wide")

# --- HAFIZA (SESSION STATE) YÖNETİMİ ---
if "agent" not in st.session_state:
    st.session_state.agent = PlanningAgent()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben proje planlama asistanınızım. Bana projenizden bahsedin."}]
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "project_name" not in st.session_state:
    st.session_state.project_name = "Plan"

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.header("🎯 AI Görev Planlayıcı")
    st.write("Projelerinizi yapay zeka ile saniyeler içinde planlayın.")
    st.divider()
    
    # Sohbeti ve planı sıfırlayan buton
    if st.button("🗑️ Yeni Plan / Sohbeti Temizle", type="primary", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Ben proje planlama asistanınızım. Bana projenizden bahsedin."}]
        st.session_state.current_plan = None
        st.session_state.project_name = "Plan"
        st.session_state.agent.reset()
        st.rerun() # Sayfayı anında yeniler

    st.subheader("💡 Demo Senaryoları")
    st.write("Hızlı test için bir senaryo seçebilirsiniz:")
    
    # demo_scenarios.py'den verileri çekiyoruz
    scenarios = get_demo_scenarios()
    for sc in scenarios:
        if st.button(sc["title"], use_container_width=True):
            # Butona basıldığında sanki kullanıcı yazmış gibi chat inputuna göndermek için state'e ekliyoruz
            st.session_state.demo_input = sc["project_name"]

    st.divider()
    st.info("Sistem Durumu: Çevrimiçi\n\nKullanılan Model: Llama-3.3-70b (Groq)")

# --- ANA EKRAN (İKİ SÜTUNLU YAPI) ---
# Sol taraf chat (oran 1), sağ taraf plan tablosu (oran 1.5)
col_chat, col_plan = st.columns([1, 1.5])

with col_chat:
    st.subheader("💬 Asistan ile Konuş")
    
    # 1. Sabit yükseklikte, kaydırılabilir bir sohbet kutusu oluşturuyoruz (Örn: 500px)
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        # Geçmiş mesajları bu sabit kutunun içine basıyoruz
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
            
    # 2. Input kutusu sütunun en altında sabit bekler
    user_input = st.chat_input("Projenizi buraya yazın (Örn: E-ticaret sitesi yapacağım)")
    
    # Demo butonu tıklandıysa inputu tetikle
    if "demo_input" in st.session_state:
        user_input = st.session_state.demo_input
        del st.session_state["demo_input"]

    if user_input and user_input.strip():
        # Kullanıcı mesajını anında hafızaya ekle
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Kullanıcı mesajını anında o kutunun içinde göster
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Proje analiz ediliyor ve görevler planlanıyor..."):
                    result = st.session_state.agent.run(user_input)
                    
                    if result.get("success"):
                        st.session_state.current_plan = result["markdown"]
                        st.session_state.project_name = result["project_name"]
                        
                        # Tabloyu sağa atıp, sola sadece kısa bilgi veriyoruz
                        chat_mesaji = "🎯 Planınız isteğinize göre güncellendi! Detayları sağ taraftaki panodan inceleyebilirsiniz."
                        st.markdown(chat_mesaji)
                        st.session_state.messages.append({"role": "assistant", "content": chat_mesaji})
                    else:
                        error_msg = f"❌ Bir hata oluştu: {result.get('error', 'Bilinmeyen hata')}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()

with col_plan:
    st.subheader("📋 Güncel Proje Planı")
    
    if st.session_state.current_plan:
        # Planı şık bir kart içinde göster
        with st.container(border=True):
            st.markdown(st.session_state.current_plan)
            
        st.divider()
        # İndirme butonu
        file_name = f"{st.session_state.project_name.replace(' ', '_')}_plan.md"
        st.download_button(
            label="⬇️ Planı Markdown Olarak İndir",
            data=st.session_state.current_plan,
            file_name=file_name,
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("👈 Sol taraftan projenizi anlatarak bir plan oluşturabilirsiniz.")