import streamlit as st
import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
TOPIC = "esp32/status"

# Estado persistente
if "esp32_connected" not in st.session_state:
    st.session_state.esp32_connected = False

if "mqtt_client" not in st.session_state:
    st.session_state.mqtt_client = None

if "audio_played" not in st.session_state:
    st.session_state.audio_played = False

if "update" not in st.session_state:
    st.session_state.update = False


# 📡 Callback MQTT
def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    print("Mensaje recibido:", mensaje)

    if mensaje == "connected":
        st.session_state.esp32_connected = True
        st.session_state.audio_played = False
        st.session_state.update = True  # 🔥 trigger UI


# 🔌 Inicializar MQTT
def init_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.subscribe(TOPIC)
    client.loop_start()  # 🔥 escucha en segundo plano
    return client


# Inicializar una sola vez
if st.session_state.mqtt_client is None:
    st.session_state.mqtt_client = init_mqtt()


# 🔥 Forzar actualización si llega mensaje
if st.session_state.update:
    st.session_state.update = False
    st.rerun()


# UI
st.title("Monitor ESP32 🚀")

if st.session_state.esp32_connected:
    st.success("ESP32 conectado 🎉")

    # 🔊 Reproducir audio solo una vez
    if not st.session_state.audio_played:
        st.session_state.audio_played = True

        st.markdown(
            """
            <audio autoplay>
                <source src="sonido.mp3" type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning("Esperando conexión del ESP32...")

# pequeño delay para no saturar
time.sleep(0.2)
