from __init__ import *
import PySimpleGUI as sg


def hitbox_edit(MoveData_obj,key):
    bone = int.from_bytes(MoveData_obj.data[key[1] + 4:key[1] + 6], 'big')
    size = int.from_bytes(MoveData_obj.data[key[1] + 6:key[1] + 8], 'big')
    print(hex(bone), 'bone')
    print(hex(size), 'size')
    layout = [[sg.Text('What bone ID do you want to use?')],
              [sg.InputText(hex(bone)[2:])],
              [sg.Text('What size do you want this hitbox to be?')],
              [sg.InputText(hex(size)[2:])],
              [sg.Button('Save')]]
    window_hitbox = sg.Window('Hitbox Edit', layout=layout, font='Courier 12')
    while True:
        event, values = window_hitbox.read()
        if event in (None, 'Save'):
            try:
                int(values[0], 16)
                int(values[1], 16)
                break
            except ValueError:
                sg.Popup('Not in Hexadecimal')
                pass
    window_hitbox.close()
    try:
        MoveData_obj.data[key[1] + 4:key[1] + 6] = int(values[0], 16).to_bytes(2, 'big')
        MoveData_obj.data[key[1] + 6:key[1] + 8] = int(values[1], 16).to_bytes(2, 'big')
    except TypeError:
        pass


def animation_edit(MoveData_obj, key):
    gnta_file = int.from_bytes(MoveData_obj.data[key[1] + 4:key[1] + 8], 'big')
    layout = [[sg.Text('What animation ID do you want to use?')],
              [sg.InputText(hex(gnta_file)[2:])],
              [sg.Button('Save')]]
    window_animation = sg.Window('Animation Edit', layout=layout, font='Courier 12')
    while True:
        event, values = window_animation.read()
        if event in (None, 'Save'):
            try:
                int(values[0], 16)
                break
            except ValueError:
                sg.Popup('Not in Hexadecimal')
                pass

    window_animation.close()
    try:
        MoveData_obj.data[key[1] + 4:key[1] + 8] = int(values[0], 16).to_bytes(4, 'big')
    except TypeError:
        pass


def sync_timer_edit(MoveData_obj, key):
    # key=('offset', index * 4, amount_of_words, purpose)
    sync_timer_amount = int.from_bytes(MoveData_obj.data[key[1] + 4:key[1] + 8], 'big')
    layout = [[sg.Text("Amount of frames")],
              [sg.Spin([i for i in range(256)], initial_value=sync_timer_amount),
               sg.Text("Amount of frames for sync timer")],
              [sg.Button("Save")]]
    window_sync = sg.Window('Sync timer edit', layout=layout, font='Courier 12')
    while True:
        print('in sync timer #2')
        event, values = window_sync.read()
        if event in (None, 'Save'):
            break
    window_sync.close()
    print('closed window_sync')
    try:
        MoveData_obj.data[key[1] + 4:key[1] + 8] = int(values[0]).to_bytes(4, 'big')
    except TypeError:
        pass


def flag_wrapper(MoveData_obj, key):
    """
    Preps a MoveData obj to be edited by flag edit function,also edits the MoveData obj
    :param MoveData_obj: MoveData_obj to be edited
    :param key: key originally built from column_builder(), in the format of ('offset', relative start, amount of bytes,
    purpose of flag)
    :return: None
    """
    MoveData_obj.data = bytearray(MoveData_obj.data)
    new_value = flag_edit(int.from_bytes(MoveData_obj.data[key[1] + 4:key[1] + 8], 'big'), key[3])
    MoveData_obj.data[key[1] + 4:key[1] + 8] = new_value.to_bytes(4, 'big')


