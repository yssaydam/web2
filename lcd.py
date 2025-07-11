from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont
import socket
import time
import subprocess
from datetime import datetime

def get_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127."):
            ip = subprocess.check_output("hostname -I", shell=True).decode().split()[0]
        return ip
    except:
        return "IP alınamadı"

def get_temp():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return output.replace("temp=", "").strip()
    except:
        return "Yok"

# Log bırak
with open("/home/yssaydam/Desktop/web2/lcd_debug.log", "a") as f:
    f.write("Kod başladı...\n")

try:
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)

    while True:
        with canvas(device) as draw:
            draw.text((0, 0), "Sezgin Kuyumculuk", font=font, fill=255)
            draw.text((0, 15), f"IP: {ip}", font=font, fill=255)
            draw.text((0, 30), f"Sıcaklık: {temp}°C", font=font, fill=255)
            draw.text((90, 50), now, font=font, fill=255)
        time.sleep(10)

except Exception as e:
    with open("/home/yssaydam/Desktop/web2/lcd_debug.log", "a") as f:
        f.write(f"{datetime.now()} - Hata: {str(e)}\n")
