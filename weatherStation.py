# -*- coding: utf-8 -*-

from Tkinter import *
import Tkinter as tk
import Adafruit_DHT as dht
import threading
import tkFont
import ImageTk
import RPi.GPIO as GPIO

from weather import Weather, Unit

weather = Weather(unit=Unit.CELSIUS)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

root = tk.Tk()

image = PhotoImage(file="background.gif")

background = Label(root, image=image)
background.place(x=0, y=0, relwidth=1, relheight=1)

temperature = StringVar()
temperature.set("----"+" °C")

humidity = StringVar()
humidity.set("----"+" %")

yahooTemp = StringVar()
yahooTemp.set("----"+ " °C")

yahooCondition = StringVar()
yahooCondition.set("Condition: ----")

temperatureLabel = Label(root, fg="white", background="#00dbde", textvariable=temperature, font=("Helvetica", 20, "bold"))
temperatureLabel.place(x=300, y=100)

humidityLabel = Label(root, fg="white", background="#00dbde", textvariable=humidity, font=("Helvetica", 20, "bold"))
humidityLabel.place(x=300, y=150)

yahooTempLabel = Label(root, fg="white", background="#00dbde", textvariable=yahooTemp, font=("Helvetica", 25, "bold"))
yahooTempLabel.place(x=0, y=100)

yahooConditionLabel = Label(root, fg="white", background="#00dbde", textvariable=yahooCondition, font=("Helvetica", 25, "bold"))

yahooConditionLabel.place(x=0, y=150)

root.attributes("-fullscreen", True)

root.bind("<1>", exit)


def exit():
    root.quit()


def readSensor():
    root.after(2000, readSensor)
    h, t = dht.read_retry(dht.DHT22, 20)
    temp = "%.1f" % t
    temperature.set(temp+" °C")
    hum = "%.1f" % h
    humidity.set(hum+"  %")
    print('Room => temp: {} humidity: {}').format(temp, humidity.get())

def getWeatherFromYahoo():
    root.after(900000, getWeatherFromYahoo)
    location = weather.lookup_by_location('montreal') 
    condition = location.condition
    yahooTemp.set(condition.temp.encode('ascii', 'ignore')+" °C")
    yahooCondition.set(condition.text.encode('ascii', 'ignore'))
    print("Yahoo => temp: {} condition: {}").format(condition.temp, condition.text)

root.after(2000, readSensor)
root.after(2000, getWeatherFromYahoo)
root.mainloop()
