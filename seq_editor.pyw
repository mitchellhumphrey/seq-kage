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
            window.close()
            return
        
        elif event in(None,'Access Specific Offset'):
            window.Close()
            Random_Access(root_folder+char_table[index].seq_path)
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
    
    temp_file.write(original_file.read(int(offset,16)))
    
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
    
    original_file.read(int(offset,16))    
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
                value = Return_offset_value(filepath,offset,access_length)
                layout2 = [[sg.Text('What would you like the value of offset ',str(offset),' and access length ',str(access_length),' to be?')],[sg.InputText(str(value))]]
                window2 = sg.Window('test2',layout2)
                window.Hide()
                while True:
                    #switched to popups here cause interpeter was throwing a fit and googling didn't help
                    try:
                        temp_value = sg.PopupGetText('enter your value as a decimal integer',default_text = str(value))
                        print(temp_value)
                        if(temp_value ==None):
                            window.UnHide()
                            window.close()
                            return
                        
                        int(temp_value)
                        Edit_file(filepath,offset,int(temp_value),access_length)
                        window.UnHide()
                        window.close()
                        return
                        
                    except TypeError:
                        sg.Popup("That's not decimal")
                        
                    
                
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
                    
    layout2 = [[sg.Text('The values')],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))],
               [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].guard_offset))]
              ]

    layout1 = [[sg.Text(random.choice(quips))],
               [sg.Text(char_table[index].name+'\'s health value')],
               [sg.Text(char_table[index].name+'\'s guard value')],
               [sg.Button('Change It!'), sg.Button('Go Back'),sg.Button('Access Specific Offset')] ]
    #yay for debugging statements, don't remove this unless you wanna type it again, which I don't
    #print(char_table[index].name,char_table[index].seq_path,char_table[index].health_offset,Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))


                    
    layout = [[sg.Column(layout1),sg.Column(layout2,element_justification = 'right')]]

        
    window = sg.Window('SEQ Kage', layout)
        
    Editor(window,index)
    
                
                
                
            
        
        

window.close()
