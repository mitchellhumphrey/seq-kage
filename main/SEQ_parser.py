import os
from __init__ import *


class SEQObject:
    def __init__(self, filepath):
        """
        :param filepath: the filepath to the SEQ that will be constructed as a class
        """
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.data = open_file_object(filepath)
        self.data = bytearray(self.data)
        self.action_id_table = self.get_action_id_table()
        self.health_offset = self.find_health_offset()
        self.guard_offset = self.health_offset + 4

    def get_action_id_table(self):
        """
        :param self: an SEQObject
        :return:
        """
        action_ids = []
        for x in range(608):
            stuff = self.data[int('30', 16) + (4 * x):int('34', 16) + (4 * x)]
            # reads bytes [30,34) and then adds 4 to each

            stuff = int.from_bytes(stuff, 'big')
            action_ids.append(stuff)
        return action_ids

    def update(self):
        write_file_object(self.filepath, self.data)
        self.filesize = os.path.getsize(self.filepath)
        self.data = open_file_object(self.filepath)
        self.action_id_table = self.get_action_id_table()
        self.health_offset = self.find_health_offset()
        self.guard_offset = self.health_offset + 4

    def write_to_file(self):
        write_file_object(self.filepath, self.data)
        self.update()

    def find_health_offset(self):
        counter = 0
        while int.from_bytes(self.data[counter:counter + 8], 'big') != int('30300020908023f', 16):
            counter += 4
        counter += 8
        pointer = int.from_bytes(self.data[counter:counter + 4], 'big')
        return pointer

    def data_range(self, start, end):
        return self.data[start:end]

    def expand_seq_file(self, expansion_length):
        print('expand function')
        # ported from original SEQ Kage
        self.data = bytearray(self.data)
        start_of_last_function = int.from_bytes(self.data[0x14:0x18], byteorder='big')
        # self.data[0x14:0x18] = (int.from_bytes(self.data[0x14:0x18], 'big') + (expansion_length * 4)).to_bytes(4,byteorder='big')
        print(start_of_last_function, 'start of last function', hex(start_of_last_function))
        pointer_to_1000s = int.from_bytes(self.data[start_of_last_function + 4:start_of_last_function + 8], 'big')
        print(pointer_to_1000s, 'pointer to 1000s', hex(pointer_to_1000s))
        print('start = ')
        self.data[pointer_to_1000s + 0x30:pointer_to_1000s + 0x34] = (
                int.from_bytes(self.data[pointer_to_1000s + 0x30:pointer_to_1000s + 0x34],
                               'big') + expansion_length * 4).to_bytes(4, 'big')

        index = 1
        while True:  # this loop fixes pointers, SEQ Expanision is next thing
            temp_data = self.data[index * 4:index * 4 + 4]
            last_data = self.data[(index - 1) * 4:(index - 1) * 4 + 4]

            if index * 4 > len(self.data):
                break
            value = int.from_bytes(temp_data, 'big')
            last_value = int.from_bytes(last_data, 'big')
            if not 0x241A0000 <= last_value <= 0x241AFFFF:
                if value in [i for i in range(0x01300000, 0x013FFFFF, 0x10000)]:  #
                    index += 1
                    temp_data = self.data[index * 4:index * 4 + 4]
                    last_data = self.data[(index - 1) * 4:(index - 1) * 4 + 4]
                    value = int.from_bytes(temp_data, 'big')
                    if value >= start_of_last_function:
                        self.data[index * 4:index * 4 + 4] = (value + (expansion_length * 4)).to_bytes(4, 'big')
            index += 1
        self.data[0x14:0x18] = (start_of_last_function + expansion_length * 4).to_bytes(4, 'big')

        print(len(self.data))
        bytes_added = 0xCCCCCCCC.to_bytes(4, byteorder='big')
        self.data = self.data[0:start_of_last_function] + (bytes_added * expansion_length) + self.data[
                                                                                             start_of_last_function:]

        print(len(self.data))
        print('updated SEQ Object', start_of_last_function)
        return start_of_last_function

    def pointer_fixer_for_range(self, expansion_length, start, stop, old_reference):
        index = 0
        while True:
            temp_data = self.data[(index * 4) + start:index * 4 + 4 + start]
            last_data = self.data[((index - 1) * 4) + start:(index - 1) * 4 + 4 + start]

            if index * 4 > (stop - start):
                break
            value = int.from_bytes(temp_data, 'big')
            last_value = int.from_bytes(last_data, 'big')
            if not 0x241A0000 <= last_value <= 0x241AFFFF:
                if value in [0x01320000, 0x01330000, 0x01340000, 0x01360000, 0x013C0000]:  # 0x01300000, 0x01310000,
                    index += 1
                    temp_data = self.data[(index * 4) + start:index * 4 + 4 + start]
                    last_data = self.data[((index - 1) * 4) + start:(index - 1) * 4 + 4 + start]
                    value = int.from_bytes(temp_data, 'big')
                    if value >= old_reference:
                        self.data[index * 4:index * 4 + 4] = (value + (expansion_length * 4)).to_bytes(4, 'big')
            index += 1

    def write_to_obj(self, MoveData_Obj):
        self.data = bytearray(self.data)
        if MoveData_Obj.starting_length < MoveData_Obj.length:
            new_start_point = self.expand_seq_file(MoveData_Obj.word_length + 0x10)

            self.data[new_start_point + 0x8:new_start_point + 0x8 + MoveData_Obj.length] = MoveData_Obj.data
            self.action_id_table[MoveData_Obj.starting_action_id] = new_start_point + 0x8
            self.pointer_fixer_for_range(new_start_point, new_start_point + 0x8,
                                         new_start_point + 0x8 + MoveData_Obj.length,
                                         new_start_point - MoveData_Obj.length)

        elif MoveData_Obj.starting_length > MoveData_Obj.length:
            og_start = self.action_id_table[MoveData_Obj.starting_action_id]
            self.data[og_start:og_start + MoveData_Obj.length] = MoveData_Obj.data
            amount_removed = len(self.data[og_start+MoveData_Obj.length:og_start+MoveData_Obj.starting_length])
            self.data[og_start + MoveData_Obj.length:og_start + MoveData_Obj.starting_length] = amount_removed * (0xCC).to_bytes(1,'big')
        else:
            self.data[self.action_id_table[MoveData_Obj.starting_action_id]:self.action_id_table[
                                                                                MoveData_Obj.starting_action_id] + MoveData_Obj.length] = MoveData_Obj.data
        self.write_action_id_table_to_obj()
        write_file_object(self.filepath, self.data)

    def write_action_id_table_to_obj(self):
        for x in range(608):
            self.data[0x30 + (4 * x):0x34 + (4 * x)] = self.action_id_table[x].to_bytes(4, 'big')