def flag_edit(flag_configuration, flag_type):
    """
    :param flag_configuration: an int that is the settings of flags for AF
    :return: int that is the new flag configuration
    """
    byte_value = hex(flag_configuration)[2:].rjust(8, '0')
    print(byte_value)
    flags = []
    for z in range(32):
        flags.append(False)
    for n in range(8):
        temp = int(byte_value[n], 16)
        print(temp)
        if temp >= 8:
            flags[31 - (4 * n)] = True
            temp -= 8
        if temp >= 4:
            flags[30 - (4 * n)] = True
            temp -= 4
        if temp >= 2:
            flags[29 - (4 * n)] = True
            temp -= 2
        if temp >= 1:
            flags[28 - (4 * n)] = True
            temp -= 1
    layout = []
    if flag_type == 'AF Flag':
        layout = af_layout(flags)
    elif flag_type == 'NF Flag':
        layout = nf_layout(flags)
    elif flag_type == 'KF Flag':
        layout = kf_layout(flags)
    elif flag_type == 'RF Flag':
        layout = rf_layout(flags)
    elif flag_type == 'K2F Flag':
        layout = k2f_layout(flags)
    elif flag_type == 'N2F Flag':
        layout = n2f_layout(flags)
    else:
        layout = []
    print(layout, 'is layout')
    window = sg.Window('Flag Edit', layout, font='Courier 12')
    event, values = window.read()
    if event == 'Done':
        for n in range(len(values)):
            flags[n] = values[n]
        finished_bytes = []
        for n in range(8):
            temp = 0
            if flags[0 + (4 * n)]:
                temp += 1
            if flags[1 + (4 * n)]:
                temp += 2
            if flags[2 + (4 * n)]:
                temp += 4
            if flags[3 + (4 * n)]:
                temp += 8
            temp = hex(temp)[2:]
            finished_bytes.insert(0, temp)
    window.close()
    print(finished_bytes, 'finished bytes')
    af_finished = ''.join(finished_bytes)
    print(af_finished)
    return int(af_finished, 16)


def af_layout(af_flags):
    layout = [[sg.Text('What AF flags do you want on this move? (Action state flags)')],
              [sg.Checkbox('stand', default=af_flags[0], tooltip='its a motherfucking test you biatch'),
               sg.Checkbox('forward', default=af_flags[1]), sg.Checkbox('back', default=af_flags[2]),
               sg.Checkbox('dash', default=af_flags[3]), sg.Checkbox('sit', default=af_flags[4]),
               sg.Checkbox('fuse', default=af_flags[5]), sg.Checkbox('ukemi', default=af_flags[6]),
               sg.Checkbox('kiri', default=af_flags[7])],
              [sg.Checkbox('spmdmg', default=af_flags[8]), sg.Checkbox('slant', default=af_flags[9]),
               sg.Checkbox('quick', default=af_flags[10]), sg.Checkbox('float', default=af_flags[11]),
               sg.Checkbox('jump', default=af_flags[12]), sg.Checkbox('fall', default=af_flags[13]),
               sg.Checkbox('small', default=af_flags[14]), sg.Checkbox('damage', default=af_flags[15])],
              [sg.Checkbox('downu', default=af_flags[16]), sg.Checkbox('downo', default=af_flags[17]),
               sg.Checkbox('getup', default=af_flags[18]), sg.Checkbox('turn', default=af_flags[19]),
               sg.Checkbox('tdown', default=af_flags[20]), sg.Checkbox('cantact', default=af_flags[21]),
               sg.Checkbox('sdef', default=af_flags[22]), sg.Checkbox('bdef', default=af_flags[23])],
              [sg.Checkbox('beast', default=af_flags[24]), sg.Checkbox('uki', default=af_flags[25]),
               sg.Checkbox('butt', default=af_flags[26]), sg.Checkbox('ndown', default=af_flags[27]),
               sg.Checkbox('def', default=af_flags[28]), sg.Checkbox('tfail', default=af_flags[29]),
               sg.Checkbox('throw', default=af_flags[30]), sg.Checkbox('attack', default=af_flags[31])],
              [sg.Button('Done')]]
    return layout


