from gpiozero import Button

DEFAULT_RAIN_SENSOR = Button(5)
#BUCKET_SIZE = 0.2794 # mm
BUCKET_SIZE = 0.011 # inches

class RainMonitor:
    def __init__(self, BUCKET=BUCKET_SIZE, button=DEFAULT_RAIN_SENSOR):
        self.tips = 0
        self.button = button
        self.bucket_size = BUCKET_SIZE

    def bucket_tipped(self):
        self.tips += 1
        #print(f"Bucket tipped! Total rainfall calculated is {self.tips * self.bucket_size}")

    def reset_rainfall(self):
        self.tips = 0

    def monitor_rainfall(self):
        self.button.when_pressed = self.bucket_tipped