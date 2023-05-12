import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

while True:
    try:
        print(GPIO.input(21))
    except KeyboardInterrupt:
        print('Przerwanie na żądanie.')
        break
