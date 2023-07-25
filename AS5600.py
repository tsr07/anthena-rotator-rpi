import smbus
import time

# Alamat I2C sensor AS5600 (pastikan sesuai dengan alamat yang benar)
AS5600_ADDRESS = 0x36

# Register untuk membaca sudut
REG_ANGLE = 0x0C

bus = smbus.SMBus(1)

def read_angle():
    # Membaca 2 byte data dari register sudut
    data = bus.read_i2c_block_data(AS5600_ADDRESS, REG_ANGLE, 2)
    
    # Menggabungkan byte data menjadi nilai sudut
    angle = (data[0] << 8) | data[1]
    
    # Konversi nilai sudut menjadi derajat (0-360)
    degrees = (angle / 4096) * 360
    
    return degrees

def bacaSudut() :
	data = []
	for i in range(0, 5):	
			angle_degrees = read_angle()
			data.append(angle_degrees)
			last_time_baca = time.time()
			time.sleep(0.05)
	sudut_real = 360 - max(data)
	data = []
	return	sudut_real
	
ALPHA = 0.8

def low_pass_filter(current_value, previous_value):
    return (ALPHA * current_value) + ((1 - ALPHA) * previous_value)


try:
	data_sudut_lama = 0
	data_sudut = 0
	
	while True:
		data_sudut = bacaSudut()
		data = low_pass_filter(data_sudut, data_sudut_lama)
		
		print("Sudut Derajat: {:.2f} {:2f}".format(data, data_sudut))
		data_sudut_lama  = data
		#time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")
