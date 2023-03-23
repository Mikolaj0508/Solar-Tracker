import serial
import time

from datetime import datetime





from datab import Data



with serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=2) as ser:
    time.sleep(0.1)
    if ser.isOpen():
        print(f"{ser.port} connected")
        data = Data()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        timeout = 60*6
        start = time.time()
        try:
            while time.time()<start + timeout:
                #starting measurments
                time.sleep(2)
                cmd = "M"
                d = data.req(char="M", number=0)
                ser.write(cmd.encode())

                
                if ser.inWaiting()>=0:
                    answer=str(ser.readlines())
                    data.resp(d,answer)
                last_one = data.last_one()
                print(f"last one  = {last_one}")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)

                    
        except Exception as e:
            print(e)
            data.close()
            quit()
print("end of programe")
data.close()
quit()
