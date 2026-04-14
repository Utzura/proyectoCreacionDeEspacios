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


def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print("Mensaje recibido:", mensaje)

    if mensaje == "connected":
        st.session_state.esp32_connected = True


def init_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(TOPIC)
    return client


# Inicializar MQTT una sola vez
if st.session_state.mqtt_client is None:
    st.session_state.mqtt_client = init_mqtt()

# Procesar mensajes (NO bloqueante)
st.session_state.mqtt_client.loop(timeout=1.0)

# UI
st.title("Monitor ESP32 🚀")

if st.session_state.esp32_connected:
    st.success("ESP32 conectado 🎉")

    audio_file = open("sonido.mp3", "rb")
    audio_bytes = audio_file.read()
    b64 = base64.b64encode(audio_bytes).decode()

    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Esperando conexión del ESP32...")

# refresco automático
time.sleep(1)
st.rerun()
