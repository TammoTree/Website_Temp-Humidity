# Complete project details at https://RandomNerdTutorials.com

from HTU2X import HTU21D
import time
from machine import Pin, SoftSPI, SoftI2C
import gc


led_rot = Pin(15, Pin.OUT)
led_gruen = Pin(17, Pin.OUT)

htu = HTU21D(22, 21)
gc.collect()

def web_page():
    if led_rot.value() == 1:
        gpio_state1="Werte sind nicht im Normbereichs"
    else:
        gpio_state1="Werte sind innerhalb des Normbereichs"


    
    html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="5"; URL="192.168">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <u><h1>Wetterstation</h1></u> 
    <p>Durschnittstemperatur: <strong>""" + str(messwerte_Durchschnitt_Temp) + """</strong>&deg;Celsius</p>
    <p>Durchschnittsluftfeuchte: <strong>""" + str(messwerte_Durschnitt_Luft) + """</strong>% </p>
    <p><strong>""" + gpio_state1 + """</strong> </p>"""
    
    

    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


messwerte_htu =[]
messwerte_htu_luft =[]

for i in range(0,5):
    messwerte_temp_htu = round(htu.temperature, 2)
    messwerte_htu.append(messwerte_temp_htu)
    messwerte_luft_htu =round(htu.humidity, 2)
    messwerte_htu_luft.append(messwerte_luft_htu)
    time.sleep(1)
print("Temp_htu:", messwerte_htu)
print("Luftfeuchte:", messwerte_htu_luft)

    

messwerte_Temp = messwerte_htu
messwerte_Temp.sort()
del messwerte_Temp[0]
messwerte_Temp.pop()
print("Werte Temp sortiert:", messwerte_Temp)

messwerte_Luft =messwerte_htu_luft
messwerte_Luft.sort()
del messwerte_Luft[0]
messwerte_Luft.pop()
print("Werte Luft sortiert:", messwerte_Luft)


messwerte_Durchschnitt_Temp = round((sum(messwerte_Temp) / len(messwerte_Temp)), 1)
print("Durschnitsswert:", messwerte_Durchschnitt_Temp)

messwerte_Durschnitt_Luft = round((sum(messwerte_Luft) / len(messwerte_Luft)),1)
print("Durschnitts_luft:", messwerte_Durschnitt_Luft)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()


    messwerte_htu =[]
    messwerte_htu_luft =[]

    for i in range(0,5):
      messwerte_temp_htu = round(htu.temperature, 2)
      messwerte_htu.append(messwerte_temp_htu)
      messwerte_luft_htu =round(htu.humidity, 2)
      messwerte_htu_luft.append(messwerte_luft_htu)
      time.sleep(1)
    print("Temp_htu:", messwerte_htu)
    print("Luftfeuchte:", messwerte_htu_luft)

    

    messwerte_Temp = messwerte_htu
    messwerte_Temp.sort()
    del messwerte_Temp[0]
    messwerte_Temp.pop()
    print("Werte Temp sortiert:", messwerte_Temp)

    messwerte_Luft =messwerte_htu_luft
    messwerte_Luft.sort()
    del messwerte_Luft[0]
    messwerte_Luft.pop()
    print("Werte Luft sortiert:", messwerte_Luft)


    messwerte_Durchschnitt_Temp = round((sum(messwerte_Temp) / len(messwerte_Temp)), 1)
    print("Durschnitsswert:", messwerte_Durchschnitt_Temp)

    messwerte_Durschnitt_Luft = round((sum(messwerte_Luft) / len(messwerte_Luft)),1)
    print("Durschnitts_luft:", messwerte_Durschnitt_Luft)
    time.sleep(5)

    if (messwerte_Durchschnitt_Temp <= 23) or (messwerte_Durschnitt_Luft <=50):
        led_gruen.value(1)
        led_rot.value(0)
    else:
        led_gruen.value(0)

    if (messwerte_Durchschnitt_Temp >= 25) or (messwerte_Durschnitt_Luft > 50):
        led_rot.value(1)
        led_gruen.value(0)
    else:
        led_rot.value(0)


