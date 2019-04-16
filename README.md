# Instrument Data Spoofer
Create spoofed data to test streaming and aggregation architecture.

## Quick Use
python3 generate_spoof_data.py --delay=0.02 --instrument='lidar'

The `delay` option sets the time to sleep between rows. The `instrument` option selects which data source to spoof.

## Options
```usage: generate_spoof_data.py [-h] [--delay DELAY] [-i INSTRUMENT]

optional arguments:
  -h, --help            show this help message and exit
  --delay DELAY         delay in seconds between rows
  -i INSTRUMENT, --instrument INSTRUMENT
                        which instrument to spoof ['imu', 'dmi', 'lidar',
                        'gps']
```
