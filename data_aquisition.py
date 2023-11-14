import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import pandas as pd
# import matplotlib.pyplot as plt


def data_aquisition(t, interval):
    x = []
    i2c = busio.I2C(board.SCL, board.SDA)

    ads = ADS.ADS1115(i2c)

    channel = AnalogIn(ads, ADS.P0)

    for _ in range(0, t):
        print("Warotśc na wejściu: ",channel.value, "Napięcie: ", channel.voltage)
        x.append(channel.voltage) 
        time.sleep(interval)

    return x
    
# fig, ax = plt.subplots()
# ax.plot(x)
# ax.set(xlabel='time(s)',ylabel='voltage(V)')
# ax.grid()
# fig.savefig("plot.png")
# plt.show()

def save_to_file(data):
    df = pd.DataFrame(data)
    df.to_csv('data.csv',index=False, header=False)



