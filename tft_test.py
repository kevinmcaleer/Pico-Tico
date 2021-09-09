from machine import SPI, Pin
from tft_st7735 import TFT
from sysfont import sysfont

# SPI.init(baudrate=1000000, *, 
# polarity=0, 
# phase=0, 
# bits=8, 
# firstbit=SPI.MSB, 
# sck=None, 
# mosi=None, 
# miso=None, 
# pins=SCK, MOSI, MISO)


spi = SPI(1, sck=Pin(10), mosi=Pin(12), miso=Pin(13))
tft = TFT(spi, aDC=8, aReset=9, aCS=13)

tft.reset()
# tft.on()
tft.rect(aStart=[1,1], aSize=[10,10], aColor=tft.RED)
# tft.text(aPos=[1,1],aString="HELLO", aFont=sysfont, aColor=tft.WHITE)