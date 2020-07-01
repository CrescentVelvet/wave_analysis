'''
@Author: your name
@Date: 2020-06-30 21:01:32
@LastEditTime: 2020-07-01 13:18:51
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \wkl\mainWindow.py
'''
import xml.etree.ElementTree as etree

# 读取
doc = etree.parse('./example.xml')
root = doc.getroot()
print(root.find("CLOCK").text)

# 保存
datats = [1,2,3,4,5,6]
root = etree.Element("MAC")
etree.SubElement(root, "GAIN_0").text="1.1"
etree.SubElement(root, "GAIN_1").text='2.2'
for data,idx in enumerate(datats):
    stringstr = "DATA"+str(idx)
    etree.SubElement(root, stringstr).text=str(data)
tree = etree.ElementTree(root)
tree.write('result.xml', encoding='utf-8')