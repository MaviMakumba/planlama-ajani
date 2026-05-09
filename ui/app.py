import streamlit as st
import sys
import os

# ui klasöründen bir üst dizine çıkıp tools klasörünü bulabilmesi için path ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.planning_pipeline import generate_project_plan
from tools.demo_scenarios import get_demo_scenarios

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI Görev Planlayıcı", page_icon="🎯", layout="wide")

# --- HAFIZA (SESSION STATE) YÖNETİMİ ---
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
    
    # Geçmiş mesajları ekrana bas
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Kullanıcıdan yeni girdi al (Demo butonundan gelen bir değer varsa onu kullan)
    user_input = st.chat_input("Projenizi buraya yazın (Örn: E-ticaret sitesi yapacağım)")
    
    # Demo butonu tıklandıysa inputu tetikle
    if "demo_input" in st.session_state:
        user_input = st.session_state.demo_input
        del st.session_state["demo_input"]

    if user_input and user_input.strip():
        # Kullanıcı mesajını ekle ve göster
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Asistanın yanıtını işle
        with st.chat_message("assistant"):
            with st.spinner("Proje analiz ediliyor ve görevler planlanıyor..."):
                # Şimdilik planning_pipeline üzerinden çalıştırıyoruz.
                # Kişi 1 asıl agent.py'yi bitirdiğinde buradaki fonksiyonu değiştireceğiz.
                result = generate_project_plan(user_input)
                
                if result.get("success"):
                    response_text = result["summary"]
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Sağ tarafta göstermek için planı hafızaya al
                    st.session_state.current_plan = result["markdown"]
                    st.session_state.project_name = result["project_name"]
                else:
                    error_msg = f"❌ Bir hata oluştu: {result.get('error', 'Bilinmeyen hata')}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

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