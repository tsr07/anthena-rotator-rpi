import RPi.GPIO as GPIO

# Tentukan mode pin GPIO menggunakan BCM numbering
GPIO.setmode(GPIO.BCM)

# Tentukan pin GPIO yang digunakan (gunakan GPIO 4 atau GPIO 5)
ADC_PIN = 4  # Misalnya, menggunakan GPIO 4 (BCM 4)
 
# Inisialisasi pin sebagai input
GPIO.setup(ADC_PIN, GPIO.IN)

try:
    while True:
        # Baca nilai analog dari potensiometer
        analog_value = GPIO.input(ADC_PIN)

        # Tampilkan nilai analog
        print("Nilai Analog:", analog_value)

except KeyboardInterrupt:
    print("\nProgram dihentikan oleh pengguna.")

finally:
    # Setelah selesai, kembalikan mode pin GPIO ke default
    GPIO.cleanup()
