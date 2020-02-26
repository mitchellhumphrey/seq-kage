import PySimpleGUI as sg
from __init__ import *

filepath = sg.PopupGetFile('put an SEQ file here')
test = SEQObject(filepath)


filepath2 = sg.PopupGetFile('put an SEQ file here')
test2 = SEQObject(filepath2)
print(type(test.data))
print(hex(test.action_id_table[0xa0]))
print(hex(test2.action_id_table[0xa0]))
