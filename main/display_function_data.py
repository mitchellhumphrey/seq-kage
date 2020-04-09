from __init__ import *
from custom_edit_function import *
import PySimpleGUI as sg


def column_builder(offset_column, purpose_column, data_column, MoveData_obj, amount_of_words, purpose, index):
    offset_column.append(
        [sg.Button('0x' + str(hex(index * 4))[2:].upper().rjust(5, '0'), pad=(0, 0), size=(9, 1),
                   key=('offset', index * 4, amount_of_words, purpose))])
    purpose_column.append([sg.Text(purpose, key=('purpose', index * 4, amount_of_words))])
    str_data = ''
    for i in range(amount_of_words):
        str_data = str_data + hex(
            int.from_bytes(MoveData_obj.data[(index * 4) + (4 * i): (index * 4) + 4 * (i + 1)], 'big'))[
                              2:].rjust(8, '0') + ' '
    data_column.append([sg.Text(str_data.upper(), key=('data', index * 4, amount_of_words))])


def build_MoveData_window(MoveData_obj):
    # column_data = [[sg.Column([[]], key='column1'), sg.Column([[]], key='column2'), sg.Column([[]], key='column3')]]
    # layout = [[sg.Button('Quit', key='Quit'), sg.Text('                      SEQ Kage')],
    # [sg.Column(column_data, scrollable=True, vertical_scroll_only=True, size=(950, 700), key='column')]]
    # window = sg.Window('SEQ Kage', layout, font='Courier 12', size=(1000, 800))
    # window.finalize()

    window = update_MoveData_window(MoveData_obj)

    return window


def update_MoveData_window(MoveData_obj):
    """
    :rtype: sg.Window
    """
    # print(MoveData_obj.AF_flag)

    column_data_offset = [[sg.Text('Offset')]]
    column_data_purpose = [[sg.Text('Purpose')]]
    column_data_data = [[sg.Text('Data')]]
    index = 0
    while MoveData_obj.word_length > index:
        if index in MoveData_obj.AF_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'AF Flag', index)
        elif index in MoveData_obj.NF_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'NF Flag', index)
        elif index in MoveData_obj.KF_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'KF Flag', index)
        elif index in MoveData_obj.RF_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'RF Flag', index)
        elif index in MoveData_obj.K2F_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'K2F Flag',
                           index)
        elif index in MoveData_obj.sync_timer_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 3, 'Sync Timer',
                           index)
        elif index in MoveData_obj.N2F_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'N2F Flag',
                           index)
        elif index in MoveData_obj.EF_flag:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'EF Flag', index)
        elif index in MoveData_obj.hitbox_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'Hitbox Location', index)
        elif index in MoveData_obj.hitbox_apperence_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'Hitbox apperance', index)
        elif index in MoveData_obj.unused_offsets:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 1, 'Unknown', index)
        elif index in MoveData_obj.async_timer_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'Async Timer',
                           index)
        elif index in MoveData_obj.summon_projectile_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 4,
                           'Summon Projectile', index)
        elif index in MoveData_obj.POW_DMG_GRD_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 3,
                           'POW DMG GRD Location', index)
        elif index in MoveData_obj.ANG_DIR_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'ANG DIR location', index)
        elif index in MoveData_obj.horizontal_mobility_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'Horizontal Mobility', index)
        elif index in MoveData_obj.vertical_mobility_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'Vertical Mobility', index)
        elif index in MoveData_obj.GFX_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 5, 'GFX', index)
        elif index in MoveData_obj.SFX_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'SFX', index)
        elif index in MoveData_obj.animation_location:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'Animation',
                           index)
        elif index in MoveData_obj.pointers_01300000:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'pointer', index)
        elif index in MoveData_obj.pointers_01320000:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'pointer', index)
        elif index in MoveData_obj.pointers_01330000:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'pointer', index)
        elif index in MoveData_obj.pointers_01340000:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'pointer', index)
        elif index in MoveData_obj.pointers_013C0000:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'pointer', index)
        elif index in MoveData_obj.AF_flag_add:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'AF Flag Add',
                           index)
        elif index in MoveData_obj.AF_flag_remove:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'AF Flag Remove',
                           index)
        elif index in MoveData_obj.NF_flag_remove:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'NF Flag Remove',
                           index)
        elif index in MoveData_obj.KF_flag_add:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'KF Flag Add',
                           index)
        elif index in MoveData_obj.KF_flag_remove:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2, 'KF Flag Remove',
                           index)
        elif index in MoveData_obj.KF_flag_projectile:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'KF Flag Projectile', index)
        elif index in MoveData_obj.K2F_flag_remove:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'K2F Flag Remove', index)
        elif index in MoveData_obj.N2F_flag_remove:
            column_builder(column_data_offset, column_data_purpose, column_data_data, MoveData_obj, 2,
                           'N2F Flag Remove', index)

        index += 1
    column_data = [
        [sg.Column(column_data_offset), sg.Column(column_data_purpose), sg.Column(column_data_data)]]

    layout = [[sg.Button('Quit', key='Quit'), sg.Text('                      SEQ Kage')],
              [sg.Column(column_data, scrollable=True, vertical_scroll_only=True, size=(950, 700), key='column')]]
    window = sg.Window('SEQ Kage', layout, font='Courier 12', size=(1000, 800))
    # print(type(window['column1']))
    # window['column1'].Update(False)
    # window['column'].Update(column_data)
    # window.refresh()
    # print(MoveData_obj.data)
    return window


