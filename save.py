'''
@Author: your name
@Date: 2020-06-30 21:01:32
@LastEditTime: 2020-07-05 21:22:58
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \wkl\mainWindow.py
'''
import xml.etree.ElementTree as etree

# 读取
def read_data_file(filename):
    doc = etree.parse(filename)
    # TODO: check the validation of the file
    root = doc.getroot()
    # TODO: translate the file to dict
    print(root.find("CLOCK").text)

# 保存
def save_data_file(filename):
    datats = [1,2,3,4,5,6]
    root = etree.Element("MAC")
    etree.SubElement(root, "GAIN_0").text="1.1"
    etree.SubElement(root, "GAIN_1").text='2.2'
    for data,idx in enumerate(datats):
        stringstr = "DATA"+str(idx)
        etree.SubElement(root, stringstr).text=str(data)
    tree = etree.ElementTree(root)
    tree.write('result.xml', encoding='utf-8')