"""Prisma: um material, vários formatos acessíveis (protótipo de hackathon)."""
import base64
import html
import json
import os
import re
import time

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env (chave e modelo)

# Aceita vários modelos separados por vírgula: se um estiver ocupado, tenta o próximo.
MODELS = [m.strip() for m in os.getenv("GEMINI_MODEL", "gemini-3.8-flash").split(",") if m.strip()]

from prompts import SYSTEM
from theme import FONTS, THEMES, build_css


@st.cache_resource
def get_client():
    return genai.Client()  # lê GEMINI_API_KEY do ambiente


def build_content(uploaded, pasted):
    parts = []
    if uploaded is not None:
        mime = "application/pdf" if uploaded.type == "application/pdf" else uploaded.type
        parts.append(types.Part.from_bytes(data=uploaded.getvalue(), mime_type=mime))
    if pasted.strip():
        parts.append("Texto do material:\n" + pasted.strip())
    parts.append("Adapte este material seguindo as instruções.")
    return parts


def adapt(uploaded, pasted):
    """Tenta de novo (até 5 vezes) quando o Google está sobrecarregado (503) ou no limite (429)."""
    resp = None
    for attempt in range(5):
        try:
            resp = get_client().models.generate_content(
                model=MODELS[attempt % len(MODELS)],
                contents=build_content(uploaded, pasted),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM,
                    response_mime_type="application/json",
                ),
            )
            break
        except Exception as e:  # noqa: BLE001
            if getattr(e, "code", None) in (429, 503) and attempt < 4:
                time.sleep(3 * (attempt + 1))  # espera 3s, 6s, 9s, 12s
                continue
            raise
    raw = (resp.text or "").strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.M).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return json.loads(raw[raw.index("{"): raw.rindex("}") + 1])


def speak_button(text, key):
    """Leitura em voz alta pelo próprio navegador (Web Speech API)."""
    components.html(
        f"""
        <div style="font-family:sans-serif">
          <button id="p" style="padding:10px 16px;font-size:16px">▶ Ouvir</button>
          <button id="s" style="padding:10px 16px;font-size:16px">■ Parar</button>
          <label style="margin-left:12px">Velocidade
            <select id="r" style="font-size:16px"><option value="0.8">Lenta</option>
            <option value="1" selected>Normal</option><option value="1.3">Rápida</option></select></label>
        </div>
        <script>
          const t = {json.dumps(text)};
          document.getElementById('p').onclick = () => {{
            speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'pt-BR'; u.rate = parseFloat(document.getElementById('r').value);
            speechSynthesis.speak(u);
          }};
          document.getElementById('s').onclick = () => speechSynthesis.cancel();
        </script>""",
        height=60,
    )


def render_block(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    st.markdown("".join(f"<p>{html.escape(p)}</p>" for p in paras), unsafe_allow_html=True)


# ---------------------------------------------------------------- UI
st.set_page_config(page_title="Prisma", page_icon="🔷", layout="wide")
st.title("🔷 Prisma")
st.caption("Um material, vários formatos acessíveis. Gerado por IA: revise antes de usar em sala.")

with st.sidebar:
    st.header("Preferências de leitura")
    font = st.selectbox("Fonte", FONTS)
    size = st.slider("Tamanho do texto (px)", 16, 32, 20)
    lh = st.slider("Espaço entre linhas", 1.4, 2.4, 1.8, 0.1)
    ls = st.slider("Espaço entre letras (em)", 0.0, 0.2, 0.05, 0.01)
    contrast = st.selectbox("Contraste", list(THEMES))
    teacher = st.toggle("Modo professor (editar antes de liberar)")

st.markdown(build_css(font, size, lh, ls, contrast), unsafe_allow_html=True)

col_in, col_out = st.columns([1, 2], gap="large")

with col_in:
    st.subheader("1. Envie o material")
    mode = st.radio("Origem", ["Arquivo", "Câmera (lousa)", "Colar texto"], horizontal=True)
    uploaded, pasted = None, ""
    if mode == "Arquivo":
        uploaded = st.file_uploader("PDF ou imagem", type=["pdf", "png", "jpg", "jpeg", "webp"])
    elif mode == "Câmera (lousa)":
        uploaded = st.camera_input("Fotografe a lousa")
    else:
        pasted = st.text_area("Cole o texto", height=200)
    if uploaded is not None and uploaded.type != "application/pdf":
        st.image(uploaded, caption="Material enviado", use_container_width=True)

    if st.button("✨ Adaptar", type="primary", disabled=(uploaded is None and not pasted.strip())):
        with st.spinner("Adaptando o material..."):
            try:
                st.session_state["result"] = adapt(uploaded, pasted)
                st.session_state.pop("done", None)
            except Exception as e:  # noqa: BLE001
                st.error(f"Não consegui adaptar o material: {e}")

with col_out:
    r = st.session_state.get("result")
    if not r:
        st.info("Envie um material e clique em **Adaptar**.")
    else:
        st.subheader(r.get("titulo", "Material adaptado"))
        for w in r.get("warnings", []):
            st.warning(f"Revise: {w}")
        t_audio, t_dys, t_adhd, t_gloss = st.tabs(
            ["🔊 Áudio-descrição", "📖 Dislexia", "✅ TDAH: micro-tarefas", "📚 Glossário"])

        with t_audio:
            text = r.get("audio_description", "")
            if teacher:
                text = st.text_area("Editar", text, height=250, key="ed_audio")
            speak_button(text, "audio")
            render_block(text)

        with t_dys:
            text = r.get("dyslexia_text", "")
            if teacher:
                text = st.text_area("Editar", text, height=250, key="ed_dys")
            speak_button(text, "dys")
            render_block(text)

        with t_adhd:
            tasks = r.get("adhd_tasks", [])
            total = max(len(tasks), 1)
            done = sum(1 for i in range(len(tasks)) if st.session_state.get(f"task_{i}"))
            st.progress(done / total, text=f"{done} de {len(tasks)} etapas concluídas")
            for i, t in enumerate(tasks):
                with st.expander(f"Etapa {i + 1}: {t['title']} (~{t.get('minutes', 3)} min)", expanded=(i == done)):
                    for step in t.get("steps", []):
                        st.markdown(f"- {step}")
                    st.checkbox("Concluí esta etapa", key=f"task_{i}")
            if tasks and done == len(tasks):
                st.success("Missão cumprida! 🎉 Você terminou todas as etapas.")
                st.balloons()

        with t_gloss:
            for g in r.get("glossary", []):
                st.markdown(f"**{g['term']}**: {g['simple']}")
                if g.get("example"):
                    st.caption(f"Exemplo: {g['example']}")
