import os
import streamlit as st
import base64
from openai import OpenAI

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
st.set_page_config(
    page_title="🌻 Análisis de Imagen - Tema Girasol",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================
# ESTILO TEMA GIRASOL
# ==============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff8dc 0%, #fff6bf 50%, #fff3b0 100%);
    color: #4a3000;
    font-family: 'Trebuchet MS', sans-serif;
}
h1, h2, h3 {
    color: #5a3e00 !important;
    text-align: center;
    font-weight: bold;
}
p, label {
    color: #5e4200 !important;
}
.stButton button {
    background-color: #f6c700 !important;
    color: #4a3000 !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}
.stButton button:hover {
    background-color: #ffd93b !important;
    transform: scale(1.05);
}
.stTextInput input, .stTextArea textarea {
    border-radius: 10px;
    border: 2px solid #f6c700;
    background-color: #fff9e6;
}
.uploadedFile {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# ENCABEZADO
# ==============================
st.markdown("""
<div style="text-align:center; background-color:#fffbea; border-radius:15px; border:3px solid #f6c700; padding:20px;">
    <h1>🌻 Análisis de Imagen con Inteligencia Artificial 🌻</h1>
    <p>Sube una imagen y deja que la IA te cuente su historia entre pétalos de girasol 🌼</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ==============================
# FUNCIÓN PARA ENCODEAR IMAGEN
# ==============================
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ==============================
# CLAVE Y CONFIGURACIÓN DEL CLIENTE
# ==============================
ke = st.text_input("🔑 Ingresa tu Clave API de OpenAI", type="password")
os.environ["OPENAI_API_KEY"] = ke

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.warning("⚠️ Por favor, ingresa tu API key para continuar.")

# ==============================
# SUBIR IMAGEN
# ==============================
uploaded_file = st.file_uploader("🌼 Sube una imagen para analizar", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("📸 Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# ==============================
# PREGUNTA OPCIONAL
# ==============================
show_details = st.toggle("💬 ¿Deseas preguntar algo específico sobre la imagen?", value=False)

if show_details:
    additional_details = st.text_area(
        "🌻 Agrega tu pregunta o contexto adicional:",
        placeholder="Ejemplo: ¿Qué emoción transmite esta imagen?",
        disabled=not show_details
    )

# ==============================
# BOTÓN DE ANÁLISIS
# ==============================
analyze_button = st.button("🌻 Analizar imagen")

# ==============================
# LÓGICA DE ANÁLISIS
# ==============================
if uploaded_file is not None and api_key and analyze_button:
    client = OpenAI(api_key=api_key)

    with st.spinner("🌼 Analizando la imagen, por favor espera..."):
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe lo que ves en esta imagen en español, usando un tono natural y descriptivo."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional del usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"🚫 Ocurrió un error durante el análisis: {e}")

elif analyze_button:
    if not uploaded_file:
        st.warning("🌻 Por favor, sube una imagen antes de analizar.")
    if not api_key:
        st.warning("🔑 Necesitas ingresar tu API key para continuar.")
