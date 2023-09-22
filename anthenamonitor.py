import sys
import smbus
import time

path_to_library = "/home/pi/.local/lib/python3.9/site-packages"
sys.path.append(path_to_library)

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
import RPi.GPIO as GPIO


certificate = {
    "type": "service_account",
    "project_id": "rotator-antena",
    "private_key_id": "5c07dbb6f2e2e6c986a43ba3deb2e50d41359604",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCfYl0+XXNTigNt\nQIXV+2+5opsZ6N7CXpt9sTqgXLbUe29/uJvG0r5gd1cCcWHy4tqb7zylNvTKLETo\n2tB/wiy7HhVkMouaqqwYFsXNeB3KAtNajh1SJ28uNKEaSoyMUz0+/QHQt306fa4e\nLHscc55evLb7Sm+LSTXQZWeCTEmfRkkw+HCqvq1qiauZRkTN5d1IoWUWmWnPRJi3\ncpISpf2doLVFS4aXS1St17N8896eilQYsGWgzYXnWwUH50HJzwodPJFqq3t6Aqfn\nG5syrN61SjGpw8RYl0U1a+qSnNklGf14mh044sVCdKbao9EjGJjuA4HNtCKc69mS\nUifMbwTDAgMBAAECggEADDJDvlz6UT8zae3REAHQl9z4j3ABc9A3h9PDD7hoiTP0\n4UooKXvA87LOJrK0cxim793LvzzIWJwwnbz4zX33XE4+Bs/TXP+IccN0WXfCl83F\njJ1pYvr/iAKg/VkNDkPkYOiNdgJEg/BQHaD7vr6eNNOuEOauSHNOuea4mADsdVKV\npVP+AT7HFnLD+T2t9yVAzn+VAXzlJ/J8yjLJyVrxXOluqSOnNf2EGgtOlqi27wm3\nGzvHB0Cr6cpBdGFNa8lkfesp4fyRgcoBgDLm7wFnRk4WFL2CGOt2NubRpL241XTw\nXoTrSnqreGlFeTyD1ZYYpwXYKgbgrLyoH+w3OJD74QKBgQDOS4c+f2s1NYiSHSUb\nYEIrQQhj9iVpGQ96hR9YLgomL1Wmso1sCPOnoCpE/UdzgvpRCKa5dqJCUAZwbTms\nksfIwzjZP1yaII26yRQErcYzuK2Z2yJliVWZX22kuGIOH75QqcvLhFRL3oG/r8ou\nAKDa/3qlN/83nkQYxelHpGADEQKBgQDFyVV15XQ5go1NwaxOFr8cKzVi4MBwJ7Pu\niOwPq4BKZVHEERFK0EIHBTvfAfsNJJ2iVNrZZAU5xD41n+WxipoAMy96CZgbeTuV\n+EkTBvOEdhW1He1WHBrERNB0vGZOgi3lFtF+ZuqQtvbW6JeHJ+HbLPCHPbMlg52N\nAeOv4JUikwKBgQCtLwbo1rs/viNa1pDSPKsP+NZ8ZKXfZyRxbNR1iKEIkXBMM1U6\nPwGd1X3m0OJs/KX75VFiHU/2b4wYUfm7ALYruog9CU5KLc4N4sSlcOUVgpJquWZU\n60grK8u2Hvxicw+oVAM8ZWkHEFLIg2Et4WUotJVXonzlSj5MtckzVbEsoQKBgQCF\nq6A6Yay/AWCGYJIW5ICchQc7oDHumqacW6VOodW+ceNk4zQQn9c/72WbPjdxloGC\nqF6P9W0isWJp03rlFosl/3HixIEscC65GGgql9QUfcoF8gfo3m2on+lSO9HY1Vo3\nLci/6MY2r7D7ZY6jJW0bN7AHdseQXvcnyVMcFmg0SQKBgCBsVYI7j6B/wYRNB5Jy\nWTlSVpKy3tGHral5o9tEALacYZartV/DOu5KRwm2DMtxKTXBsVrge1MbZZi62lfD\n36EkhlWqNgLraMtoCahVqNVgyrzknZtTBuL55IjxmuFzv5XPjft6l/1yGHsp7bxX\nCEx1FgyOOSYn6+08PGz6xtn9\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-gl3ag@rotator-antena.iam.gserviceaccount.com",
    "client_id": "113103775624449184445",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-gl3ag%40rotator-antena.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rotator-antena-default-rtdb.firebaseio.com/'
})
ref = db.reference()
AS5600_ADDRESS = 0x36
# Register untuk membaca sudut liat datasheet
REG_ANGLE = 0x0E

bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RPWM = 13  # GPIO pin 13 to the RPWM on the BTS7960
LPWM = 19  # GPIO pin 19 to the LPWM on the BTS7960

# For enabling "Left" and "Right" movement
L_EN = 5  # connect GPIO pin 5 to L_EN on the BTS7960
R_EN = 6  # connect GPIO pin 6 to R_EN on the BTS7960

# Set all of our PINS to output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)

# Enable "Left" and "Right" movement on the HBRidge
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)

rpwm = GPIO.PWM(RPWM, 50)
lpwm = GPIO.PWM(LPWM, 50)

rpwm.ChangeDutyCycle(0)
rpwm.start(0)

waktu_lama = 0
PWM_VALUE = 20

def read_angle():
    # Membaca 2 byte data dari register sudut
    data = bus.read_i2c_block_data(AS5600_ADDRESS, REG_ANGLE, 2)

    # Menggabungkan byte data menjadi nilai sudut
    angle = (data[0] << 8) | data[1]

    # Konversi nilai sudut menjadi derajat (0-360)
    degrees = map_value(((angle / 4096) * 360), 0,360,360,0)

    return degrees



def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low



try:
    previous_input = db.reference('input_degree').get()
    while True:
        sudut = read_angle()
        sudut = int(sudut)

        # Mengambil data sudut yang diinginkan dari Firebase Realtime Database
        target_degree = db.reference('input_degree').get()
        kiri = db.reference('kiri').get()
        kanan = db.reference('kanan').get()
        
        if time.time() - waktu_lama > 0.5:
            waktu_lama = time.time()
            ref = db.reference()
            ref.update({'degree': sudut})

        if target_degree != previous_input:
            previous_input = target_degree
            if target_degree is not None:
                while True:
                    sudut = read_angle()
                    sudut = int(sudut)
                    error = int(eval(target_degree)) - sudut
                    print(f"target_degree: {target_degree} | degree: {sudut} | err: {error} | pwm: {PWM_VALUE}")
                    stop = db.reference('stop').get()
                    
                    if stop == 'true':
                        #print("test")
                        ref = db.reference()
                        ref.update({'stop': 'false'})
                        lpwm.ChangeDutyCycle(0)
                        rpwm.ChangeDutyCycle(0)
                        error = 0.8
                   
                    if time.time() - waktu_lama > 0.5:
                        waktu_lama = time.time()
                        ref = db.reference()
                        ref.update({'degree': sudut})

                    if abs(error) > 0.8:
                        if error > 0:
                            print("Gerakkan ke kanan")
                            rpwm.ChangeDutyCycle(PWM_VALUE)
                            lpwm.ChangeDutyCycle(0)
                        # Tambahkan logika kendali motor untuk gerakan ke kiri
                        elif error < 0:
                            lpwm.start(0)
                            rpwm.ChangeDutyCycle(0)
                            lpwm.ChangeDutyCycle(PWM_VALUE)
                            print("Gerakkan ke kiri")
                        # Tambahkan logika kendali motor untuk gerakan ke kanan
                    else:
                        print("Sudut sudah tepat")
                        rpwm.ChangeDutyCycle(0)
                        lpwm.ChangeDutyCycle(0)
                        break
                        # Tambahkan logika kendali motor untuk berhenti

        else:

            if kanan == "true" and kiri == "false":
                print("Speeding up {} ke kiri".format(PWM_VALUE))
                lpwm.start(0)
                lpwm.ChangeDutyCycle(PWM_VALUE)

            if kanan == "false" and kiri == "false":
                print("stop")
                rpwm.ChangeDutyCycle(0)
                lpwm.ChangeDutyCycle(0)
            if kiri == "true" and kanan == "false":
                print("Speeding up {} ke kanan".format(PWM_VALUE))
                rpwm.ChangeDutyCycle(PWM_VALUE)
            if kiri == "true" and kanan == "true":
                print("stop")
                rpwm.ChangeDutyCycle(0)
                lpwm.ChangeDutyCycle(0)

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")
















