# This class is meant to control the PI M-235.5DD linear actuator

import serial
import time

STD_DELAY_MS = 5

class M235_5DD_Actuator:
    def __init__(self, port, baud_rate, timeout_ms=1000):
        self.serial = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout_ms/1000)

    def __del__(self):
        self.serial.close()

    ############################################################################
    ###################### INITIALIZATION FUNCTIONS ############################
    ############################################################################

    def close_serial(self):
        self.serial.close()

    def connect(self):
        address_device = bytes([1, 48, 13])
        self.serial.write(address_device)
        response = self.serial.readline().decode().strip()
        if response:
            print("Probe Motor Connected")
        else:
            print("Error writing connect command")

        time.sleep(STD_DELAY_MS / 1000)

    def on(self):
        command = b"MN\r"
        self.serial.write(command)
        print("Probe turns on")
        time.sleep(STD_DELAY_MS / 1000)

    def off(self):
        command = b"MF\r"
        self.serial.write(command)
        print("Probe turns off")
        time.sleep(STD_DELAY_MS / 1000)

    def reset(self):
        command = b"RT\r"
        self.serial.write(command)
        print("Probe reset")
        time.sleep(STD_DELAY_MS / 1000)

    ############################################################################
    ########################### SETTER FUNCTIONS ###############################
    ############################################################################

    def set_Pgain(self, gain):
        if gain < 0:
            print("Parameter out of range")
            return
        Pgain = str(gain)
        command = "DP" + Pgain + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set P gain command")
            return
        # print("P gain set to " + Pgain)
        time.sleep(STD_DELAY_MS / 1000)

    def set_Igain(self, gain):
        if gain < 0:
            print("Parameter out of range")
            return
        Igain = str(gain)
        command = "DI" + Igain + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set I gain command")
            return
        # print("I gain set to " + Igain)
        time.sleep(STD_DELAY_MS / 1000)

    def set_Dgain(self, gain):
        if gain < 0:
            print("Parameter out of range")
            return
        Dgain = str(gain)
        command = "DD" + Dgain + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set D gain command")
            return
        # print("D gain set to " + Dgain)
        time.sleep(STD_DELAY_MS / 1000)

    def set_integration_limit(self, limit):
        if limit < 0:
            print("Parameter out of range")
            return
        Ilimit = str(limit)
        command = "DL" + Ilimit + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set integration limit command")
            return
        # print("I limit set to " + Ilimit)
        time.sleep(STD_DELAY_MS / 1000)

    def set_home(self):
        print("Set home")
        command = "DH\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set home command")
            return
        # print("Current position set as Home")
        time.sleep(STD_DELAY_MS / 1000)

    def set_velocity(self, vel):
        if vel > 61440:
            vel = 61440
        if vel < 0:
            vel = 0
        velocity = str(vel)
        command = "SV" + velocity + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set velocity command")
            return
        # print("Velocity set to " + velocity)
        time.sleep(STD_DELAY_MS / 1000)

    def set_acceleration(self, acc):
        if acc > 2000000:
            acc = 2000000
        if acc < 200:
            acc = 200
        acceleration = str(acc)
        command = "SA" + acceleration + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in acceleration command")
            return
        # print("Acceleration set to " + acceleration)
        time.sleep(STD_DELAY_MS / 1000)

    def set_limit_switch(self, state):
        command = "LN\r" if state else "LF\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set limit switch command")
            return
        # print("Limit switch enabled= " + str(state))
        time.sleep(STD_DELAY_MS / 1000)

    def set_max_following_error(self, error):
        if error < 0:
            print("Parameter out of range")
            return
        err_str = str(error)
        command = "SM" + err_str + "\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing in set max following error command")
            return
        # print("Following error set to " + err_str)
        time.sleep(STD_DELAY_MS / 1000)

    ############################################################################
    ########################### GETTER FUNCTIONS ###############################
    ############################################################################
        
    def get_Pgain(self):
        command = "GP\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get P gain command")
            return -1

    def get_Igain(self):
        command = "GI\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get I gain command")
            return -1

    def get_Dgain(self):
        command = "GD\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get D gain command")
            return -1

    def get_integration_limit(self):
        command = "GL\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get integration limit command")
            return -1

    def get_current_error(self):
        command = "TE\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get current error command")
            return -1

    def get_current_pos(self):
        command = "TP\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get current pos command")
            return -1

    def get_current_pos_mm(self):
        pos = self.get_current_pos()
        return pos / 2048.0

    def get_current_vel(self, time_ms=1000):
        milliseconds = str(time_ms)
        command = "TV" + milliseconds + "\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get current vel command")
            return -1

    def get_programmed_vel(self):
        command = "TY\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get programmed vel command")
            return -1

    def get_programmed_acc(self):
        command = "TL\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get programmed acc command")
            return -1

    def get_following_error(self):
        command = "TL\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get following error command")
            return -1

    def get_target_pos(self):
        command = "TL\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get target pos command")
            return -1

    def get_dynamic_target(self):
        command = "TL\r"
        self.serial.write(command.encode())
        num_bytes = self.serial.readline().decode().strip()
        if num_bytes:
            return int(num_bytes[3:])
        else:
            print("Device not responding to get dynamic target command")
            return -1


    ############################################################################
    ########################### MOVEMENT FUNCTIONS ###############################
    ############################################################################



    def go_home(self):
        command = "GH\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing go home command")
            return
        time.sleep(0.1)
        dummy_error = self.wait_after_stop(50)
        time.sleep(0.1)

    def find_origin(self):
        command = "FE1\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing find origin command")
            return
        print("Finding zero...")
        accumulator = 0
        while accumulator < 5:
            speed = self.get_current_vel(500)
            if speed == 0:
                accumulator += 1
            time.sleep(0.05)
        print("Found origin")
        time.sleep(0.1)

    def custom_command(self, my_command):
        command = my_command + "\r"
        num_bytes = self.serial.write(command.encode())
        if num_bytes <= 0:
            print("Error writing custom command:", my_command)
            return

    def move_abs(self, target, blocking=True):
        pos_str = str(target)
        command = "MA" + pos_str + "\r"
        num_bytes = self.serial.write(command.encode())
        if num_bytes <= 0:
            print("Error writing move absolute command")
            return
        if blocking:
            time.sleep(0.1)
            dummy_error = self.wait_after_stop(10)
            time.sleep(0.1)

    def move_rel(self, delta, blocking=True):
        delta_str = str(delta)
        command = "MR" + delta_str + "\r"
        num_bytes = self.serial.write(command.encode())
        if num_bytes <= 0:
            print("Error writing move relative command")
            return
        if blocking:
            time.sleep(0.1)
            dummy_error = self.wait_after_stop(10)
            time.sleep(0.1)

    def wait_after_stop(self, time_ms):
        buff = ""
        milliseconds = str(time_ms)
        command = "WS" + milliseconds + ",TE\r"
        num_bytes = self.serial.write(command.encode())
        if num_bytes <= 0:
            print("Error writing wait after stop command")
            return -1
        num_bytes = self.serial.read_until(b'\r\n', 100)
        buff = num_bytes.decode('utf-8')
        buff = buff.strip()
        buff = buff[3:]
        if num_bytes:
            return int(buff)
        else:
            print("Device not responding to wait after stop command")
            return -1

    def hard_stop(self):
        command = "AB\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing hard stop command")
            return
        time.sleep(0.1)

    def soft_stop(self):
        command = "AB1\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing soft stop command")
            return
        time.sleep(0.1)

    def brakes_on(self):
        command = "BN\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing brakes ON command")
            return
        time.sleep(0.1)

    def brakes_off(self):
        command = "BF\r"
        res = self.serial.write(command.encode())
        if res <= 0:
            print("Error writing brakes OFF command")
            return
        time.sleep(0.1)

