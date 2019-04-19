#/usr/bin/python

# Avro Schemas for Sidewalk Instruments

dmi = {
 "namespace": "dmi.avro",
 "type": "record",
 "name": "sidewalk_rig",
 "fields": [
     {"name": "coordinate_id",  "type": "int"},
     {"name": "record_no", "type": "int"},
     {"name": "left_total",  "type": "int"},
     {"name": "right_total", "type": "int"},
     {"name": "left",  "type": "int"},
     {"name": "right", "type": "int"},    
     ]
}
