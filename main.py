
CONFIG_FILE = "config.json"
CONFIG = {}
import os, json
if CONFIG_FILE in os.listdir():
    with open(CONFIG_FILE, 'r') as f:
        CONFIG = json.load(f)

from umqtt.simple import MQTTClient
import machine, neopixel, ubinascii, micropython, utime

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

PIN = machine.Pin(CONFIG.get("pin"))
LEDS = CONFIG.get("leds")
SERVER = CONFIG.get("mqtt_server")
TOPIC = CONFIG.get("mqtt_topic")

pixels = neopixel.NeoPixel(PIN, LEDS)

def allblack():
    black = (0, 0, 0)
    for i in range(0, LEDS):
        pixels[i] = black
    pixels.write()

allblack()

STEPS = [ 
    [[[1], [0, 0, 0]]]
]
COUNT = 1
REPEAT = False
INDEX = 0
LAST_FRAME_TIME = utime.ticks_ms()
REPEAT_EVERY = 1000/4 # 3 fps

def dopattern():
    global INDEX
    global LAST_FRAME_TIME

    current = utime.ticks_ms()
    if utime.ticks_diff(current, LAST_FRAME_TIME) >= REPEAT_EVERY:
        if INDEX < COUNT:
            LAST_FRAME_TIME = current
            step = STEPS[INDEX]
            print(step)
            INDEX = INDEX + 1
            for leds, color in step:
                for led in leds:
                    pixels[led-1] = color
            pixels.write()

        elif REPEAT:
            INDEX = 0
            dopattern()
        else:
            allblack()

def sub_cb(topic, msg):
    print((topic, msg))
    try:
        global INDEX
        global STEPS
        global COUNT
        global REPEAT
        global REPEAT_EVERY

        new_pattern = json.loads(msg)
        steps = new_pattern.get("steps")
        repeat = new_pattern.get("repeat", False)
        fps = new_pattern.get("fps", 1)

        for i in range(0, len(steps)):
            step = steps[i]
            for leds, color in step:
                if len(leds) > 0:
                    if leds[0] == 0:
                        leds.clear()
                        leds.extend(range(0, LEDS))
                    elif leds[0] == -1:
                        mod = leds[1]
                        off = leds[2]
                        leds.clear()
                        leds.extend([x for x in range(0, LEDS) if (x-off) % mod == 0])

        INDEX = 0
        STEPS = steps
        COUNT = len(STEPS)
        REPEAT = repeat
        REPEAT_EVERY = 1000/fps

        allblack()

    except:
        print("error")

def init():
    black = (0, 0, 0)
    white = (10, 10, 10)
    for i in range(0, LEDS):
        pixels[i] = white
        pixels[i-1] = black
        pixels.write()
    allblack()

def main(server):
    init()
    c = MQTTClient(CLIENT_ID, server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    while True:
        c.check_msg()
        dopattern()
    c.disconnect()

machine.freq(160000000)
main(SERVER)
