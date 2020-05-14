# -*- coding: utf-8 -*-

'''
@Author: my name
@Date: 2020-05-11 01:01:24
@LastEditTime: 2020-05-13 20:54:02
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: MultiChannel.py
'''

import serial.tools.list_ports

# 接收
def parse_param(datas):
    """

    :param datas: str()
    :return: dict()
    """
    head = datas[:12]
    if head != 'FAF501814000'.lower():
        print('parse_param error!!!!')
        return {}
    return {
        'head': datas[:12],
        'r_w0': eval('0x' + datas[12:14]),
        'r_w1': eval('0x' + datas[14:16]),
        'low_v': eval('0x' + datas[16:18]),
        'high_v': eval('0x' + datas[18:20]),
        'read_time': eval('0x' + datas[20:28]),
        'pre_set_count': eval('0x' + datas[28:36]),
        'mode': eval('0x' + datas[36:38]),
        'signal': eval('0x' + datas[38:40]),
        'reserve': datas[40:124],
        'hour': eval('0x' + datas[124:126]),
        'min': eval('0x' + datas[126:128]),
        'second': eval('0x' + datas[128:130]),
        'year': eval('0x' + datas[130:134]),
        'month': eval('0x' + datas[134:136]),
        'day': eval('0x' + datas[136:138]),
        'week_day': eval('0x' + datas[138:140]),
    }

# 发送
def parse_signal(datas):
    """

    :param datas: str()
    :return: dict()
    """
    head = datas[:12]
    if head != 'FAF501820010'.lower():
        print('parse_param error!!!!')
        return {}
    return {
        'head': datas[:12],
        'r_w0': eval('0x' + datas[12:14]),
        'r_w1': eval('0x' + datas[14:16]),
        'low_v': eval('0x' + datas[16:18]),
        'high_v': eval('0x' + datas[18:20]),
        'read_time': eval('0x' + datas[20:28]),
        'pre_set_count': eval('0x' + datas[28:36]),
        'mode': eval('0x' + datas[36:38]),
        'signal': eval('0x' + datas[38:40]),
        'reserve': datas[40:124],
        'hour': eval('0x' + datas[124:126]),
        'min': eval('0x' + datas[126:128]),
        'second': eval('0x' + datas[128:130]),
        'year': eval('0x' + datas[130:134]),
        'month': eval('0x' + datas[134:136]),
        'day': eval('0x' + datas[136:138]),
        'week_day': eval('0x' + datas[138:140]),
    }

bps = 115200
time_out = 1
port_list = list(serial.tools.list_ports.comports())
print(len(port_list))
for i in range(len(port_list)):
    print(i, '---', serial.Serial(list(port_list[i])[0], bps, timeout=time_out).name)
# COM_NUM = input('Please input a number to choose a COM:')
COM_NUM = 0
ser = serial.Serial(list(port_list[int(COM_NUM)])[0], bps, timeout=time_out)
# write data
cmd_query_data = bytes.fromhex('fa f5 01 02 00 00 0e fe')
cmd_query_param = bytes.fromhex('fa f5 01 01 00 00 0f fe')
i = 0
while True:
    i += 1
    # if ser.in_waiting:
    if True:
        ser.write(cmd_query_data)
        recv = ser.read(4104).hex()
        # print(recv)
        parsed = parse_signal(recv)
        print(parsed)
ser.close()  # close serial
