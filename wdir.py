wind_angles = [] # List to store wind direction in degrees every 5 seconds, cleared after every transmission

def voltage_divider(r1, r2, vin):
    vout = (vin * r2) / (r1 + r2)
    return round(vout, 1)

def populate_V2D():
    R1 = 10_000 # Static resistor value on board
    VIN = 3.3 # Input voltage can be 5.0 or 3.3
    resistances = [ # Resistor values inside wind vain
    33_000,
    6570,
    8200,
    891,
    1000,
    688,
    2200,
    1410,
    3900,
    3140,
    16_000,
    14_120,
    120_000,
    42_120,
    64_900,
    21_880]
    volts, degrees = {}, 0.0

    for r2 in resistances:
        voltage = voltage_divider(R1, r2, VIN)
        volts[voltage] = degrees
        degrees += 22.5 # Degrees between each resistor/reed switch in wind vane
    return volts

def wdir_average():
    global wind_angles
    import math
    sin_sum, cos_sum = 0.0, 0.0

    for angle in wind_angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)
    
    flen = float(len(wind_angles))
    s, c = sin_sum / flen, cos_sum / flen
    arc = math.degrees(math.atan(s / c))

    if s > 0 and c > 0:
        avg = arc
    elif c < 0:
        avg = arc + 180
    elif s < 0 and c > 0:
        avg = arc + 360
    wind_angles.clear() # Clear readings to average
    return 0.0 if avg == 360 else avg

def monitor_wdir():
    from gpiozero import MCP3008
    from time import sleep
    global wind_angles
    failed_count = 0
    adc, volts = MCP3008(), populate_V2D()

    while True:
        vane_voltage = round(adc.value * 3.3, 1)
        if vane_voltage in volts:
            wind_angles.append(volts[vane_voltage])
        else:
            failed_count += 1
            print(f"Unkown wind direction voltage: {vane_voltage}\n\tReading was not recorded\n\tTotal readings not recorded: {failed_count}")
        sleep(5)