import serial
import time
import math
from datetime import datetime

from datab import Data


def main(starting_angle=35):
    with serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=2) as ser:
        time.sleep(0.1)
        if ser.isOpen():
            print(f"{ser.port} connected")
            data = Data()
            max_power = data.max_power()
            print(max_power)
            start_pos = True
            movement_dir = {
                "M": 0,
                "R": starting_angle,
                "L": starting_angle*2
            }
            last_one = 0
            current_power = max_power
            try:
                # main loop
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time)
                while True:
                    while start_pos:
                        right_left = False
                        for key, value in movement_dir.items():
                            
                            if key != "M" and (not math.isclose(current_power,last_one,rel_tol=0.12)):
                                time.sleep(2)
                                cmd = f"{key}{value}"
                                ser.write(cmd.encode())
                                right_left = True

                            time.sleep(2)
                            cmd = "M"
                            d = data.req(char="M", number=0)
                            ser.write(cmd.encode())

                            if ser.inWaiting() >= 0:
                                answer = str(ser.readlines())
                                data.resp(d, answer)

                        max_val, direction = data.last_three()
                        current_power = max_val
                        
                        print(f"max_val = {max_val}, direction = {direction}")

                        # best position in starting point (reverse list)
                        if right_left:
                            if direction == 2:
                                cmd = f"R{starting_angle}"
                                ser.write(cmd.encode())
                                time.sleep(2)
                            elif direction == 1:
                                cmd = f"R{starting_angle * 2}"
                                ser.write(cmd.encode())
                                start_pos, not_best_find = False, True
                            elif direction == 0:
                                start_pos, not_best_find = False, True
                    while not_best_find:
                        current_power = max_val
                        i = 0
                        step_angle = 20
                        max_iter = (90 - starting_angle) // step_angle * 2
                        
                        while i <= max_iter and (not math.isclose(max_power, current_power, rel_tol=0.02)):
                            current_power = data.last_one()
                            print(f"current power = {current_power}")
                            if direction == 1:
                                time.sleep(2)
                                cmd = f"R{step_angle}"
                                ser.write(cmd.encode())
                                i += 1
                            else:
                                time.sleep(2)
                                cmd = f"L{step_angle}"
                                ser.write(cmd.encode())
                                i += 1

                            time.sleep(2)
                            cmd = "M"
                            d = data.req(char="M", number=0)
                            ser.write(cmd.encode())

                            if ser.inWaiting() >= 0:
                                answer = str(ser.readlines())
                                data.resp(d, answer)
                            time.sleep(2)

                            last_one = data.last_one()
                            print(f"last one  = {last_one}")
                            time.sleep(0.1)

                            if last_one < current_power:
                                if direction == 1:
                                    direction = 0
                                else:
                                    direction = 1
                                step_angle = math.ceil(step_angle * 0.75)
                            print(f"step angle in next = {step_angle}, direction in next = {direction}")
                            print(f"num of iterations {i}")
                            print("---------------------------------")
                        not_best_find = False
                        start_pos = True
            except Exception as e:
                print(e)
                data.close()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                quit()
    print("end of programme")
    data.close()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)
    quit()


if __name__ == "__main__":
    main()
