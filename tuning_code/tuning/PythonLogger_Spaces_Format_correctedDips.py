import serial
import numpy as np

# Set up serial connection
ser = serial.Serial("COM4", 9600)

def correct_dip(data):
    corrected_data = []
    for i, row in enumerate(data):
        if i == 0:
            corrected_data.append(row)
            continue
        
        prev_row = corrected_data[-1]
        corrected_row = list(row)
        
        for j, val in enumerate(row):
            # Check if any other slider has increased by approximately 10
            other_sliders = [x for idx, x in enumerate(prev_row) if idx != j]
            other_sliders_increased = any([abs(x - y) >= 10 for x, y in zip(row, other_sliders)])
            
            # If the value dipped compared to the previous reading and other sliders increased, correct the dip
            if val < prev_row[j] and other_sliders_increased:
                corrected_row[j] = np.interp(i, [0, len(data) - 1], [prev_row[j], row[j] + 10])
        
        corrected_data.append(corrected_row)
    
    return corrected_data

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

def log_data_to_file(original_values, corrected_values):
    with open("serial_data_log.txt", "a") as f:
        f.write(f"Original: {original_values[0]} {original_values[1]} {original_values[2]} {original_values[3]} ")
        f.write(f"Corrected: {corrected_values[0]} {corrected_values[1]} {corrected_values[2]} {corrected_values[3]}\n")

if __name__ == "__main__":
    data_buffer = []
    
    while True:
        u_val, d_val, l_val, r_val = read_serial_data()
        
        if all(val is not None for val in (u_val, d_val, l_val, r_val)):
            print(f"u_val: {u_val}, d_val: {d_val}, l_val: {l_val}, r_val: {r_val}")
            data_buffer.append([u_val, d_val, l_val, r_val])
            corrected_data = correct_dip(data_buffer)
            log_data_to_file((u_val, d_val, l_val, r_val), corrected_data[-1])
