#!/usr/bin/env python
#
# Copyright (c) 2015-2021 University of Antwerp, Aloxy NV.
#
# This file is part of pyd7a.
# See https://github.com/Sub-IoT/pyd7a for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import os
from time import sleep
import sys
import struct
import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS, ResponseMode
from modem.modem import Modem

# This example can be used with a node running the gateway app included in Sub-IoT, which is connect using the supplied serial device.
# It will query the sensor file (file 0x40) from other nodes running sensor_pull, using adhoc synchronization and print the results.
from util.logger import configure_default_logger

from examples.influxdb_gas import influx_db_gateway


def received_command_callback(cmd):
  logging.info(cmd)
  #if cmd.execution_completed:
  #  os._exit(0)
  try:
    cmd = str(cmd)
    first_split = cmd.split('[', 1)[1]
    first_split = first_split.split(']', 1)[0]
    second_split = [x.strip() for x in first_split.split(',')]
    int_split = [int(x) for x in second_split]
    logging.info(int_split)
    #continue adjustmens before sending to gateway
    x_coord = int_split[0]
    y_coord = int_split[1]
    byte_data = int_split[2:6]
    data_type = chr(int_split[6])
    logging.info(x_coord)
    logging.info(y_coord)
    if (data_type == 'T' or data_type == 'H'):
      float_data = bytearray(byte_data) 
      #logging.info(float_data)
      float_data = struct.unpack('<f', float_data)[0]
      float_data = round(float_data,2)
      logging.info(float_data)
      #send data to database
      db_gateway = influx_db_gateway.InfluxDbGateway()
      result = db_gateway.insert_data({"type": data_type, "x": x_coord, "y": y_coord, "value": float_data})
    elif (data_type == 'L'):
      ch1 = (byte_data[1] << 8) | byte_data[0] #infrared
      ch0 = (byte_data[3] << 8) | byte_data[2] #infrared+visible light
      #logging.info(ch1)
      #logging.info(ch0)
      visible_light = ch0 - ch1
      logging.info(visible_light)
      #send data to database
      db_gateway = influx_db_gateway.InfluxDbGateway()
      result = db_gateway.insert_data({"type": data_type, "x": x_coord, "y": y_coord, "value": float(visible_light)})
    logging.info(data_type)
  except:
    pass


def write_file(x, y, data_type):
  modem.execute_command_async(
    alp_command=Command.create_with_write_file_action(
      file_id=0x30,
      data = [ord(data_type),int(x),int(y)],
      offset = 0,
      interface_type=InterfaceType.D7ASP,
      interface_configuration=Configuration(
        qos=QoS(resp_mod=ResponseMode.RESP_MODE_NO),
        addressee=Addressee(
          access_class=0x11,
          id_type=IdType.NOID
        )
      )
    )
  )

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
config = argparser.parse_args()

configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)
modem.connect()

"""
modem.execute_command_async(
  alp_command=Command.create_with_read_file_action(
    file_id=0x40,
    length=2,
    interface_type=InterfaceType.D7ASP,
    interface_configuration=Configuration(
      qos=QoS(resp_mod=ResponseMode.RESP_MODE_ALL),
      addressee=Addressee(
        access_class=0x11,
        id_type=IdType.NOID
      )
    )
  )
)
"""

try:
  while True:
    logging.info("Type x coordinate:")
    inp_x = input()
    if int(inp_x) <= 255 and int(inp_x) >= 0:
      logging.info("Type y coordinate:")
      inp_y = input()
      if int(inp_y) <= 255 and int(inp_y) >= 0:
        logging.info("Data type request: type T (for temp) or H (for hum) or L (for light)")
        inp = input()
        if inp == "T" or inp == "H" or inp == "L":
          write_file(inp_x, inp_y, inp)
          logging.info("Executing query...")
          #sleep(5)
except KeyboardInterrupt:
  sys.exit(0)
