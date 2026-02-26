import streamlit as st
import os
import time
import glob
import os
from gtts import gTTS
from PIL import Image
import base64

def sidebar_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

sidebar_bg("gato2}.jpg")
st.title("Conversión de Texto a Audio")
image = Image.open('gato1.jpg')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Esrcibe, pega o selecciona texto de esta página para ser escuchado.")


try:
    os.mkdir("temp")
except:
    pass

st.subheader("Fragmento de El Gato Bajo la Lluvia de Ernest Hemingway")
st.write('Sólo dos americanos había en aquel hotel. No conocían a ninguna de las personas que subían y bajaban por las escaleras hacia y desde sus habitaciones. La suya estaba en el segundo piso, frente al mar y al monumento de la guerra, en el jardín público de grandes palmeras y verdes bancos. Cuando hacía buen tiempo, no faltaba algún pintor con su caballete. A los artistas les gustaban aquellos árboles y los brillantes colores de los hoteles situados frente al mar.

Los italianos venían de lejos para contemplar el monumento a la guerra, hecho de bronce que resplandecía bajo la lluvia. El agua se deslizaba por las palmeras y formaba charcos en los senderos de piedra. Las olas se rompían en una larga línea y el mar se retiraba de la playa, para regresar y volver a romperse bajo la lluvia. Los automóviles se alejaron de la plaza donde estaba el monumento. Del otro lado, a la entrada de un café, un mozo estaba contemplando el lugar ahora solitario....')
           
st.markdown(f"¿Quieres escucharlo?")
text = st.text_area("Copia el texto que quieras escuchar en el cuadro abajo")

tld='com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang=="Español" :
    lg='es'
if option_lang=="English" :
    lg='en'

def text_to_speech(text, tld,lg):
    
    tts = gTTS(text,lang=lg) # tts = gTTS(text,'en', tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("Convertir a audio"):
     result, output_text = text_to_speech(text, 'com',lg)#'tld
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"## Tú audio:")
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     #if display_output_text:
     
     #st.write(f" {output_text}")
    
#if st.button("ElevenLAabs",key=2):
#     from elevenlabs import play
#     from elevenlabs.client import ElevenLabs
#     client = ElevenLabs(api_key="a71bb432d643bbf80986c0cf0970d91a", # Defaults to ELEVEN_API_KEY)
#     audio = client.generate(text=f" {output_text}",voice="Rachel",model="eleven_multilingual_v1")
#     audio_file = open(f"temp/{audio}.mp3", "rb")

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
     st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
