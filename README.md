# Pico-Tico
Kevin McAleer, September 2021, based on Arduino code by Alex Flom

## Thingiverse STLs:
<https://www.thingiverse.com/thing:4946788>

## Alex Flom's Documentation
Alex provides detailed instructions and information to build your own Tico Robot here:
<https://playrobotics.com/blog/tico-tic-tac-toe-arduino-robot-documentation/>

# Tico Arduino code:
This is the Original Arduino version of the code
<https://github.com/PlayRoboticsGit/tico>

# Pico-Tico MicroPython code fo the Raspberry Pi Pico
<https://github.com/kevinmcaleer/Pico-Tico>

See the accompanying video:
![https://youtu.be/U741QL8LzZM](https://www.youtube.com/embed/U741QL8LzZM)

---

# Files
- [`configure.py`](configure.py) - this file helps you set the servos to the correct position before attaching the servo horns
- [`sysfont.py`](sysfont.py) - you need this file to enable the tft_st7735 library to draw text
- [`tft_st7735.py`](tft_st7735.py) - this is the ST7735 SPI driver library for the Tico-Pico screen
- [`ticopico.py`](ticopico.py) - this is the main program for playing tic-tac-toe. Rename this to main.py and upload the Pico if you want this to always start
- [`README.md`](README.md) - this is this file you are reading now
- [`.gitignore`](.gitignore) - this file contains lists of files to exclude from the source code control software, GIT

---