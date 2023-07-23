import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Konfigurasi I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inisialisasi modul ADS1115
ads = ADS.ADS1115(i2c)

# Konfigurasi penguatan (GAIN) ADC, pilih sesuai dengan kebutuhan
# Pilihan GAIN: 2/3 (±6.144V), 1 (±4.096V), 2 (±2.048V), 4 (±1.024V), 8 (±0.512V), 16 (±0.256V)
GAIN = 2

# Pilih saluran (channel) ADC yang akan digunakan, misalnya 0 atau 1
CHANNEL = 0

# Buat objek AnalogIn untuk membaca nilai analog dari saluran yang dipilih
analog_in = AnalogIn(ads, CHANNEL, gain=GAIN)

try:
    while True:
        # Baca nilai analog dari potensiometer
        analog_value = analog_in.value
        
        # Konversi nilai analog ke tegangan (dalam volt)
        voltage = analog_in.voltage

        # Tampilkan nilai analog dan tegangan
        print("Nilai Analog:", analog_value)
        print("Tegangan (Volt):", voltage)

        # Tunggu sejenak sebelum membaca kembali
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")
