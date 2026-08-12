import urequests, network
import time
from machine import Pin

led = Pin(22, Pin.OUT)       # LED di GPIO 23
buzzer = Pin(23, Pin.OUT)   # Buzzer di GPIO 23

#Konfigurasi Wifi
SSID = "iot"
PASSWORD = "Iot@12345678"

# --------  Menghubungkan Ke Wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Menghubungkan Wi-Fi...")
    time.sleep(1)

print("Wi-Fi Terhubung:", wlan.ifconfig())

# --- Konfigurasi ---
SERVER_URL = "http://192.168.110.90:5000/status"  # ganti IP server Flask

while True:
    try:
        res = urequests.get(SERVER_URL)
        state = res.json()
        res.close()

        # kontrol lampu
        if state["lampu"] == "on":
            led.value(1)
        else:
            led.value(0)

        # kontrol buzzer
        if state["buzzer"] == "on":
            buzzer.value(1)
        else:
            buzzer.value(0)

        print("Status:", state)
    except Exception as e:
        print("Error:", e)

    time.sleep(0.2)  # cek status setiap 3 detik
