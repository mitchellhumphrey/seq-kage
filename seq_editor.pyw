from characters import * 
import PySimpleGUI as sg
import os
import shutil
import random

quips = ["Ahh yes, it's all coming together","Everything's coming up Millhouse"]


def Editor(window,index):
    while True:
        event, values = window.read()
        if event in (None, 'Go Back'):        # if user closes window or clicks cancel
            if(sg.PopupYesNo('Would you like to go back?')=='Yes'):
                window.close()
                return
                
                
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

def Char_Index_select(list_of_chars,window):
    counter = 0
    while True:
        
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
                        #window.close()
                        return index
                        
                             
                    
            elif event in (None,"Quit"):
                if(sg.PopupYesNo('Would you like to quit?')=='Yes'):
                    quit()
                        
                    
        except TypeError:
            pass
                


def Edit_file(filepath,offset,value):
    "offset is hex value<--------------------"
    "value MUST be an integer that is 4 bytes or less"
    original_file = open(filepath,'rb')
    temp_file = open(filepath+'temp','wb+')
    
    temp_file.write(original_file.read(int(offset,16)))
    
    temp_file.write(value.to_bytes(4,'big'))
    original_file.read(4)
    temp_file.write(original_file.read())
    temp_file.close()
    original_file.close()
    os.remove(filepath)
    shutil.move(filepath+'temp',filepath)



def Return_offset_value(filepath,offset):
    "offset is hex value<--------------------"
    original_file = open(filepath,'rb')
    
    original_file.read(int(offset,16))    
    value = int.from_bytes(original_file.read(4),'big')
    original_file.close()
    return value




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



while True:
    
    index = Char_Index_select(char_table,window_radio)
                    
    layout2 = [[sg.Text('The values')],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].guard_offset))]
              ]

    layout1 = [[sg.Text(random.choice(quips))],
               [sg.Text(char_table[index].name+'\'s health value')],
               [sg.Text(char_table[index].name+'\'s guard value')],
               [sg.Button('Change It!'), sg.Button('Go Back')] ]
    #yay for debugging statements, don't remove this unless you wanna type it again, which I don't
    #print(char_table[index].name,char_table[index].seq_path,char_table[index].health_offset,Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))


                    
    layout = [[sg.Column(layout1),sg.Column(layout2,element_justification = 'right')]]

        # Create the Window
    window = sg.Window('SEQ Kage', layout)
        # Event Loop to process "events" and get the "values" of the inputs
    
    Editor(window,index)
    
                
                
                
            
        
        

window.close()
