from __init__ import *
import sys
import time
import getopt


def main(default=''):
    while True:
        if debug:
            logging.basicConfig(filename=str(int(time.time())) + ' SEQ_Kage.log', filemode='w', level=logging.DEBUG)
        logging.info("Starting Main")
        # this is the main function loop, more things will be added to this layout eventully
        layout = [[sg.Text('Select the path to your SEQ')],
                  [sg.Input(default), sg.FileBrowse(file_types=(("SEQ Files", "*.seq"),))],
                  [sg.Text('Select your action ID you wish to Edit (In Hex)')],
                  [sg.Input()],
                  [sg.Button('Expand this SEQ'), sg.Spin(values=[i for i in range(1024)], initial_value=0)],
                  [sg.Ok()]]

        window = sg.Window('SEQ Kage', layout=layout, font='Courier 12')

        while True:
            event, values = window.read()
            default = values[0]
            if event == 'Ok':
                try:
                    int(values[1], 16)

                    SEQ = SEQObject(values[0])

                    # checking to see if SEQ is character SEQ
                    # if (SEQ.data[])
                    print(int.from_bytes(SEQ.data[0:4], 'big'))
                    if int.from_bytes(SEQ.data[0:4], 'big') != 0x11:
                        print("Not a Character SEQ")
                        sg.Popup("Not a Character SEQ")

                    else:

                        SEQ.update()
                        window.close()
                        MoveData_obj = build_MoveData(SEQ, int(values[1], 16))

                        window = build_MoveData_window(MoveData_obj)
                        display_MoveData_window(window, MoveData_obj, SEQ)
                        break

                except ValueError:
                    logging.info("Action ID value is not given as a hex number")
                    sg.Popup('Your Action ID is not in hex')
                    
            elif event == 'Expand this SEQ':
                logging.info("Calling SEQ Expansion")
                SEQ = SEQObject(values[0])
                SEQ.expand_seq_file(values[2])
                SEQ.write_to_file()
            else:
                return


if __name__ == '__main__':
    main(*sys.argv[1:2])
