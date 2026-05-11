import streamlit as st
import sys
import os
import time

# ui klasöründen bir üst dizine çıkıp tools klasörünü bulabilmesi için path ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.agent import PlanningAgent
from tools.demo_scenarios import get_demo_scenarios

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI Görev Planlayıcı", page_icon="🎯", layout="wide")

# --- 1. ÇOKLU SOHBET (MULTI-CHAT) HAFIZA YÖNETİMİ ---
if "agent" not in st.session_state:
    st.session_state.agent = PlanningAgent()

if "chats" not in st.session_state:
    # Sistemi ilk açtığında varsayılan bir sohbet odası oluştur
    default_id = str(int(time.time()))
    st.session_state.chats = {
        default_id: {
            "title": "Yeni Proje",
            "messages": [{"role": "assistant", "content": "Merhaba! Ben proje planlama asistanınızım. Bana projenizden bahsedin."}],
            "current_plan": None,
            "project_name": "Plan",
            "agent_memory": [] # Yapay zekanın bu projeye özel hafıza yedeği
        }
    }
    st.session_state.current_chat_id = default_id

# Sohbeti bir değişkene at
active_chat = st.session_state.chats[st.session_state.current_chat_id]

# --- 2. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.header("🎯 AI Görev Planlayıcı")
    
    # YENİ PROJE BUTONU
    if st.button("➕ Yeni Proje Başlat", type="primary", use_container_width=True):
        new_id = str(int(time.time()))
        st.session_state.chats[new_id] = {
            "title": f"Proje {len(st.session_state.chats) + 1}",
            "messages": [{"role": "assistant", "content": "Merhaba! Yeni bir proje için hazırım. Ne planlıyoruz?"}],
            "current_plan": None,
            "project_name": "Plan",
            "agent_memory": []
        }
        st.session_state.current_chat_id = new_id
        st.session_state.agent.reset() # Ajanın anlık hafızasını sıfırla ki eski proje buraya karışmasın
        st.rerun()

    st.divider()
    st.subheader("📂 Geçmiş Projeler")
    
    # GEÇMİŞ SOHBETLERİ LİSTELE VE BUTON YAP
    for chat_id, chat_data in st.session_state.chats.items():
        # Aktif olanı yeşil nokta ile, diğerlerini klasör ikonu ile göster
        btn_label = f"🟢 {chat_data['title']}" if chat_id == st.session_state.current_chat_id else f"📁 {chat_data['title']}"
        
        if st.button(btn_label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            # Ajanın hafızasını bu seçilen sohbete göre geri yükle
            st.session_state.agent.memory.history = st.session_state.chats[chat_id]["agent_memory"].copy()
            st.rerun()

    st.divider()
    st.subheader("💡 Demo Senaryoları")
    scenarios = get_demo_scenarios()
    for sc in scenarios:
        # Key parametresini ekledik ki butonlar çakışmasın
        if st.button(sc["title"], key="demo_" + sc["title"], use_container_width=True):
            st.session_state.demo_input = sc["project_name"]

    st.divider()
    st.info("Sistem Durumu: Çevrimiçi\n\nKullanılan Model: Llama-3.3-70b")

# --- 3. ANA EKRAN (İKİ SÜTUNLU YAPI) ---
col_chat, col_plan = st.columns([1, 1.5])

with col_chat:
    st.subheader("💬 Asistan ile Konuş")
    
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        # Aktif sohbetin mesajlarını bas
        for msg in active_chat["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
            
    user_input = st.chat_input("Projenizi buraya yazın (Örn: E-ticaret sitesi yapacağım)")
    
    if "demo_input" in st.session_state:
        user_input = st.session_state.demo_input
        del st.session_state["demo_input"]

    if user_input and user_input.strip():
        # Eğer bu projeye yazılan ilk mesajsa, soldaki "Yeni Proje" ismini kullanıcının ilk 3 kelimesiyle değiştir
        if len(active_chat["messages"]) == 1:
            active_chat["title"] = " ".join(user_input.split()[:3]) + "..."

        active_chat["messages"].append({"role": "user", "content": user_input})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.chat_message("assistant"):
                with st.spinner("Proje analiz ediliyor ve görevler planlanıyor..."):
                    result = st.session_state.agent.run(user_input)
                    
                    if result.get("success"):
                        active_chat["current_plan"] = result["markdown"]
                        active_chat["project_name"] = result["project_name"]
                        
                        chat_mesaji = "🎯 Planınız isteğinize göre güncellendi! Detayları sağ taraftaki panodan inceleyebilirsiniz."
                        st.markdown(chat_mesaji)
                        active_chat["messages"].append({"role": "assistant", "content": chat_mesaji})
                        
                        # HER BAŞARILI İŞLEMDEN SONRA, AJANIN GÜNCEL HAFIZASINI BU SOHBETİN YEDEĞİNE KAYDET
                        active_chat["agent_memory"] = st.session_state.agent.memory.history.copy()
                    else:
                        error_msg = f"❌ Bir hata oluştu: {result.get('error', 'Bilinmeyen hata')}"
                        st.error(error_msg)
                        active_chat["messages"].append({"role": "assistant", "content": error_msg})
        
        st.rerun()

with col_plan:
    st.subheader("📋 Güncel Proje Planı")
    
    if active_chat["current_plan"]:
        with st.container(border=True):
            st.markdown(active_chat["current_plan"])
            
        st.divider()
        file_name = f"{active_chat['project_name'].replace(' ', '_')}_plan.md"
        st.download_button(
            label="⬇️ Planı Markdown Olarak İndir",
            data=active_chat["current_plan"],
            file_name=file_name,
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("👈 Sol taraftan projenizi anlatarak bir plan oluşturabilirsiniz.")