def nf_layout(NF_flags):
    return [[sg.Text("What NF flags do you want")],
            [sg.Checkbox('kamae', default=NF_flags[0]), sg.Checkbox('disp', default=NF_flags[1]),
             sg.Checkbox('tdmg', default=NF_flags[2]), sg.Checkbox('jump2', default=NF_flags[3]),
             sg.Checkbox('leverdir', default=NF_flags[4]), sg.Checkbox('getup', default=NF_flags[5]),
             sg.Checkbox('hiteft', default=NF_flags[6]), sg.Checkbox('nfog', default=NF_flags[7])],
            [sg.Checkbox('takeon', default=NF_flags[8]), sg.Checkbox('(blank)', default=NF_flags[9]),
             sg.Checkbox('bdrivesleep', default=NF_flags[10]), sg.Checkbox('jump', default=NF_flags[11]),
             sg.Checkbox('fall', default=NF_flags[12]), sg.Checkbox('jspd', default=NF_flags[13]),
             sg.Checkbox('shotdef', default=NF_flags[14]), sg.Checkbox('move', default=NF_flags[15])],
            [sg.Checkbox('attack', default=NF_flags[16]), sg.Checkbox('button', default=NF_flags[17]),
             sg.Checkbox('combo', default=NF_flags[18]), sg.Checkbox('disp_n', default=NF_flags[19]),
             sg.Checkbox('kabehit', default=NF_flags[20]), sg.Checkbox('bodytouch', default=NF_flags[21]),
             sg.Checkbox('aguard', default=NF_flags[22]), sg.Checkbox('damage', default=NF_flags[23])],
            [sg.Checkbox('guard', default=NF_flags[24]), sg.Checkbox('autodir', default=NF_flags[25]),
             sg.Checkbox('eneauto', default=NF_flags[26]), sg.Checkbox('njpturn', default=NF_flags[27]),
             sg.Checkbox('ringout', default=NF_flags[28]), sg.Checkbox('kabe', default=NF_flags[29]),
             sg.Checkbox('tdown', default=NF_flags[30]), sg.Checkbox('lever', default=NF_flags[31])],
            [sg.Button('Done')]]


def kf_layout(KF_flags):
    return [[sg.Text("What KF flags do you want"), sg.Text('Has tooltip')],
            [sg.Checkbox('replay', tooltip='No Effect', default=KF_flags[0]),
             sg.Checkbox('BDrive', tooltip='Changes lighting, no sub or tech roll', default=KF_flags[1]),
             sg.Checkbox('Shot', tooltip='??', default=KF_flags[2]),
             sg.Checkbox('Pow_W', tooltip='weak hit. affects blockstun and hitstun', default=KF_flags[3]),
             sg.Checkbox('Pow_M', tooltip='medium hit', default=KF_flags[4]),
             sg.Checkbox('Pow_S', tooltip=': strong hit', default=KF_flags[5]),
             sg.Checkbox('Low', tooltip='attack hits low, and can be evaded by float flag', default=KF_flags[6]),
             sg.Checkbox('Middle', tooltip=': attack hits middle', default=KF_flags[7])],
            [sg.Checkbox('High', tooltip='attack hits high, and can be evaded by sit flag', default=KF_flags[8]),
             sg.Checkbox('Punch', tooltip=': attack is classified as a punch', default=KF_flags[9]),
             sg.Checkbox('Kick', tooltip=': attack is classified as a kick', default=KF_flags[10]),
             sg.Checkbox('Throw', tooltip=': attack is classified as a throw', default=KF_flags[11]),
             sg.Checkbox('Oiuchi', tooltip=': Hits later on OTG', default=KF_flags[12]),
             sg.Checkbox('Special', tooltip=': Builds no chakra', default=KF_flags[13]),
             sg.Checkbox('NoGuard', tooltip=': Unblockable', default=KF_flags[14]),
             sg.Checkbox('TDown', tooltip='Lets you get thrown', default=KF_flags[15])],
            [sg.Checkbox('SPTata', tooltip='This is a large bounce', default=KF_flags[16]),
             sg.Checkbox('Break', default=KF_flags[17]), sg.Checkbox('Combo', default=KF_flags[18]),
             sg.Checkbox('Down', default=KF_flags[19]), sg.Checkbox('Yoro', default=KF_flags[20]),
             sg.Checkbox('Butt', default=KF_flags[21]), sg.Checkbox('Uki', default=KF_flags[22]),
             sg.Checkbox('Furi', default=KF_flags[23])],
            [sg.Checkbox('Koro', default=KF_flags[24]), sg.Checkbox('Reach_L', default=KF_flags[25]),
             sg.Checkbox('Tata', default=KF_flags[26]), sg.Checkbox('NoSpeEp', default=KF_flags[27]),
             sg.Checkbox('Beast', default=KF_flags[28]), sg.Checkbox('Freeze', default=KF_flags[29]),
             sg.Checkbox('Cancel', default=KF_flags[30]), sg.Checkbox('AtkCan', default=KF_flags[31])],
            [sg.Button('Done')]]


