# slave_sensor2.py
import network
import socket
import time
import dht
from machine import Pin
import gc

gc.collect()

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.1)
wlan.active(True)
wlan.connect("carvajal1", "12345678")

print("Conectando como sensor2...")
while not wlan.isconnected():
    time.sleep(0.5)
print("sensor2 conectado. IP:", wlan.ifconfig()[0])

# Puedes usar otro pin si quieres, ej. GPIO4
d = dht.DHT11(Pin(14))  # o Pin(4)

while True:
    try:
        d.measure()
        temp = d.temperature()
        hum = d.humidity()
        payload = f"sensor2:{temp},{hum}"

        s = socket.socket()
        s.connect(("192.168.4.1", 8888))
        s.send(payload.encode())
        s.close()
        print(f" sensor2 enviado: {temp}°C, {hum}%")
    except Exception as e:
        print(" sensor2 error:", e)
    time.sleep(5)
