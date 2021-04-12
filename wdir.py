#from gpiozero import MCP3008

#adc = MCP3008(channel=0)
#count = 0
values = []
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
    21_880
]

def voltage_divider(r1, r2, vin):
    vout = (vin * r2) / (r1 + r2)
    return round(vout, 3)

def populate_V2D():
    volts = {}
    degrees = 0.0
    for r2 in resistances:
        voltage = voltage_divider(R1, r2, VIN)
        volts[voltage] = degrees
        degrees += 22.5
    return volts