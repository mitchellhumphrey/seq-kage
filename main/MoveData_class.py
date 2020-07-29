import logging

class MoveData:
    def __init__(self, input_data, action_id):
        self.starting_length = len(input_data)
        self.data = input_data
        self.data = bytearray(self.data)
        self.hitbox_location = []
        self.hitbox_apperence_location = []
        self.sync_timer_location = []
        self.async_timer_location = []
        self.summon_projectile_location = []
        self.POW_DMG_GRD_location = []
        self.ANG_DIR_location = []
        self.horizontal_mobility_location = []
        self.vertical_mobility_location = []
        self.GFX_location = []
        self.SFX_location = []
        self.animation_location = []
        self.pointers_01300000 = []
        self.pointers_01320000 = []
        self.pointers_01330000 = []
        self.pointers_01340000 = []
        self.pointers_013C0000 = []
        self.AF_flag = []
        self.NF_flag = []
        self.KF_flag = []
        self.RF_flag = []
        self.K2F_flag = []
        self.N2F_flag = []
        self.EF_flag = []
        self.unused_offsets = []
        self.AF_flag_add = []
        self.AF_flag_remove = []
        self.NF_flag_remove = []
        self.KF_flag_add = []
        self.KF_flag_remove = []
        self.KF_flag_projectile = []
        self.K2F_flag_remove = []
        self.N2F_flag_remove = []
        self.length = 0
        self.word_length = 0
        self.starting_action_id = action_id
        self.update(self.data)

    def update(self, data):
        self.clear()
        index = 0
        self.length = len(data)
        self.word_length = len(data) // 4
        while self.length > index * 4:
            if data[index * 4:(index * 4) + 4] == 0x01300000:
                self.pointers_01300000.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x01320000:
                self.pointers_01320000.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x01330000:
                self.pointers_01330000.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x01340000:
                self.pointers_01340000.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x013C0000:
                self.pointers_013C0000.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A0000:
                self.AF_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A0900:
                self.NF_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A0700:
                self.NF_flag_remove.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A1200:
                self.KF_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A2D00:
                self.RF_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A4800:
                self.K2F_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x241A5700:
                self.N2F_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x24190100:
                self.EF_flag.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x47000026:
                self.summon_projectile_location.append(index)
                index += 4
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x2011263F:
                self.sync_timer_location.append(index)
                index += 3
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x24150A00:
                self.async_timer_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x21040026:
                self.hitbox_location.append(index)
                index += 3
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x21050026:
                self.POW_DMG_GRD_location.append(index)
                index += 3
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x21060026:
                self.ANG_DIR_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x21070026:
                self.hitbox_apperence_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x2414010B:
                self.horizontal_mobility_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x2414020B:
                self.vertical_mobility_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x2A002626:
                self.GFX_location.append(index)
                index += 5
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') in [i for i in
                                                                            range(0x24170000, 0x2417FF00, 0x100)]:
                self.SFX_location.append(index)
                index += 2
            elif int.from_bytes(data[index * 4:(index * 4) + 4], 'big') == 0x0402023F:
                self.animation_location.append(index)
                index += 2
            else:
                self.unused_offsets.append(index)
                index += 1

    def clear(self):
        """
        :return: clears all the indexed information of the MoveData, should only be used for the update() command,
        returns nothing
        """
        self.hitbox_location = []  #
        self.hitbox_apperence_location = []  #
        self.sync_timer_location = []  #
        self.async_timer_location = []  #
        self.summon_projectile_location = []  #
        self.POW_DMG_GRD_location = []  #
        self.ANG_DIR_location = []  #
        self.horizontal_mobility_location = []  #
        self.vertical_mobility_location = []  #
        self.GFX_location = []  #
        self.SFX_location = []  #
        self.animation_location = []  #
        self.pointers_01300000 = []  #
        self.pointers_01320000 = []  #
        self.pointers_01330000 = []  #
        self.pointers_01340000 = []  #
        self.pointers_013C0000 = []  #
        self.AF_flag = []  #
        self.AF_flag_add = []  #
        self.AF_flag_remove = []  #
        self.NF_flag = []  #
        self.NF_flag_remove = []  #
        self.KF_flag = []  #
        self.KF_flag_add = []  #
        self.KF_flag_remove = []  #
        self.KF_flag_projectile = []  #
        self.RF_flag = []  #
        self.K2F_flag = []  #
        self.K2F_flag_remove = []  #
        self.N2F_flag = []  #
        self.N2F_flag_remove = []  #
        self.EF_flag = []  #
        self.unused_offsets = []  #

    def print(self):
        """
        :return: prints the information contained in the MoveData class, will not print empty lists, returns nothing
        """
        print('Amount of words is', (len(self.data) // 4), 'index starts at 0')

        if len(self.AF_flag) != 0:
            print('AF flag locations ', self.AF_flag)
        if len(self.AF_flag_add) != 0:
            print('AF flag add', self.AF_flag_add)
        if len(self.AF_flag_remove) != 0:
            print('AF flag remove', self.AF_flag_remove)

        if len(self.NF_flag) != 0:
            print('NF Flag locations', self.NF_flag)
        if len(self.NF_flag_remove) != 0:
            print('NF Flag remove', self.NF_flag_remove)

        if len(self.KF_flag) != 0:
            print('KF Flag locations', self.KF_flag)
        if len(self.KF_flag_add) != 0:
            print('KF Flag add', self.KF_flag_add)
        if len(self.KF_flag_remove) != 0:
            print('KF Flag remove', self.KF_flag_remove)
        if len(self.KF_flag_projectile) != 0:
            print('KF Flag projectile', self.KF_flag_projectile)

        if len(self.RF_flag) != 0:
            print('RF Flag locations', self.RF_flag)

        if len(self.K2F_flag) != 0:
            print('K2F Flag locations', self.K2F_flag)
        if len(self.K2F_flag_remove) != 0:
            print('K2F Flag remvoe', self.K2F_flag_remove)

        if len(self.N2F_flag) != 0:
            print('N2F Flag locations', self.N2F_flag)
        if len(self.N2F_flag_remove) != 0:
            print('N2F Flag remove', self.N2F_flag_remove)

        if len(self.EF_flag) != 0:
            print('EF Flag locations', self.EF_flag)

        if len(self.pointers_01300000) != 0:
            print('01 30 00 00 pointers', self.pointers_01300000)
        if len(self.pointers_01320000) != 0:
            print('01 32 00 00 pointers', self.pointers_01320000)
        if len(self.pointers_01330000) != 0:
            print('01 33 00 00 pointers', self.pointers_01330000)
        if len(self.pointers_01340000) != 0:
            print('01 34 00 00 pointers', self.pointers_01340000)
        if len(self.pointers_013C0000) != 0:
            print('01 3C 00 00 pointers', self.pointers_013C0000)

        if len(self.hitbox_location) != 0:
            print('Hitbox locations', self.hitbox_location)
        if len(self.hitbox_apperence_location) != 0:
            print('Hitbox apperance locations', self.hitbox_apperence_location)

        if len(self.sync_timer_location) != 0:
            print('Sync timer locations', self.sync_timer_location)
        if len(self.async_timer_location) != 0:
            print('Async timer locations', self.async_timer_location)

        if len(self.summon_projectile_location) != 0:
            print('Projectile summon location', self.summon_projectile_location)

        if len(self.animation_location) != 0:
            print('Animation location', self.animation_location)

        if len(self.GFX_location) != 0:
            print('GFX locations', self.GFX_location)
        if len(self.SFX_location) != 0:
            print('SFX locations', self.SFX_location)

        if len(self.POW_DMG_GRD_location) != 0:
            print('POW DMG GRD location', self.POW_DMG_GRD_location)
        if len(self.ANG_DIR_location) != 0:
            print('ANG DIR location', self.ANG_DIR_location)

        if len(self.vertical_mobility_location) != 0:
            print('Vertical mobility location', self.vertical_mobility_location)
        if len(self.horizontal_mobility_location) != 0:
            print('Horizontal mobility location', self.horizontal_mobility_location)

        print('unknown words are', self.unused_offsets)

    def __str__(self):
        return "{0}".format(self.__dict__)

def build_MoveData(an_seq_object, action_id):
    """
    :param an_seq_object: SEQ_Object of the SEQ in which the MoveData object will be made of
    :param action_id: the Action ID of the move you want to use AS AN INTEGER, if you want to start not where an
    Action ID points, use default constructor
    :return: returns a MoveData object
    """
    temp_list = list(an_seq_object.action_id_table)
    temp_list.append(int.from_bytes(an_seq_object.data[0x14:0x18], 'big'))
    temp_list.sort()
    end = 0
    CC_counter = 0
    print(an_seq_object.action_id_table[action_id], 'is the pointed to value')
    print(temp_list[608], 'this is 609 in temp list, should be bigger')
    while (an_seq_object.action_id_table[action_id] >= temp_list[end]): #  and (CC_counter < 3)
        end += 1
        #print(end)
        if int.from_bytes(an_seq_object.data[(an_seq_object.action_id_table[action_id] + end * 4):(
                an_seq_object.action_id_table[action_id] + (end + 1) * 4)], 'big') == 0xCCCCCCCC:
            CC_counter += 1

    #if CC_counter > 3:
       # return MoveData(an_seq_object.data_range(an_seq_object.action_id_table[action_id],
        #  an_seq_object.action_id_table[action_id] + ((end - 4) * 4)), action_id)
    print(an_seq_object.action_id_table[action_id] + ((end - 4) * 4))
    print(temp_list[end])
    return MoveData(an_seq_object.data_range(an_seq_object.action_id_table[action_id], temp_list[end]), action_id)
