import streamlit as st
import subprocess
import json
import requests
import os

st.set_page_config(page_title="Antigravity Cloud - Personal Cabinet", page_icon="🛸", layout="wide")

st.title("🛸 Antigravity Cloud")
st.subheader("Личный кабинет управления вашим ИИ-агентом")

# --- Side Bar ---
st.sidebar.header("🛡️ Статус Системы")

def get_status():
    try:
        result = subprocess.run(["openclaw", "status", "--json"], capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}

status_data = get_status()

if "error" not in status_data:
    gateway_status = status_data.get("gateway", {}).get("state", "Unknown")
    st.sidebar.success(f"Gateway: {gateway_status}")
    st.sidebar.info(f"Version: {status_data.get('update', {}).get('current', 'N/A')}")
else:
    st.sidebar.error("Gateway Offline")

# --- Main Dashboard ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧠 Активная Модель")
    # Здесь будем дергать активную сессию
    st.info("Текущая модель: Gemini 3 Flash")
    
    st.markdown("### ⚙️ Быстрая смена")
    if st.button("🚀 Переключить на Gemini 3 Flash"):
        subprocess.run(["openclaw", "config", "set", "agents.defaults.model", "google-antigravity/gemini-3-flash"])
        st.success("Настройки обновлены!")
        
    if st.button("🦙 Переключить на Llama 3.3"):
        subprocess.run(["openclaw", "config", "set", "agents.defaults.model", "groq/llama-3.3-70b-versatile"])
        st.success("Настройки обновлены!")

with col2:
    st.markdown("### 💰 Баланс OpenRouter")
    st.metric(label="Баланс", value="$10.45", delta="+$2.00")
    st.progress(70, text="Лимит токенов (окно 1M)")

st.divider()

st.markdown("### 📄 Логи сессии (Live)")
st.code("Watching for updates...", language="bash")

# --- Controls ---
st.divider()
if st.button("🔄 Перезагрузить Gateway (Self-Heal)"):
    with st.spinner("Перезагрузка..."):
        subprocess.run(["openclaw", "gateway", "restart"])
    st.success("Gateway перезапущен!")
