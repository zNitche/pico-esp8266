import machine
from config import Config
import time
import utime


class ESP8266:
    def __init__(self, uart):
        self.uart = uart

        self.state_pin = machine.Pin(Config.STATE_PIN_ID, machine.Pin.OUT)
        self.reset_pin = machine.Pin(Config.RESET_PIN_ID, machine.Pin.OUT)

    def startup(self):
        self.state_pin.on()

        self.reset_pin.off()

        time.sleep(2)
        self.reset_pin.on()

    def check_module(self):
        status, data = self.cmd("AT", "ready")

        return status

    def disconnect_from_network(self):
        self.cmd("AT+CWQAP")

    def connect_to_network(self, ssid, password):
        self.disconnect_from_network()

        self.cmd(f'AT+CWJAP="{ssid}","{password}"')
        self.cmd("AT+CWMODE=1")
        self.cmd("AT+CIPMODE=0")

    def init_hotspot(self, ssid, password):
        self.disconnect_from_network()

        self.cmd(f'AT+CWSAP="{ssid}","{password}",1,4')

        self.cmd("AT+CWMODE=2")
        self.cmd("AT+CIPMODE=0")

    def get_connected_devices(self):
        self.cmd("AT+CWLIF")

    def get_address_as_client(self):
        status, data = self.cmd("AT+CIFSR")

        return self.parse_cmd_data(data)

    def get_address_as_host(self):
        status, data = self.cmd("AT+CIPAP?")

        return self.parse_cmd_data(data)

    def check_connection_with_target(self, target_ip):
        return self.cmd(f'AT+PING="{target_ip}"')

    def parse_cmd_data(self, cmd_data):
        cmd_data = cmd_data.replace("\r", "").replace("\"", "").split("\n")
        cleared_cmd_data = [row for row in cmd_data if row != ""]

        return cleared_cmd_data

    def cmd(self, cmd, ack="OK", timeout=5000):
        status = False
        output_data = ""

        current_time = utime.ticks_ms()

        self.uart.write(f"{cmd}\r\n")

        while (utime.ticks_ms() - current_time) < timeout:
            uart_row = self.uart.read()

            if uart_row is not None:
                try:
                    row_data = uart_row.decode()
                    print(row_data)

                    output_data += row_data

                    if ack in row_data:
                        status = True
                        break
                except:
                    pass

        return status, output_data
