# slave_sensor1.py
import network
import socket
import time
import dht
from machine import Pin
import gc

gc.collect()

# Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.1)
wlan.active(True)
wlan.connect("carvajal1", "12345678")

print("Conectando como sensor1...")
while not wlan.isconnected():
    time.sleep(0.5)
print("✅ sensor1 conectado. IP:", wlan.ifconfig()[0])

# Sensor DHT11 en GPIO15
d = dht.DHT11(Pin(12))

while True:
    try:
        d.measure()
        temp = d.temperature()
        hum = d.humidity()
        payload = f"sensor1:{temp},{hum}"

        # Enviar
        s = socket.socket()
        s.connect(("192.168.4.1", 8888))
        s.send(payload.encode())
        s.close()
        print(f"📤 jimmy1 enviado: {temp}°C, {hum}%")
    except Exception as e:
        print("❌ sensor1 error:", e)
    time.sleep(5)
