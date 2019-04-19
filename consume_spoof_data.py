#/usr/bin/python

import argparse
import csv
import time

from kafka import KafkaConsumer
from kafka.errors import KafkaError
#import avro.schema
#import avro.io
#import io

DATA_OUT_DIR = '/data/'
DMI_OUT_FILEPATH = DATA_OUT_DIR + 'dmi.csv' 
IMU_OUT_FILEPATH = DATA_OUT_DIR + 'imu.csv'
LIDAR_OUT_FILEPATH = DATA_OUT_DIR + 'lidar.csv'
GPS_OUT_FILEPATH = DATA_OUT_DIR + 'gps.csv'
INSTRUMENTS = ['imu', 'dmi', 'lidar', 'gps']

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--instrument', help='which instrument data to save to disk {0}'.format(INSTRUMENTS))
args = parser.parse_args()
instrument = args.instrument.lower()
if 'dmi' in instrument:
    filepath = DMI_OUT_FILEPATH
    topic = 'dmi'
elif 'imu' in instrument:
    filepath = IMU_OUT_FILEPATH
    topic = 'imu'
elif 'lidar' in instrument:
    filepath = LIDAR_OUT_FILEPATH
    topic = 'lidar'
elif 'gps' in instrument:
    filepath = GPS_OUT_FILEPATH
    topic = 'gps'
else:
    print('ERROR: ARGUMENT {0} NOT IN INSTRUMENTS {1}'.format(args.instrument, INSTRUMENTS))
    assert False

consumer = KafkaConsumer(topic,
                         group_id='A',
                         bootstrap_servers=['localhost:9092'])
 
#schema_path="user.avsc"
#schema = avro.schema.parse(open(schema_path).read())


def write_to_disk(line, filepath):
    try:
        with open(filepath, 'ab') as writer:
            writer.write(line)
            writer.write('\n'.encode())
    except EnvironmentError as err:
        print('ERROR WRITING TO DISK: {0}'.format(err))




if __name__ == "__main__":
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
        #                                      message.offset, message.key,
        #                                      message.value))
        #line = message.value.decode('utf-8')
        line = message.value
        write_to_disk(line, filepath)
        print(line)

