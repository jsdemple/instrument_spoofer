#/usr/bin/python

import argparse
import csv
import time

from utils import parse_line_into_schema

from fastavro import writer, reader, parse_schema
import avro_schemas

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
    schema = avro_schemas.dmi
    field_names = [d['name'] for d in schema['fields']]
    topic = 'dmi'
elif 'imu' in instrument:
    filepath = IMU_OUT_FILEPATH
    schema = avro_schemas.imu
    field_names = [d['name'] for d in schema['fields']]
    topic = 'imu'
elif 'lidar' in instrument:
    filepath = LIDAR_OUT_FILEPATH
    schema = avro_schemas.lidar
    field_names = [d['name'] for d in schema['fields']]
    topic = 'lidar'
elif 'gps' in instrument:
    filepath = GPS_OUT_FILEPATH
    schema = avro_schemas.gps  
    field_names = [d['name'] for d in schema['fields']]
    topic = 'gps'
else:
    print('ERROR: ARGUMENT {0} NOT IN INSTRUMENTS {1}'.format(args.instrument, INSTRUMENTS))
    assert False

parsed_schema = parse_schema(schema)

consumer = KafkaConsumer(topic,
                         group_id='A',
                         bootstrap_servers=['localhost:9092'])
 

def write_to_disk(line, filepath):
    try:
        with open(filepath, 'ab') as f:
            f.write(line)
            f.write('\n'.encode())
    except EnvironmentError as err:
        print('ERROR WRITING TO DISK: {0}'.format(err))


def write_to_avro(line, schema, filepath):
    try:
        with open(filepath, 'a+b') as out:
            writer(out, parsed_schema, line)
    except EnvironmentError as err:
        print('ERROR WRITING TO DISK (AVRO): {0}'.format(err))


#def parse_line_to_avro(line, schema):



if __name__ == "__main__":
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
        #                                      message.offset, message.key,
        #                                      message.value))
        raw_line = message.value
        row = raw_line.decode('utf-8').split(',')
        record = parse_line_into_schema(row, schema)

        #line = message.value.decode('utf-8').split(',')
        #line = [int(x) for x in line]
        #line = message.value
        print(raw_line)
        print(record)
        #records = [(dict(zip(field_names, line)))]
        #print(records)
        #write_to_avro(records, parsed_schema, filepath)

