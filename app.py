import os
import uuid
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Text Response Generator", layout="centered")

with st.sidebar:
    st.header("API Keys")
    st.caption("Keys entered here override environment variables. They are not stored.")

    openrouter_key = st.text_input("OpenRouter API Key", type="password", value="")
    anthropic_key = st.text_input("Anthropic API Key", type="password", value="")

    st.divider()
    st.header("Supabase")
    supabase_url = st.text_input("Supabase URL", value="")
    supabase_key = st.text_input("Supabase Key", type="password", value="")

if openrouter_key:
    os.environ["OPENROUTER_API_KEY"] = openrouter_key
if anthropic_key:
    os.environ["ANTHROPIC_API_KEY"] = anthropic_key
if supabase_url:
    os.environ["SUPABASE_URL"] = supabase_url
if supabase_key:
    os.environ["SUPABASE_KEY"] = supabase_key

from llm import get_client, MODEL_OPTIONS
from storage.supabase import save_response

st.title("Text Response Generator")

model_name = st.selectbox("Model", MODEL_OPTIONS)
prompt = st.text_area("Prompt", placeholder="Type your prompt here...", height=150)

if st.button("Generate", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        uid = str(uuid.uuid4())

        with st.spinner("Generating response..."):
            try:
                client = get_client(model_name)
                response = client.generate(prompt)
            except Exception as e:
                st.error(f"LLM error: {e}")
                st.stop()

        st.subheader("Response")
        st.markdown(response)

        try:
            save_response(uid, prompt, response, model_name)
            st.success(f"Saved to Supabase  |  id: {uid}")
        except Exception as e:
            st.warning(f"Response generated but failed to save: {e}")
