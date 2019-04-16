#/usr/bin/python

import argparse
import csv
import time


DMI_FILEPATH = './data/pi/dmi.csv'
IMU_FILEPATH = './data/pi/imu.csv'
LIDAR_FILEPATH = './data/server/lidar.csv'
GPS_FILEPATH = './data/server/gps.csv'
INSTRUMENTS = ['imu', 'dmi', 'lidar', 'gps']

parser = argparse.ArgumentParser()
parser.add_argument('--delay', help='delay in seconds between rows')
parser.add_argument('-i', '--instrument', help='which instrument to spoof {0}'.format(INSTRUMENTS))
args = parser.parse_args()
delay = float(args.delay)
instrument = args.instrument.lower()
if 'dmi' in instrument:
    filepath = DMI_FILEPATH
elif 'imu' in instrument:
    filepath = IMU_FILEPATH
elif 'lidar' in instrument:
    filepath = LIDAR_FILEPATH
elif 'gps' in instrument:
    filepath = GPS_FILEPATH
else:
    print('ERROR: ARGUMENT {0} NOT IN INSTRUMENTS {1}'.format(args.instrument, INSTRUMENTS))
    assert False


def spoof_from_csv(csv_filepath, delay_between_rows):
    """
    Act like the data from a csv is coming from an instrument collecting live data
    """
    with open(csv_filepath, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(','.join(row))
            # send to kafka
            # wait for delay
            time.sleep(delay_between_rows)


if __name__ == "__main__":
    try:
        while True:
            spoof_from_csv(filepath, delay)
    except KeyboardInterrupt:
        print('\nInterrupted. Exitting')
