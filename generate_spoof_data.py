#/usr/bin/python

import argparse
import csv
import time

import avro_schemas

from kafka import KafkaProducer
from kafka.errors import KafkaError
producer = KafkaProducer(bootstrap_servers='localhost:9092')

DMI_FILEPATH = './data/pi/dmi.csv'
IMU_FILEPATH = './data/pi/imu.csv'
LIDAR_FILEPATH = './data/server/lidar.csv'
GPS_FILEPATH = './data/server/gps.csv'
INSTRUMENTS = ['imu', 'dmi', 'lidar', 'gps']

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delay', help='delay in seconds between rows')
parser.add_argument('-i', '--instrument', help='which instrument to spoof {0}'.format(INSTRUMENTS))
args = parser.parse_args()
delay = float(args.delay)
instrument = args.instrument.lower()
if 'dmi' in instrument:
    filepath = DMI_FILEPATH
    schema = avro_schemas.dmi
    field_names = [d['name'] for d in schema['fields']]
    topic = 'dmi'
elif 'imu' in instrument:
    filepath = IMU_FILEPATH
    schema = avro_schemas.imu
    field_names = [d['name'] for d in schema['fields']]
    topic = 'imu'
elif 'lidar' in instrument:
    filepath = LIDAR_FILEPATH
    schema = avro_schemas.lidar
    field_names = [d['name'] for d in schema['fields']]
    topic = 'lidar'
elif 'gps' in instrument:
    filepath = GPS_FILEPATH
    schema = avro_schemas.gps
    field_names = [d['name'] for d in schema['fields']]
    topic = 'gps'
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
            coordinate_id = str(int(time.time() * 10**9))
            row[0] = coordinate_id
            message = ','.join(row)
            print(message)
            # send to kafka
            producer.send(topic, bytes(message, 'utf-8'))
            # wait for delay
            time.sleep(delay_between_rows)


if __name__ == "__main__":
    try:
        while True:
            spoof_from_csv(filepath, delay)
    except KeyboardInterrupt:
        print('\nInterrupted. Exitting')

