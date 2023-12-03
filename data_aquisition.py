import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import pandas as pd
# import matplotlib.pyplot as plt


def data_aquisition(t, freq):
    x = []
    i2c = busio.I2C(board.SCL, board.SDA)

    ads = ADS.ADS1115(i2c)
    ads.mode = Mode.CONTINUOUS
    ads.gain = 2/3
    # ads.data_rate = 16

    channel = AnalogIn(ads, ADS.P0)
    # _ = channel.value

    i = 0
    T = 1 / freq
    start = time.time()
    while (time.time() - start) <= t:
        i += 1
        print(f'| {i}. | Kanał: {channel.value} | Napięcie: {channel.voltage} |')
        x.append(round(channel.voltage, 4))
        time.sleep(T)

    return x

# fig, ax = plt.subplots()
# ax.plot(x)
# ax.set(xlabel='time(s)',ylabel='voltage(V)')
# ax.grid()
# fig.savefig("plot.png")
# plt.show()


def save_to_file(data, fn):
    df = pd.DataFrame()
    # df['channel'] = data_ch
    df['voltage'] = data
    df.to_csv(f'{fn}.csv', index=False, header=True)
