from gpiozero import Button
from math import pi
from time import sleep
from threading import Lock

DEFAULT_WIND_SENSOR = Button(6) # Button(6)

class WindMonitor:
    wind_count = 0
    wind_list = []
    wind_count_lock, wind_list_lock = Lock(), Lock()

    def __init__(self, button=DEFAULT_WIND_SENSOR):
        self.wind_count = 0
        self.wind_list = []
        self.button = button
        self.wind_count_lock = Lock()
        self.wind_list_lock = Lock()
        self.ADJUSTMENT = 1.18 # compensate for anemometer factor

    def calculate_speed(self, stop_event):
        delay = 5 # 5 seconds
        while not stop_event.is_set():
            with self.wind_count_lock.acquire and self.wind_list_lock:
                if self.wind_count > 0:
                    radius_cm = 9.0
                    cm_in_mile = 160934.4
                    circumference_cm = (2 * pi) * radius_cm
                    rotations = self.wind_count / 2.0
                    dist_miles = (circumference_cm * rotations) / cm_in_mile
                    miles_per_sec = dist_miles / delay # Divide distance by time
                    miles_per_hour = (miles_per_sec * 3600) * self.ADJUSTMENT # miles per second times seconds in an hour
                    self.wind_list.append(miles_per_hour)
                    self.wind_count = 0 # Reset wind count
                sleep(delay)

    def spin(self):
        with self.wind_count_lock:
            self.wind_count += 1

    def monitor_wind(self):
        self.button.wind_sensor.when_pressed = self.spin