import sys

path_to_library = "/home/pi/.local/lib/python3.9/site-packages"
sys.path.append(path_to_library)

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
import RPi.GPIO as GPIO
import time

certificate = {
  "type": "service_account",
  "project_id": "antenaproject-fab4e",
  "private_key_id": "6f34e17311cd7ff7900ae767f7b8a8292c49dff9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwj/fdKWvpxHI7\nrnfbkD9gORqI04BdQwKquAmvuOvllJ+VkiAGkcyBjVikuwphBf/dGqO6klcm5ITO\nK3NHEVfj6wQz2BMQIEC4JSVKCuw9XL9cdSq5BNMJb2zNZeqkEzILyiHRX1g0ZsaM\nAeIk2H/5QNE17RlSFwHuN5GP8UgrCkqqbaAKwKH1lS/Nbd5mOV+/RcSEVquoQzda\n4WqJRLNBiqcCAHBCyLucmm0LJ7oEI7V1xzxvOPPV1yex3fvI61kcTUuL864FoX+7\nIKpVsSPi5Mj77t1o+D/4xRrcY+ChpzlLst2aeJORG5pizd3GvUnDutk2ZgUmfpSY\neS7Kw4MXAgMBAAECggEAOuOBzcuLeRgy65H42wwE/1B8d6dnWHPJt2wTmv7n+xYz\nldz7foVxesJMjwDtaMfp+3JvqoI1vDyayPL4C3uO329a4vnN/eJsA58sDUKQYbUG\nBE319mjUBIEb/nPgK2JVnlYIKn+M+UlQLpFQPm7RXC6QuNZATD9tPulczPAyXFwP\npblkyA+t+txacnzgfvyDNCVA6BqYkY9yrLC6h9dSYfcYLn49pR3zdSRYcadp4Ixi\nVqSQs731IMfxeIJY3QD0kh5AxcPIDASxkUNdY69FabE1AOgZVbFoe+O6RiDZB7eC\nsJiGX9TZhPsijzEd4A3ncl/JGrWM3VOx30r4XminNQKBgQDlrq38LbV2U+cPfXzi\nsYNIKaODkex/JaeO9h7ru6mDDQIof2pF6k12rYEj0aNB3mMQSZb89co3ddDyqH7W\n3Wq7xuxk7OswSUB6RLy7P7cZIbGsDwRULI8z3M+21jU7ZQtqXW7c0jHpj4GOjrYW\nMkp8qNLwIvaGBcQh0fIQU6UYNQKBgQDEyxwFl5mAi/T6dMJUc+2P9JY7JTzS/XOn\nXIEPPJyA1LtYOTs3duJKUH1ZhwDw2T4qpQNk3D4CyHHhquDFTTQVayESzCndpq4l\nzgedX2+5zczPH5RpTPZDyfln6gOgZilGYgP/v13d35tUAnmYSTuRn7+3V6AC68Lx\nXgg3D6/PmwKBgBVtYGngUceCOFInoNj9OoQm7kw99tQ9zQ33RBc14LCLLCJfEKkJ\nHMTvltainhptBszkMKPUwlK+OQoKUhr1eRmfizo3KBHPI6bEdt75KLm9fPfSRtMb\nfRiXhwFFpp2t5Yy8vrT3HxTtAGcuRSp48p4CmfsxJ9KFAzEshuqjAwnpAoGBAKCO\nSY1ycyWCiltwuT+n2XEyjwMwTWCisiIggZdJzzH43eSLxPlqgBM7ehl54NWfmG24\ndX1rhxhEK01/WaT/aPf0kGZCtgGFxN1JK8NEouXHt0phLHeA+Aa0mUwji9PopdIr\nk7Grksy7a4HuBwCs9vHHkOXnkr/vU/wSyMcLgFfzAoGAPUM4vABFmp8NoVxKCzFS\nzfppWOfS+qFPiGDBCSNRxSCyuU8a/ftI+MasON/2lQE/gkYO05PAoyj/FHkJt4TD\ni9wVZjPGJwOZ6gftyMoa7skYpRgunNeVaJFpKAniL01EoiooD7lmaVR8Y8l+y3+t\nkiAajV8zftn4+0ddxw8fnjE=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-medhc@antenaproject-fab4e.iam.gserviceaccount.com",
  "client_id": "113622627910152661803",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-medhc%40antenaproject-fab4e.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

RPWM = 13;  # GPIO pin 19 to the RPWM on the BTS7960
LPWM = 19;  # GPIO pin 26 to the LPWM on the BTS7960

# For enabling "Left" and "Right" movement
L_EN = 5;  # connect GPIO pin 20 to L_EN on the BTS7960
R_EN = 6;  # connect GPIO pin 21 to R_EN on the BTS7960


# Set all of our PINS to output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)


# Enable "Left" and "Right" movement on the HBRidge
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)


rpwm= GPIO.PWM(RPWM, 50)
lpwm= GPIO.PWM(LPWM, 50)

rpwm.ChangeDutyCycle(0)
rpwm.start(0) 


cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://antenaproject-fab4e-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

#db =firestore.client()
#data = {"message": "data masuk lurrr"}
#db.collection("message").add(data)

ref = db.reference()






counter = 0
while True :
    kiri = ref.child('kiri').get()
    kanan = ref.child('kanan').get()
    # print("Kanan : {}    |    Kiri : {}".format(kanan, kiri))

    if kanan == "true" and kiri == "false":
      print("Speeding up " + str(counter), kanan)
      rpwm.ChangeDutyCycle(counter)
      counter += 10
      if counter >= 50 :
        counter = 50
      #time.sleep(0.05)
    if kanan == "false" and kiri == "false":
      print("stop")
      rpwm.ChangeDutyCycle(0)
      lpwm.ChangeDutyCycle(0)
      counter=0    
    if kiri == "true" and kanan == "false":
        lpwm.start(0)
        print("Speeding up " + str(counter), kiri)
        lpwm.ChangeDutyCycle(counter)
        counter += 10
        if counter >= 50 :
          counter = 50
