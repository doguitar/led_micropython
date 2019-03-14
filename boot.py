import esp
esp.osdebug(None)

import json, os

def do_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

    network.WLAN(network.AP_IF).active(False)

CONFIG = "config.json"
if os.path.exists(CONFIG) and os.path.isfile(CONFIG):
    try:
        config = {}
        with open(CONFIG, 'r') as f:
            config = json.load(f)
        do_connect(config.get("ssid"), config.get("password"))
    except:
        pass
