import network
from machine import Pin
import ujson as json

led = machine.Pin('LED', machine.Pin.OUT)

def load_wifi_credentials():
    with open("wifi_credentials.json", "r") as file:
        data = json.load(file)
        return data["networks"]

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    available_networks = wlan.scan()

    wifi_networks = load_wifi_credentials()

    # Find the desired network in the scanned networks
    for network_info in available_networks:
        ssid = network_info[0].decode()
        for wifi_network in wifi_networks:
            if ssid == wifi_network["ssid"]:
                print("Connecting to", ssid)
                wlan.connect(ssid, wifi_network["password"])
                while not wlan.isconnected():
                    led.value(0)
                    pass
                print("Connected to", ssid)
                led.value(1)
                return

    print("Desired network not found")

connect_to_wifi()
