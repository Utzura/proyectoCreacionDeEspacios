import streamlit as st
import paho.mqtt.client as mqtt
import time
import base64

BROKER = "test.mosquitto.org"
TOPIC = "esp32/status"

# Estado persistente
if "esp32_connected" not in st.session_state:
    st.session_state.esp32_connected = False

if "mqtt_client" not in st.session_state:
    st.session_state.mqtt_client = None

if "audio_played" not in st.session_state:
    st.session_state.audio_played = False


def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print("Mensaje recibido:", mensaje)

    if mensaje == "connected":
        st.session_state.esp32_connected = True
        st.session_state.audio_played = False  # permitir reproducir


def init_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(TOPIC)
    client.loop_start()  # 🔥 escucha en segundo plano
    return client


# Inicializar MQTT una sola vez
if st.session_state.mqtt_client is None:
    st.session_state.mqtt_client = init_mqtt()


# UI
st.title("Monitor ESP32 🚀")

if st.session_state.esp32_connected:
    st.success("ESP32 conectado 🎉")

    # 🔥 AUTOPLAY FORZADO (solo una vez)
    if not st.session_state.audio_played:
        st.session_state.audio_played = True

        audio_file = open("sonido.mp3", "rb")
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

        st.markdown(
            f"""
            <audio id="player" autoplay>
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>

            <script>
                var audio = document.getElementById("player");
                if (audio) {{
                    audio.play().catch(e => console.log("Autoplay bloqueado:", e));
                }}
            </script>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning("Esperando conexión del ESP32...")

time.sleep(1)
st.rerun()
