import os
import __init__ as other


class SEQObject:
    def __init__(self, filepath):
        """
        :param filepath: the filepath to the SEQ that will be constructed as a class
        """
        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.data = other.open_file_object(filepath)
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
        self.filesize = os.path.getsize(self.filepath)
        self.data = other.open_file_object(self.filepath)
        self.action_id_table = self.get_action_id_table()
        self.health_offset = self.find_health_offset()
        self.guard_offset = self.health_offset + 4

    def write_to_file(self):
        other.write_file_object(self.filepath, self.data)
        self.update()

    def find_health_offset(self):
        counter = 0
        while int.from_bytes(self.data[counter:counter + 8], 'big') != int('30300020908023f', 16):
            counter += 4
        counter += 8
        pointer = int.from_bytes(self.data[counter:counter + 4], 'big')
        return pointer
