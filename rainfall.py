from gpiozero import Button
from threading import Lock
from time import sleep

DEFAULT_RAIN_SENSOR = Button(5)
#BUCKET_SIZE = 0.2794 # mm
BUCKET_SIZE = 0.011 # inches

class RainMonitor:
    def __init__(self, BUCKET=BUCKET_SIZE, button=DEFAULT_RAIN_SENSOR):
        self.tips = 0
        self.button = button
        self.bucket_size = BUCKET_SIZE
        self.tips_lock = Lock()

    def bucket_tipped(self):
        with self.tips_lock:
            self.tips += 1
            #print(f"Bucket tipped! Total rainfall calculated is {self.tips * self.bucket_size}")

    def total_rain(self): # Convert tips to rain in hundreths of an inch and reset tips counter
        while True:
            if not self.tips_lock.locked():
                t_rain = self.tips * self.bucket_size
                self.tips = 0
                return t_rain
            else:
                sleep(2)

    def monitor(self):
        self.button.when_pressed = self.bucket_tipped