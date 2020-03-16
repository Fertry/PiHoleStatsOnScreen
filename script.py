# https://github.com/Fertry

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import datetime
import time
import requests
import json

''' Se puede reducir el tiempo de actualización pero algunas pantallas 
pueden dar problemas de actualización de la imagen! '''
DELAY_TIME = 15

RST = None
display = Adafruit_SSD1306.SSD1306_128_64(rst=RST) # 128_64 indica la resolución
display.begin()
display.clear()
display.display()

width = display.width
height = display.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline = 0, fill = 0)

# Podemos cargar otras fuentes desde internet
# La fuente elegida debe estar presente en el mismo directorio que el script
fontTime = ImageFont.truetype("Arial.ttf", 16)
fontText = ImageFont.truetype("Arial.ttf", 12)

# Constantes para dibujar en pantalla
padding = -2
top = padding
bottom = height - padding
x = 0

# Función principal
def main():
	
    data = requests.get("http://IP_DE_LA_RASPBERRY_PI/admin/api.php?summary")
    hora = datetime.datetime.now().hour
    minuto = datetime.datetime.now().minute

    draw.rectangle((0,0,width,height), outline = 0, fill = 0)
    draw.text((32,top), str(hora) + ":" + str(minuto), font = fontTime, fill = 255)
    draw.text((x,top + 19), "%s%%" % data.json()["ads_percentage_today"], font = fontText, fill = 255)
    draw.text((x,top + 38), "Anuncios bloqueados: ", font = fontText, fill = 255)
    draw.text((x,top + 54), "%s" % data.json()["ads_blocked_today"], font = fontText, fill = 255)

    display.image(image)
    display.display()
    	
if __name__ == "__main__":
	
	while True:
		
		# Apagamos la pantalla durante la noche para evitar "burn-in"
		if (datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 6):
			
			draw.rectangle((0,0,width,height), outline = 0, fill = 0)
			display.image(image)
			display.display()
			
		else:
			
			try:
				
				main()
				
			except:
				
				print("Error encontrado")
				
		time.sleep(DELAY_TIME)