def rf_layout(RF_flags):
    return [[sg.Text("What RF flags do you want")],
            [sg.Checkbox('Color', default=RF_flags[0]), sg.Checkbox('Tyakurasub', default=RF_flags[1]),
             sg.Checkbox('Haziki', default=RF_flags[2]), sg.Checkbox('HazikiR', default=RF_flags[3]),
             sg.Checkbox('All Guard', default=RF_flags[4]), sg.Checkbox('Eftrev', default=RF_flags[5]),
             sg.Checkbox('TargetDira', default=RF_flags[6]), sg.Checkbox('GCancelChk', default=RF_flags[7])],
            [sg.Checkbox('GCancelOk', default=RF_flags[8]), sg.Checkbox('GCancel', default=RF_flags[9]),
             sg.Checkbox('GaAttack', default=RF_flags[10]), sg.Checkbox('NKawarimi', default=RF_flags[11]),
             sg.Checkbox('AutoMotion', default=RF_flags[12]), sg.Checkbox('Event00', default=RF_flags[13]),
             sg.Checkbox('ShadowOff', default=RF_flags[14]), sg.Checkbox('NoBack', default=RF_flags[15])],
            [sg.Checkbox('Intrude', default=RF_flags[16])],
            [sg.Button('Done')]]


def k2f_layout(K2F_flags):
    return [[sg.Text("What K2F flags do you want")],
            [sg.Checkbox('yoro2', default=K2F_flags[0]), sg.Checkbox('hiki', default=K2F_flags[1]),
             sg.Checkbox('hiki2', default=K2F_flags[2]), sg.Checkbox('mission', default=K2F_flags[3]),
             sg.Checkbox('natemi', default=K2F_flags[4]), sg.Checkbox('superarmor', default=K2F_flags[5]),
             sg.Checkbox('mato2', default=K2F_flags[6]), sg.Checkbox('atkallcan', default=K2F_flags[7])],
            [sg.Checkbox('toji', default=K2F_flags[8]), sg.Checkbox('hasa', default=K2F_flags[9]),
             sg.Checkbox('shave', default=K2F_flags[10]), sg.Checkbox('nemu', default=K2F_flags[11]),
             sg.Checkbox('wing', default=K2F_flags[12]),
             sg.Checkbox('null', tooltip='Grounded only crumple (OTK 2X)', default=K2F_flags[13]),
             sg.Checkbox('null', default=K2F_flags[14])],
            [sg.Button('Done')]]


def n2f_layout(N2F_flags):
    return [[sg.Text("What N2F flags do you want")],
            [sg.Checkbox('Ukemi', default=N2F_flags[0]), sg.Checkbox('Kawarimi', default=N2F_flags[1]),
             sg.Checkbox('Nagenuke', default=N2F_flags[2]), sg.Checkbox('Push', default=N2F_flags[3]),
             sg.Checkbox('Defeft', default=N2F_flags[4]), sg.Checkbox('Hitshock', default=N2F_flags[5]),
             sg.Checkbox('Defshock', default=N2F_flags[6]), sg.Checkbox('Gage', default=N2F_flags[7])],
            [sg.Checkbox('Tyakura', default=N2F_flags[8]), sg.Checkbox('CameraOff', default=N2F_flags[9]),
             sg.Checkbox('CutOff', default=N2F_flags[10]), sg.Checkbox('N/A', default=N2F_flags[11]),
             sg.Checkbox('null', default=N2F_flags[12]), sg.Checkbox('null', default=N2F_flags[13]),
             sg.Checkbox('null', default=N2F_flags[14])],
            [sg.Button('Done')]]
