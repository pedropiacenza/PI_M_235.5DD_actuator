from linear_actuator import M235_5DD_Actuator
import time

if __name__ == '__main__': 
    my_probe = M235_5DD_Actuator("/dev/ttyUSB0", 19200)
    my_probe.connect()
    my_probe.on()
    my_probe.set_Pgain(160)
    my_probe.set_Igain(10)
    my_probe.set_Dgain(5)
    my_probe.set_integration_limit(1400)
    my_probe.set_velocity(20*2048)
    my_probe.set_acceleration(2000000)
    my_probe.go_home()
    print(f"Current position [mm] is: {my_probe.get_current_pos_mm()}")
    print(f"P gain is {my_probe.get_Pgain()}")
    print(f"I gain is {my_probe.get_Igain()}")
    print(f"D gain is {my_probe.get_Dgain()}")
    
    my_probe.move_rel(5*2048)
    time.sleep(2)
    my_probe.go_home()
    my_probe.off()
    my_probe.close_serial()
    
    
    