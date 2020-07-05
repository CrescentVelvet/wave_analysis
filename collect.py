'''
@Author: your name
@Date: 2020-06-30 19:57:03
@LastEditTime: 2020-07-05 21:20:08
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \wkl\collect.py
'''
#coding=utf-8
import serial.tools.list_ports
import time

# 查询参数、设置参数 收包解包
def parse_param(datas):
    """
    :param datas: str()
    :return: dict()
    """
    HEAD = datas[:12]
    if HEAD != 'FAF501814000'.lower() and HEAD != 'FAF502814000'.lower(): # 前一个是查询，后一个是设置
        print('parse_param error!!!')
        return {}
    return {
        'HEAD': datas,
        'GAIN_0:': eval('0x' + datas[12:14]),
        'GAIN_1:': eval('0x' + datas[14:16]),
        'VOL': eval('0x' + datas[16:18]),
        'VOH': eval('0x' + datas[18:20]),
        'M_T': eval('0x' + datas[20:28]),
        'COUNT': eval('0x' + datas[28:36]),
        'MODE': eval('0x' + datas[36:38]),
        'SOURCE': eval('0x' + datas[38:40]),
        'RESERVE': datas[40:76],
        'SN': datas[76:108],
        'ver': datas[108:124],
        'HOUR': eval('0x' + datas[124:126]),
        'MIN': eval('0x' + datas[126:128]),
        'SEC': eval('0x' + datas[128:130]),
        'YR': eval('0x' + datas[130:134]),
        'MON': eval('0x' + datas[134:136]),
        'DAY': eval('0x' + datas[136:138]),
        'WD': eval('0x' + datas[138:140]),
    }

# 查询数据、查询清零数据 收包接包
def parse_signal(datas):
    """
    :param datas: str()
    :return: dict()
    """
    HEAD = datas[:12]
    print(HEAD)
    if HEAD != 'FAF501820010'.lower() and HEAD != 'FAF502820010'.lower():# 前一个是查询数据，后一个是查询清零数据
        print('parse_param error!!!')
        return {}
    signal = []
    for i in range(0,1024):
        signal.append(eval('0x' + datas[12+8*i, 20+8*i]))
    return {
        'HEAD': HEAD,
        'DATA': signal
    }

# 查询数据和参数、查询数据和参数并清零数据
def parse_signal_and_params(datas):
    """
    :param datas: str()
    :return: dict()
    """
    HEAD = datas[:12]
    print(HEAD)
    if HEAD != 'FAF503824010'.lower() and HEAD != 'FAF504824010'.lower():# 前一个是查询数据和参数，后一个是查询数据和参数并清零数据
        print('parse_param error!!!')
        return {}
    signal = []
    for i in range(0,1024):
        signal.append(eval('0x' + datas[12+8*i, 20+8*i]))
    params = HEAD + datas[8204:]
    return {
        'HEAD': HEAD,
        'DATA': signal,
        'GAIN_0:': eval('0x' + params[12:14]),
        'GAIN_1:': eval('0x' + params[14:16]),
        'VOL': eval('0x' + params[16:18]),
        'VOH': eval('0x' + params[18:20]),
        'M_T': eval('0x' + params[20:28]),
        'COUNT': eval('0x' + params[28:36]),
        'MODE': eval('0x' + params[36:38]),
        'SOURCE': eval('0x' + params[38:40]),
        'RESERVE': params[40:76],
        'SN': params[76:108],
        'ver': params[108:124],
        'HOUR': eval('0x' + params[124:126]),
        'MIN': eval('0x' + params[126:128]),
        'SEC': eval('0x' + params[128:130]),
        'YR': eval('0x' + params[130:134]),
        'MON': eval('0x' + params[134:136]),
        'DAY': eval('0x' + params[136:138]),
        'WD': eval('0x' + params[138:140]),
    }

# bps = 115200
# time_out = 1
# port_list = list(serial.tools.list_ports.comports())
# for i in range(len(port_list)):
#     print(i, '---', serial.Serial(list(port_list[i])[0], bps, timeout=time_out).name)
# COM_NUM = input('Please input an order number to choose a COM:')
# ser = serial.Serial(list(port_list[int(COM_NUM)])[0], bps, timeout=time_out)


# cmd_query_data = bytes.fromhex('fa f5 01 02 00 00 0e fe') # 查询数据
# cmd_query_param = bytes.fromhex('fa f5 01 01 00 00 0f fe') # 查询参数
# cmd_enable_MCA = bytes.fromhex('fa f5 01 00 00 00 10 fe') # enable_MCA
# cmd_disable_MCA = bytes.fromhex('fa f5 02 00 00 00 0f fe') # disable_MCA
# cmd_query_data_and_clear = bytes.fromhex('fa f5 02 02 00 00 0d fe') # 查询数据并清零
# cmd_query_data_and_param = bytes.fromhex('fa f5 03 02 00 00 0c fe') # 查询数据和参数
# cmd_query_param = bytes.fromhex('fa f5 04 02 00 00 0b fe') # 查询数据和参数并清零数据


# while True:
#     # if ser.in_waiting:
#     if True:
#         ser.write(cmd_query_param)
#         recv = ser.read(4104).hex()
#         print(recv)
#         parsed = parse_signal(recv)
#         print(parsed)
#         time.sleep(1)
# ser.close()  # close serial