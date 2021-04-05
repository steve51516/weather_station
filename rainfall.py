from gpiozero import Button

bucket = Button(5)
BUCKET_SIZE = 0.2794
tips = 0

def bucket_tipped():
    global tips
    tips += 1
    print(f"Bucket tipped! Total rainfall calculated is {tips * BUCKET_SIZE}")

def reset_rainfall():
    global tips
    tips = 0