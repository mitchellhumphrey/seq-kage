class Character:
    def __init__(self,path,health_offset_temp,guard_offset_temp,name):
        self.seq_path = path
        self.health_offset = health_offset_temp
        self.guard_offset = guard_offset_temp
        self.name = name
        
        
def seq(a):
    return "//files//chr//"+a+"//0000.seq"


char_table = [
Character("//files//chr//nar//0000.seq","2FAD4","2FAD8","Naruto"),
Character("//files//chr//nej//0000.seq","25C0C","25C10","Neji"),
Character("//files//chr//ank//0000.seq","25720","25724","Anko"),
Character("//files//chr//bou//0000.seq","28154","28158","Jirobo"),
Character("//files//chr//cho//0000.seq","26DE8","26DEC","Choji"),
Character("//files//chr//gai//0000.seq","24714","24718","Gai"),
Character("//files//chr//gar//0000.seq","28644","28648","Garra"),
Character("//files//chr//hak//0000.seq","24C1C","24C20","Haku"),
Character("//files//chr//hi2//0000.seq","24540","24544","Awakened Hinata"),
Character("//files//chr//hin//0000.seq","25AD0","25AD4","Hinata"),
Character("//files//chr//ino//0000.seq","26FF4","26FF8","Ino"),
Character("//files//chr//hak//0000.seq","2317C","23180","Iruka"),
Character(seq('ita'),"2959C","295A0","Itachi")



]