import os
import streamlit as st
import base64
from openai import OpenAI

# 🌻 Estilo temático de girasol
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
p, label, .stTextInput, .stTextArea, .stExpander {
    color: #4a3000 !important;
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
</style>
""", unsafe_allow_html=True)

# 🌻 Configuración de la página
st.set_page_config(page_title="Análisis de Imagen 🌻", layout="centered", initial_sidebar_state="collapsed")

# 🌻 Título
st.title("🌻 Análisis de Imagen: 🤖🏞️")

# Clave API
ke = st.text_input('🔑 Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=api_key) if api_key else None

# Función para convertir la imagen
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Subida de imagen
uploaded_file = st.file_uploader("🌼 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("📸 Imagen subida", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Opción de pregunta adicional
show_details = st.toggle("💬 Preguntar algo específico sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area(
        "🌻 Añade contexto o tu pregunta aquí:",
        disabled=not show_details
    )

# Botón de análisis
analyze_button = st.button("🌻 Analiza la imagen", type="secondary")

# Lógica del análisis
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🌼 Analizando ... por favor espera 🌼"):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe lo que ves en la imagen en español."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional del usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages, max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"🚫 Ocurrió un error: {e}")
else:
    if not uploaded_file and analyze_button:
        st.warning("🌻 Por favor, sube una imagen antes de analizar.")
    if not api_key:
        st.warning("🔑 Ingresa tu API key para continuar.")
