# main_ap.py - ESP32 Principal (Access Point + Servidor TCP)
import network
import socket
import time

# Configuración del AP
SSID = "carvajal1"
PASSWORD = "12345678"

ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
ap.active(True)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

print("📶 AP activo")
print("SSID:", SSID)
print("IP del AP:", ap.ifconfig()[0])
print("Esperando datos de sensores...\n")

def start_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8888))
    s.listen(2)
    print("📡 Servidor TCP listo en puerto 8888\n")

    while True:
        try:
            client, addr = s.accept()
            print(f"Conexión desde: {addr[0]}")
            
            data = client.recv(64)
            if data:  # ← ¡ESTA LÍNEA ES CLAVE! No puede estar vacía
                msg = data.decode().strip()
                if ":" in msg:
                    sensor_id, values = msg.split(":", 1)
                    if sensor_id in ["sensor1", "sensor2"]:
                        temp, hum = values.split(",", 1)
                        print(f" {sensor_id} → Temp: {temp}°C | Hum: {hum}%\n")
                    else:
                        print(f"  Sensor desconocido: {sensor_id}\n")
                else:
                    print(f" Formato inválido: {msg}\n")
            client.close()
        except Exception as e:
            print("❌ Error:", e)
            time.sleep(1)

# Ejecutar servidor
start_server()
