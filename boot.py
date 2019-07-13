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

def boot():
    config_file = "config.json"
    if config_file in os.listdir('.') :
        try:
            config = {}
            with open(config_file, 'r') as f:
                config = json.load(f)

            frequency = config.get("frequency", None)
            if frequency:
                import machine
                machine.freq(frequency)

            do_connect(config.get("ssid"), config.get("password"))
        except:
            pass

boot()