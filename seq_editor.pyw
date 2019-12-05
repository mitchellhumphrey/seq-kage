from characters import * 
import PySimpleGUI as sg
import os
import shutil


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

root_folder = ''
while(root_folder==''):
    root_folder = sg.PopupGetFolder('FPK unpacked root filepath', 'Please select the unpacked root FPK filepath')
    if(root_folder==''):
        sg.Popup("That's an empty file >_>")

#=====================building layout and window for character selection, since this will not change is it outside of main program loop =========
radio_table = []
for x in char_table:
    radio_table.append(sg.Radio(x.name,'sel'))

radio_layout = [[sg.Text('Select the Character you wish to edit')]]+[radio_table]+[[sg.Button('Select'),sg.Button('Quit')]]

window_radio = sg.Window('Character Select',radio_layout)

#==============================main program loop============================================================
break_flag = False
while True:
    counter = 0
    while True:
        #if(stop == True):
        #    break
        
        event2, values2 = window_radio.read()
        try:
            if event2 in (None,'Select'):
                print('should be going forward')
                counter+=1
                print(values2)
                if(counter>10):
                    sg.Popup('Ight imma head out')
                    quit()
                print(len(char_table))
                for x in range(len(char_table)):
                    print('x is ',x)
                    if(values2[x]==True):
                        index = x
                        break_flag = True
                        break
                if break_flag:
                    break
                '''
                if(values2[0]==True):
                    Character = naruto
                        
                    break
                elif(values2[1]==True):
                    Character = neji
                        
                    break'''
                
                    
            elif event2 in (None,"Quit"):
                if(sg.PopupYesNo('Would you like to quit?')=='Yes'):
                    break
                        
                    
        except TypeError:
            pass
                
            
            

    layout2 = [[sg.Text('The values')],
                    [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))],
                    [sg.InputText(Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].guard_offset))]

                    ]

    layout1 = [  [sg.Text('Ah yes, it\'s all coming together')],
                    [sg.Text(char_table[index].name+'\'s health value')],
                    [sg.Text(char_table[index].name+'\'s guard value')],
                    [sg.Button('Change It!'), sg.Button('Go Back')] ]
    print(char_table[index].name,char_table[index].seq_path,char_table[index].health_offset,Return_offset_value(root_folder+char_table[index].seq_path,char_table[index].health_offset))


                    
    layout = [[sg.Column(layout1),sg.Column(layout2,element_justification = 'right')]]

        # Create the Window
    window = sg.Window('Naruto health editor', layout)
        # Event Loop to process "events" and get the "values" of the inputs

    while True:
        event, values = window.read()
        if event in (None, 'Go Back'):        # if user closes window or clicks cancel
            if(sg.PopupYesNo('Would you like to go back?')=='Yes'):
                window.close()
                break
                
                
        else:  
            try:
                int(values[0])
                int(values[0])
                Edit_file(root_folder+char_table[index].seq_path,char_table[index].health_offset,int(values[0]))
                Edit_file(root_folder+char_table[index].seq_path,char_table[index].guard_offset,int(values[1]))
                window.close()
                break
                    
                        
            except ValueError:
                print('wrong type dummy')
                sg.Popup("you didn't just type numbers you silly goose")
                
                
                
            
        
        

window.close()