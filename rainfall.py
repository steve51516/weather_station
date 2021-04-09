from gpiozero import Button

bucket = Button(5)
#BUCKET_SIZE = 0.2794 # mm
BUCKET_SIZE = 0.011 # inches
tips = 0

def bucket_tipped():
    global tips
    tips += 1
    #print(f"Bucket tipped! Total rainfall calculated is {tips * BUCKET_SIZE}")

def reset_rainfall():
    global tips
    tips = 0

def monitor_rainfall():
    bucket.when_pressed = bucket_tipped