def display_MoveData_window(window, MoveData_Obj, SEQ_Object):
    while True:
        event, values = window.read()
        print(event, 'event')
        print(values)

        if event in ('Quit', None):
            if sg.PopupYesNo('Would you like to save?'):
                SEQ_Object.write_to_obj(MoveData_Obj)
            break

        else:
            window.close()
            line_movedata_window(MoveData_Obj, event)
            window = build_MoveData_window(MoveData_Obj)
    window.close()
    return


def line_movedata_window(MoveData_Obj, key):
    layout = [[sg.Text(
        'Would you like to Use custom editor for this line, insert before this line, delete, or edit this line?')],
        [sg.Radio('Custom Edit', group_id='radio'), sg.Radio('Insert', group_id='radio'),
         sg.Radio('Edit this line', group_id='radio'),
         sg.Radio('Delete', group_id='radio')],
        [sg.Button('Go')]]
    window = sg.Window('button', layout, font='Courier 12')
    event, values = window.read()
    window.close()
    print('closed window')
    if event == 'Go':
        if values[1]:
            insert_line_movedata(MoveData_Obj, key)
        elif values[3]:
            delete_line_movedata(MoveData_Obj, key)
        elif values[2]:
            edit_line_movedata(MoveData_Obj, key)
        elif values[0]:
            if key[3] in ['AF Flag', 'KF Flag', 'NF Flag', 'K2F Flag', 'N2F Flag', 'RF Flag']:
                flag_wrapper(MoveData_Obj, key)
            elif key[3] == 'Sync Timer':
                sync_timer_edit(MoveData_Obj, key)
            elif key[3] == 'Animation':
                animation_edit(MoveData_Obj, key)
            elif key[3] == 'Hitbox Location':
                hitbox_edit(MoveData_Obj, key)

    return


def edit_line_movedata(MoveData_Obj, key):
    print('in edit line movedata')
    current_value = MoveData_Obj.data[key[1]:key[1] + (key[2] * 4)]
    layout = [[sg.Text('Edit the line in hex')],
              [sg.InputText(hex(int.from_bytes(current_value, byteorder='big'))[2:])],
              [sg.Button('Go')]
              ]
    window = sg.Window('Insert Window', layout, font='Courier 12')
    event, values = window.read()
    if event == 'Go':
        if len(values[0].replace(' ', '')) % 8 == 0:
            given_input = int(values[0].replace(' ', ''), 16)
            MoveData_Obj.data = bytearray(MoveData_Obj.data)
            MoveData_Obj.data[key[1]:key[1] + (key[2] * 4)] = given_input.to_bytes(key[2] * 4, byteorder='big')

    window.close()
    return


def insert_line_movedata(MoveData_Obj, key):
    print('in insert line movedata')
    layout = [[sg.Text('Type the line in hex you would like to add')],
              [sg.InputText()],
              [sg.Button('Go')]
              ]
    window = sg.Window('Insert Window', layout, font='Courier 12')
    event, values = window.read()
    if event == 'Go':
        if len(values[0].replace(' ', '')) % 8 == 0:
            given_input = int(values[0].replace(' ', ''), 16)

            print((len(values[0].replace(' ', ''))))
            MoveData_Obj.data = MoveData_Obj.data[0:key[1]] + given_input.to_bytes(
                (len(values[0].replace(' ', ''))) // 2,
                byteorder='big') + MoveData_Obj.data[key[1]:]
            MoveData_Obj.update(MoveData_Obj.data)
        else:
            sg.Popup('That was not as word, bad')
    window.close()


def delete_line_movedata(MoveData_Obj, key):
    MoveData_Obj.data = MoveData_Obj.data[0:key[1]] + MoveData_Obj.data[key[1] + (key[2] * 4):]
    MoveData_Obj.update(MoveData_Obj.data)
    # MoveData_Obj.print()
