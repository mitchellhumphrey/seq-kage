from characters import * 
import PySimpleGUI as sg
import os
import shutil
import random

quips = ["Ahh yes, it's all coming together","Everything's coming up Millhouse"]

def Edit_Action_IDs(filepath):
    
    move_dict = {
        '8B':0x3B8,
        '6B':0x2B4,
        '5B':0x2B0,
        '4B':0x2B8,
        '2B':0x2BC}
    
    gen_layout = [[]]
    index,counter = 0,0
    for x in move_dict:
        gen_layout[index].append(sg.Button(x))
        counter += 1
        if counter % 4 == 0:
            index += 1
            gen_layout.append([])
    gen_layout.append([sg.Button('Go Back')])
    
    
    window = sg.Window('Edit Action IDs', gen_layout)
    
    while True:
        event, values = window.read()
        if event in (None,'Go Back'):
            window.close()
            return
        elif event in move_dict:
            move_offset = Return_offset_value(filepath,move_dict[event])
            window.close()
            break
        
    Flag_Edit(filepath,move_offset)




def Get_health_offset(filepath):
    offset = 0
    print(hex(Return_offset_value(filepath,'9730',8))[2:])
    counter = 0
    while True:
        value = hex(Return_offset_value(filepath,hex(offset),8))[2:]
        if offset % 10000 == 0 or counter == 9676:
            print(offset)
        #print(value)
        if value == '30300020908023f': #header to pointer for character health
            return Return_offset_value(filepath,offset+8,4)
        else:
            offset += 4
            counter += 1


