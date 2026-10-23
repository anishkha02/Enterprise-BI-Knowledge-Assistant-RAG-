import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="BI Knowledge Assistant", page_icon="📊")
st.title("📊 Enterprise BI Knowledge Assistant")
st.caption("Ask about KPIs, data dictionary tables, SSRS reports and Power BI dashboards.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("e.g. How is customer churn rate calculated?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching documentation..."):
            try:
                r = requests.post(f"{API_URL}/ask", json={"question": prompt}, timeout=60)
                r.raise_for_status()
                data = r.json()
                text = (data["answer"]
                        + "\n\n**Sources:** " + ", ".join(data["sources"])
                        + f"\n\n*Response time: {data['latency_s']}s*")
            except Exception as e:
                text = f"Error contacting the API: {e}"
        st.markdown(text)
    st.session_state.messages.append({"role": "assistant", "content": text})