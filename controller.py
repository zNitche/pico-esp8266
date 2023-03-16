import machine
from config import Config
from esp8266 import ESP8266


class Controller:
    def __init__(self):
        self.uart = machine.UART(Config.UART_ID, Config.UART_BAUDRATE)
        self.esp = ESP8266(self.uart)

        self.wifi_ssid = ""
        self.wifi_password = ""

        self.hotspot_ssid = "test_hotspot"
        self.hotspot_password = "hotspot1234"

    def esp_as_client(self):
        print(f"Connecting to network: {self.wifi_ssid}")
        self.esp.connect_to_network(self.wifi_ssid, self.wifi_password)

        address_data = self.esp.get_address_as_client()

        if len(address_data) > 0:
            print(f"Address data: {address_data}")

    def esp_as_host(self):
        print(f"Creating network: {self.hotspot_ssid}")
        self.esp.init_hotspot(self.hotspot_ssid, self.hotspot_password)

        address_data = self.esp.get_address_as_host()

        if len(address_data) > 0:
            print(f"Address data: {address_data}")

    def start_server(self):
        print("Starting server at port 8080")

        if self.esp.start_server(8080):
            print("Server running...")

            self.esp.server_mainloop()

    def mainloop(self):
        print("Starting ESP8266...")
        self.esp.startup()

        if self.esp.check_module():
            print("ESP8266 running...")

            self.esp_as_client()
            # self.esp_as_host()

            self.start_server()

