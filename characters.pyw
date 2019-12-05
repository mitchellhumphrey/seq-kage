class Character:
    def __init__(self,path,health_offset_temp,guard_offset_temp,name):
        self.seq_path = path
        self.health_offset = health_offset_temp
        self.guard_offset = guard_offset_temp
        self.name = name
char_table = [
Character("//files//chr//nar//0000.seq","2FAD4","2FAD8","Naruto"),
Character("//files//chr//nej//0000.seq","25C0C","25C10","Neji"),
Character("//files//chr//ank//0000.seq","25720","25724","Anko"),
Character("//files//chr//bou//0000.seq","28154","28158","Jirobo")]