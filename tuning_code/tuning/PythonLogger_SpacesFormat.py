import serial

# Set up serial connection
ser = serial.Serial("COM4", 9600)

def read_serial_data():
    ser_line = ser.readline().decode('utf-8').strip()
    data = ser_line.split(' ')
    
    if len(data) == 4:
        try:
            u_val = int(data[0])
            d_val = int(data[1])
            l_val = int(data[2])
            r_val = int(data[3])
            return u_val, d_val, l_val, r_val
        except ValueError:
            pass
    
    return None, None, None, None

def log_data_to_file(u_val, d_val, l_val, r_val):
    with open("serial_data_log.txt", "a") as f:
        f.write(f"{u_val} {d_val} {l_val} {r_val}\n")

if __name__ == "__main__":
    while True:
        u_val, d_val, l_val, r_val = read_serial_data()
        
        if all(val is not None for val in (u_val, d_val, l_val, r_val)):
            print(f"u_val: {u_val}, d_val: {d_val}, l_val: {l_val}, r_val: {r_val}")
            log_data_to_file(u_val, d_val, l_val, r_val)