def Flag_Edit(filepath, input_offset = 0):
    num_of_bytes = 56
    #print(data)
    while True:
        if input_offset != 0:
            break
        try:
            offset = sg.PopupGetText("Please put in hex")
            int(offset,16)
            break
        except ValueError:
            sg.Popup("Not a valid offset")
    
    if input_offset != 0:
        offset = input_offset
    
    print(filepath)
    print(offset)
    data = hex(Return_offset_value(filepath,offset,num_of_bytes))
    data = data[2:] #removes the 0x in front of data so you can work with it
    
    
    #splits up data into the flag sections
    index = -1
    buffer = 0
    split_data = []
    for elem in data:
        if buffer % 16 == 0:
            buffer = 0
            index += 1
            split_data.append('')
        split_data[index]+=(elem)
        buffer += 1
    print(split_data)
    
    for x in range(len(split_data)):
        if split_data[x][:8].upper()=='241A0000':
            print('AF Flags: Action state flags')
            print(split_data[x][8:])
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            
            AF_flags = []
            for z in range(32):
                AF_flags.append(False)
            
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    AF_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    AF_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    AF_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    AF_flags[28-(4*n)]=True
                    temp-=1
            
        
            
            layout = [[sg.Text('What AF flags do you want on this move? (Action state flags)')],
                      [sg.Checkbox('stand',default = AF_flags[0],tooltip='its a motherfucking test you biatch'),sg.Checkbox('forward',default = AF_flags[1]),sg.Checkbox('back',default = AF_flags[2]),sg.Checkbox('dash',default = AF_flags[3]),sg.Checkbox('sit',default = AF_flags[4]),sg.Checkbox('fuse',default = AF_flags[5]),sg.Checkbox('ukemi',default = AF_flags[6]),sg.Checkbox('kiri',default = AF_flags[7])],
                      [sg.Checkbox('spmdmg',default = AF_flags[8]),sg.Checkbox('slant',default = AF_flags[9]),sg.Checkbox('quick',default = AF_flags[10]),sg.Checkbox('float',default = AF_flags[11]),sg.Checkbox('jump',default = AF_flags[12]),sg.Checkbox('fall',default = AF_flags[13]),sg.Checkbox('small',default = AF_flags[14]),sg.Checkbox('damage',default = AF_flags[15])],
                      [sg.Checkbox('downu',default = AF_flags[16]),sg.Checkbox('downo',default = AF_flags[17]),sg.Checkbox('getup',default = AF_flags[18]),sg.Checkbox('turn',default = AF_flags[19]),sg.Checkbox('tdown',default = AF_flags[20]),sg.Checkbox('cantact',default = AF_flags[21]),sg.Checkbox('sdef',default = AF_flags[22]),sg.Checkbox('bdef',default = AF_flags[23])],
                      [sg.Checkbox('beast',default = AF_flags[24]),sg.Checkbox('uki',default = AF_flags[25]),sg.Checkbox('butt',default = AF_flags[26]),sg.Checkbox('ndown',default = AF_flags[27]),sg.Checkbox('def',default = AF_flags[28]),sg.Checkbox('tfail',default = AF_flags[29]),sg.Checkbox('throw',default = AF_flags[30]),sg.Checkbox('attack',default = AF_flags[31])],
                      [sg.Button('Done')]]
            window = sg.Window('AF Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        AF_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if AF_flags[0+(4*n)]==True:
                            temp += 1
                        if AF_flags[1+(4*n)]==True:
                            temp += 2
                        if AF_flags[2+(4*n)]==True:
                            temp += 4
                        if AF_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    AF_finished = ''.join(finished_bytes)
                    print(AF_finished)
                    split_data[x] = '241a0000'+AF_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
            
        if split_data[x][:8].upper()=='241A0900':
            print('NF Flags')
            print(split_data[x][8:])
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            NF_flags = []
            for z in range(32):
                NF_flags.append(False)
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    NF_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    NF_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    NF_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    NF_flags[28-(4*n)]=True
                    temp-=1
            
            layout = [[sg.Text("What NF flags do you want")],
                      [sg.Checkbox('kamae',default = NF_flags[0]),sg.Checkbox('disp',default = NF_flags[1]),sg.Checkbox('tdmg',default = NF_flags[2]),sg.Checkbox('jump2',default = NF_flags[3]),sg.Checkbox('leverdir',default = NF_flags[4]),sg.Checkbox('getup',default = NF_flags[5]),sg.Checkbox('hiteft',default = NF_flags[6]),sg.Checkbox('nfog',default = NF_flags[7])],
                      [sg.Checkbox('takeon',default = NF_flags[8]),sg.Checkbox('(blank)',default = NF_flags[9]),sg.Checkbox('bdrivesleep',default = NF_flags[10]),sg.Checkbox('jump',default = NF_flags[11]),sg.Checkbox('fall',default = NF_flags[12]),sg.Checkbox('jspd',default = NF_flags[13]),sg.Checkbox('shotdef',default = NF_flags[14]),sg.Checkbox('move',default = NF_flags[15])],
                      [sg.Checkbox('attack',default = NF_flags[16]),sg.Checkbox('button',default = NF_flags[17]),sg.Checkbox('combo',default = NF_flags[18]),sg.Checkbox('disp_n',default = NF_flags[19]),sg.Checkbox('kabehit',default = NF_flags[20]),sg.Checkbox('bodytouch',default = NF_flags[21]),sg.Checkbox('aguard',default = NF_flags[22]),sg.Checkbox('damage',default = NF_flags[23])],
                      [sg.Checkbox('guard',default = NF_flags[24]),sg.Checkbox('autodir',default = NF_flags[25]),sg.Checkbox('eneauto',default = NF_flags[26]),sg.Checkbox('njpturn',default = NF_flags[27]),sg.Checkbox('ringout',default = NF_flags[28]),sg.Checkbox('kabe',default = NF_flags[29]),sg.Checkbox('tdown',default = NF_flags[30]),sg.Checkbox('lever',default = NF_flags[31])],
                      [sg.Button('Done')]]
            
            
            
            
            
            window = sg.Window('NF Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        NF_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if NF_flags[0+(4*n)]==True:
                            temp += 1
                        if NF_flags[1+(4*n)]==True:
                            temp += 2
                        if NF_flags[2+(4*n)]==True:
                            temp += 4
                        if NF_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    NF_finished = ''.join(finished_bytes)
                    print(NF_finished)
                    split_data[x] = '241a0900'+NF_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
            
            
            
        if split_data[x][:8].upper()=='241A1200' or split_data[x][:8].upper()=='48040000':
            print('KF Flags')
            print(split_data[x][8:])
            
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            KF_flags = []
            for z in range(32):
                KF_flags.append(False)
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    KF_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    KF_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    KF_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    KF_flags[28-(4*n)]=True
                    temp-=1
            
            layout = [[sg.Text("What KF flags do you want")],
                      [sg.Checkbox('replay:No Effect',default = KF_flags[0]),sg.Checkbox('BDrive: Changes lighting, no sub or tech roll',default = KF_flags[1]),sg.Checkbox('Shot: ??',default = KF_flags[2]),sg.Checkbox('Pow_W: weak hit. affects blockstun and hitstun',default = KF_flags[3]),sg.Checkbox('Pow_M: medium hit',default = KF_flags[4]),sg.Checkbox('Pow_S: strong hit',default = KF_flags[5]),sg.Checkbox('Low: attack hits low, and can be evaded by float flag',default = KF_flags[6]),sg.Checkbox('Middle: attack hits middle',default = KF_flags[7])],
                      [sg.Checkbox('High',tooltip = 'attack hits high, and can be evaded by sit flag',default = KF_flags[8]),sg.Checkbox('Punch: attack is classified as a punch',default = KF_flags[9]),sg.Checkbox('Kick: attack is classified as a kick',default = KF_flags[10]),sg.Checkbox('Throw: attack is classified as a throw',default = KF_flags[11]),sg.Checkbox('Oiuchi: Hits later on OTG',default = KF_flags[12]),sg.Checkbox('Special: Builds no chakra',default = KF_flags[13]),sg.Checkbox('NoGuard: Unblockable',default = KF_flags[14]),sg.Checkbox('TDown: ??',default = KF_flags[15])],
                      [sg.Checkbox('SPTata: This is a large bounce',default = KF_flags[16]),sg.Checkbox('Break',default = KF_flags[17]),sg.Checkbox('Combo',default = KF_flags[18]),sg.Checkbox('Down',default = KF_flags[19]),sg.Checkbox('Yoro',default = KF_flags[20]),sg.Checkbox('Butt',default = KF_flags[21]),sg.Checkbox('Uki',default = KF_flags[22]),sg.Checkbox('Furi',default = KF_flags[23])],
                      [sg.Checkbox('Koro',default = KF_flags[24]),sg.Checkbox('Reach_L',default = KF_flags[25]),sg.Checkbox('Tata',default = KF_flags[26]),sg.Checkbox('NoSpeEp',default = KF_flags[27]),sg.Checkbox('Beast',default = KF_flags[28]),sg.Checkbox('Freeze',default = KF_flags[29]),sg.Checkbox('Cancel',default = KF_flags[30]),sg.Checkbox('AtkCan',default = KF_flags[31])],
                      [sg.Button('Done')]]
            
            
            
            
            
            window = sg.Window('KF Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        KF_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if KF_flags[0+(4*n)]==True:
                            temp += 1
                        if KF_flags[1+(4*n)]==True:
                            temp += 2
                        if KF_flags[2+(4*n)]==True:
                            temp += 4
                        if KF_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    KF_finished = ''.join(finished_bytes)
                    print(KF_finished)
                    split_data[x] = '241a1200'+KF_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
            
            
            
            
            
            
        if split_data[x][:8].upper()=='241A2D00':
            print('RF Flags')
            print(split_data[x][8:])
            
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            RF_flags = []
            for z in range(32):
                RF_flags.append(False)
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    RF_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    RF_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    RF_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    RF_flags[28-(4*n)]=True
                    temp-=1
            
            layout = [[sg.Text("What RF flags do you want")],
                      [sg.Checkbox('Color',default = RF_flags[0]),sg.Checkbox('Tyakurasub',default = RF_flags[1]),sg.Checkbox('Haziki',default = RF_flags[2]),sg.Checkbox('HazikiR',default = RF_flags[3]),sg.Checkbox('All Guard',default = RF_flags[4]),sg.Checkbox('Eftrev',default = RF_flags[5]),sg.Checkbox('TargetDira',default = RF_flags[6]),sg.Checkbox('GCancelChk',default = RF_flags[7])],
                      [sg.Checkbox('GCancelOk',default = RF_flags[8]),sg.Checkbox('GCancel',default = RF_flags[9]),sg.Checkbox('GaAttack',default = RF_flags[10]),sg.Checkbox('NKawarimi',default = RF_flags[11]),sg.Checkbox('AutoMotion',default = RF_flags[12]),sg.Checkbox('Event00',default = RF_flags[13]),sg.Checkbox('ShadowOff',default = RF_flags[14]),sg.Checkbox('NoBack',default = RF_flags[15])],
                      [sg.Checkbox('Intrude',default = RF_flags[16])],
                      [sg.Button('Done')]]
            
            
            
            
            
            window = sg.Window('RF Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        RF_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if RF_flags[0+(4*n)]==True:
                            temp += 1
                        if RF_flags[1+(4*n)]==True:
                            temp += 2
                        if RF_flags[2+(4*n)]==True:
                            temp += 4
                        if RF_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    RF_finished = ''.join(finished_bytes)
                    print(RF_finished)
                    split_data[x] = '241a2d00'+RF_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
        if split_data[x][:8].upper()=='241A4800':
            print('K2F Flags')
            print(split_data[x][8:])
            
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            K2F_flags = []
            for z in range(32):
                K2F_flags.append(False)
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    K2F_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    K2F_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    K2F_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    K2F_flags[28-(4*n)]=True
                    temp-=1
            
            layout = [[sg.Text("What K2F flags do you want")],
                      [sg.Checkbox('yoro2',default = K2F_flags[0]),sg.Checkbox('hiki',default = K2F_flags[1]),sg.Checkbox('hiki2',default = K2F_flags[2]),sg.Checkbox('mission',default = K2F_flags[3]),sg.Checkbox('natemi',default = K2F_flags[4]),sg.Checkbox('superarmor',default = K2F_flags[5]),sg.Checkbox('mato2',default = K2F_flags[6]),sg.Checkbox('atkallcan',default = K2F_flags[7])],
                      [sg.Checkbox('toji',default = K2F_flags[8]),sg.Checkbox('hasa',default = K2F_flags[9]),sg.Checkbox('shave',default = K2F_flags[10]),sg.Checkbox('nemu',default = K2F_flags[11]),sg.Checkbox('wing',default = K2F_flags[12]),sg.Checkbox('null',tooltip='Grounded only crumple (OTK 2X)',default = K2F_flags[13]),sg.Checkbox('null',default = K2F_flags[14])],
                      [sg.Button('Done')]]
            
            
            
            
            
            window = sg.Window('K2F Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        K2F_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if K2F_flags[0+(4*n)]==True:
                            temp += 1
                        if K2F_flags[1+(4*n)]==True:
                            temp += 2
                        if K2F_flags[2+(4*n)]==True:
                            temp += 4
                        if K2F_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    K2F_finished = ''.join(finished_bytes)
                    print(K2F_finished)
                    split_data[x] = '241a2d00'+K2F_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
            
            
            
        if split_data[x][:8].upper()=='241A5700':
            print('N2F Flags')
            print(split_data[x][8:])
            
            bytes = []
            for i in range(len(split_data[x][8:])):
                bytes.append(split_data[x][8:][i])
            print(bytes)
            
            N2F_flags = []
            for z in range(32):
                N2F_flags.append(False)
            #============================ assigning if boxes should be checked ===============================
            for n in range(len(bytes)):
                temp = int(bytes[n],16)
                print(temp)
                if temp >= 8:
                    N2F_flags[31-(4*n)]=True
                    temp-=8
                if temp >= 4:
                    N2F_flags[30-(4*n)]=True
                    temp-=4
                if temp >= 2:
                    N2F_flags[29-(4*n)]=True
                    temp-=2
                if temp>=1:
                    N2F_flags[28-(4*n)]=True
                    temp-=1
            
            layout = [[sg.Text("What N2F flags do you want")],
                      [sg.Checkbox('Ukemi',default = N2F_flags[0]),sg.Checkbox('Kawarimi',default = N2F_flags[1]),sg.Checkbox('Nagenuke',default = N2F_flags[2]),sg.Checkbox('Push',default = N2F_flags[3]),sg.Checkbox('Defeft',default = N2F_flags[4]),sg.Checkbox('Hitshock',default = N2F_flags[5]),sg.Checkbox('Defshock',default = N2F_flags[6]),sg.Checkbox('Gage',default = N2F_flags[7])],
                      [sg.Checkbox('Tyakura',default = N2F_flags[8]),sg.Checkbox('CameraOff',default = N2F_flags[9]),sg.Checkbox('CutOff',default = N2F_flags[10]),sg.Checkbox('N/A',default = N2F_flags[11]),sg.Checkbox('null',default = N2F_flags[12]),sg.Checkbox('null',default = N2F_flags[13]),sg.Checkbox('null',default = N2F_flags[14])],
                      [sg.Button('Done')]]
            
            
            
            
            
            window = sg.Window('N2F Flags', layout)
            while True:
                event, values = window.read()
                if event in (None,'Done'):
                    for n in range(len(values)):
                        N2F_flags[n] = values[n]
                    finished_bytes = []
                    for n in range(8):
                        temp = 0
                        if N2F_flags[0+(4*n)]==True:
                            temp += 1
                        if N2F_flags[1+(4*n)]==True:
                            temp += 2
                        if N2F_flags[2+(4*n)]==True:
                            temp += 4
                        if N2F_flags[3+(4*n)]==True:
                            temp += 8
                        temp = hex(temp)[2:]
                        finished_bytes.insert(0,temp)
                    print(finished_bytes)
                    N2F_finished = ''.join(finished_bytes)
                    print(N2F_finished)
                    split_data[x] = '241a2d00'+N2F_finished
                    print(split_data)
                    window.close()
                    break
            
            
            
            
            
            
            
            
            
            
            
        finished = ''.join(split_data)
        valuezzzz = int(finished,16)
        Edit_file(filepath,offset,valuezzzz,num_of_bytes)


def Editor(window,index):
    while True:
        
        event, values = window.read()
        if event in (None, 'Go Back'):        # if user closes window or clicks cancel
            window.close()
            return
        elif event in(None,"Flag Edit"):
            window.Close()
            Flag_Edit(root_folder+char_table[index].seq_path)
            event, values = window.read()
        elif event in(None,'Access Specific Offset'):
            window.Close()
            Random_Access(root_folder+char_table[index].seq_path)
            event, values = window.read()
        elif event in(None,'Edit predectected moves'):
            window.Close()
            Edit_Action_IDs(root_folder+char_table[index].seq_path)
            event, values = window.read()
        else:  
            try:
                int(values[0])
                int(values[0])
                Edit_file(root_folder+char_table[index].seq_path,char_table[index].health_offset,int(values[0]))
                Edit_file(root_folder+char_table[index].seq_path,char_table[index].guard_offset,int(values[1]))
                window.close()
                return
                    
                        
            except ValueError:
                sg.Popup("you didn't just type numbers you silly goose")


char_sel_window_shown = True

def Char_Index_select(list_of_chars,window):
    global char_sel_window_shown
    counter = 0
    while True:
        if char_sel_window_shown == False:
            window.UnHide()
        event, values = window.read()
        try:
            if event in (None,'Select'):
                print('should be going forward')
                counter+=1
                print(values)
                if(counter>10):
                    sg.Popup('Ight imma head out')
                    quit()
                print(len(char_table))
                for x in range(len(char_table)):
                    
                    if(values[x]==True):
                        index = x
                        window.Hide()
                        char_sel_window_shown = False
                        return index
                        
                             
                    
            elif event in (None,"Quit"):
                if(sg.PopupYesNo('Would you like to quit?')=='Yes'):
                    quit()
                        
                    
        except TypeError:
            pass
                



def Edit_file(filepath,offset,value,num_of_bytes = 4):
    "offset is hex value<--------------------"
    "value MUST be an integer that is num_of_bytes bytes or less"
    original_file = open(filepath,'rb')
    temp_file = open(filepath+'temp','wb+')
    
    try:
        offset_value = int(offset,16)
    except:
        offset_value = offset
    
    temp_file.write(original_file.read(offset_value))
    
    temp_file.write(value.to_bytes(num_of_bytes,'big'))
    original_file.read(num_of_bytes)
    temp_file.write(original_file.read())
    temp_file.close()
    original_file.close()
    os.remove(filepath)
    shutil.move(filepath+'temp',filepath)



def Return_offset_value(filepath,offset,length = 4):
    "offset is hex value<--------------------"
    original_file = open(filepath,'rb')
    try:
        original_file.read(int(offset,16))    
    except:
        print('whoops')
    
        original_file.read(offset)
    
    
    
    value = int.from_bytes(original_file.read(length),'big')
    original_file.close()
    return value


def Random_Access(filepath):

    text =  [[sg.Text('What offset do you wish to access?(in hex)')],
               [sg.Text('How many bytes would you like to see?')],
               [sg.Button('Enter'),sg.Button('Go Back')]
    ]
    input = [[sg.InputText()],
             [sg.InputText()]]

    layout = [[sg.Column(text),sg.Column(input)]]
    window = sg.Window('test',layout)
    while True:
        event,values = window.read()
        if event in (None, 'Go Back'):        # if user closes window or clicks cancel
            window.close()
            return
               
        if event in ('None','Enter'):
            try:
                int(values[0],16)
                
                offset = values[0]
                access_length = int(values[1])
                value = hex(Return_offset_value(filepath,offset,access_length))
                value = value[2:]
                layout2 = [[sg.Text('What would you like the value of offset ',str(offset),' and access length ',str(access_length),' to be?')],[sg.InputText(str(value))]]
                window2 = sg.Window('test2',layout2)
                window.Hide()
                while True:
                    #switched to popups here cause interpeter was throwing a fit and googling didn't help
                    try:
                        temp_value = sg.PopupGetText('enter your value as a hexadecimal integer',default_text = str(value))
                        print(temp_value)
                        if(temp_value ==None):
                            window.UnHide()
                            window.close()
                            return
                        
                        int(temp_value,16)
                        Edit_file(filepath,offset,int(temp_value,16),access_length)
                        window.UnHide()
                        window.close()
                        return
                        
                    except TypeError:
                        sg.Popup("That's not hexadecimal")
                        
                    
                
            except TypeError:
                sg.Popup("Those aren't valid inputs")
    



sg.change_look_and_feel('Default')

#===============================grabbing root folder, will not proceed until you have a path selected=================================

root_folder = '@'
while(root_folder=='@'or root_folder==''):
    root_folder = sg.PopupGetFolder('FPK unpacked root filepath', 'Please select the unpacked root FPK filepath')
    if(root_folder=='@'or root_folder==''):
        sg.Popup("That's an empty file >_>")
        quit()
    print(root_folder)

#=====================building layout and window for character selection, since this will not change is it outside of main program loop =========
radio_table =[]
radio_table2=[]
radio_table3=[]
radio_table4=[]
for x in range(len(char_table)):
    if(x<10):
        radio_table.append(sg.Radio(char_table[x].name,'sel'))
    elif(x<20):
        radio_table2.append(sg.Radio(char_table[x].name,'sel'))
    elif(x<28):
        radio_table3.append(sg.Radio(char_table[x].name,'sel'))
    else:
        radio_table4.append(sg.Radio(char_table[x].name,'sel'))
final_radio_table = [radio_table,radio_table2,radio_table3,radio_table4]

radio_layout = [[sg.Text('Select the Character you wish to edit')]]+final_radio_table+[[sg.Button('Select'),sg.Button('Quit')]]

window_radio = sg.Window('Character Select',radio_layout)

#==============================main program loop============================================================
break_flag = False
print('aaaaaa')


while True:
    
    index = Char_Index_select(char_table,window_radio)
    health_offset = Get_health_offset(root_folder+char_table[index].seq_path)  
    print(hex(health_offset))    
    layout2 = [[sg.Text('The values')],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,hex(health_offset)))],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,hex(health_offset+4)))]
              ]

    layout1 = [[sg.Text(random.choice(quips))],
               [sg.Text(char_table[index].name+'\'s health value')],
               [sg.Text(char_table[index].name+'\'s guard value')],
               [sg.Button('Change It!'), sg.Button('Go Back'),sg.Button('Access Specific Offset'),sg.Button('Flag Edit'),sg.Button('Edit predectected moves')] ]
    #yay for debugging statements, don't remove this unless you wanna type it again, which I don't
    #print(char_table[index].name,char_table[index].seq_path,char_table[index].health_offset,Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))


                    
    layout = [[sg.Column(layout1),sg.Column(layout2,element_justification = 'right')]]

        
    window = sg.Window('SEQ Kage', layout)
        
    Editor(window,index)
    
                
                
                
            
        
        

window.close()
