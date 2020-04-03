# import PySimpleGUI as sg
from __init__ import *
print('1')
# sync_timer_edit(1,2)
print('2')
filepath = sg.PopupGetFile('put an SEQ file here', file_types=(("SEQ Files", "*.seq"),))
SEQ = SEQObject(filepath)
# SEQ.expand_seq_file(0x48)
# SEQ.write_to_file()
# SEQ.expand_seq_file(1000)
start = int(sg.PopupGetText('Input the action state you want to edit in hex'), 16)
print(SEQ.action_id_table[start])
print(start)
temp_data = build_MoveData(SEQ, start)

# print(test.action_id_table[start])
# print(temp_list[end])

window = build_MoveData_window(temp_data)
display_MoveData_window(window, temp_data, SEQ)

# SEQ.expand_seq_file(0x1200)
# SEQ.write_to_file()
