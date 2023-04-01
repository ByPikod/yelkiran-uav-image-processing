"""Bindings class"""
import socket
import threading
from time import sleep

try:
    from gpiozero import Servo, LED, Button
except ImportError:
    print("Currently not running on Raspberry PI.")


class Bindings:
    """
    This class contains the communication functions.
    By extending this class, we will be able to support both simulator and raspberry communication.
    """
    
    terminate = False

    def open_package_door(self):
        """Binding for activate servo motor and open the package door."""


class Server(Bindings):
    """
    Connects to the simulator via socket and sends the command to drop ball.
    """

    socket_client: socket.socket

    def __init__(self, host, port):

        try:
            self.socket_client = socket.socket()
            self.socket_client.connect((host, port))
            print("Successfully connected to the server!")
        except socket.error as msg:
            print(f"Failed to connect server: {msg}")
            exit(0)

    def open_package_door(self):
        self.socket_client.send(b'\x01')


class Raspberry(Bindings):
    """
    Raspberry pi connector.
    """

    def __init__(self):        
        self.servo = Servo(17)
        self.servo.max()
        self.led = LED(27)
        self.led.on()
        self.button = Button(2)
        print("Servo configured.")
    
    def open_package_door(self):
        print("Package door is opened!")
        self.servo.min()
        
        def blink():
            self.led.on()
            sleep(0.3)
            self.led.off()
            sleep(0.3)
            self.led.on()
            sleep(0.3)
            self.led.off()
            sleep(0.3)
            self.led.on()
            self.servo.max()
            
        t1 = threading.Thread(target=blink)
        t1.start()
        
