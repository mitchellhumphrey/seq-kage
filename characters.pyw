class Character:
    def __init__(self,path,health_offset_temp,guard_offset_temp,name):
        self.seq_path = path
        self.health_offset = health_offset_temp
        self.guard_offset = guard_offset_temp
        self.name = name
        
        
def seq(a):
    return "//files//chr//"+a+"//0000.seq"


char_table = [


Character(seq('ank'),"25720","25724","Anko"),
Character(seq('bou'),"28154","28158","Jirobo"),
Character(seq('cho'),"26DE8","26DEC","Choji"),
Character(seq('gai'),"24714","24718","Gai"),
Character(seq('gar'),"28644","28648","Gaara"),
Character(seq('hak'),"24C1C","24C20","Haku"),
Character(seq('hi2'),"24540","24544","Awakened Hinata"),
Character(seq('hin'),"25AD0","25AD4","Hinata"),
Character(seq('ino'),"26FF4","26FF8","Ino"),
Character(seq('hak'),"2317C","23180","Iruka"),
Character(seq('ita'),"2959C","295A0","Itachi"),
Character(seq('kab'),"25274","25278","Kabuto"),
Character(seq('kak'),"32580","32584","Kakashi"),
Character(seq('kan'),"25404","25408","Kankuro"),
Character(seq('kib'),"28E54","28E58","Kiba"),
Character(seq('kid'),"26E3C","26E40","Kidomaru"),
Character(seq('kim'),"27350","27354","Kimimaro"),
Character(seq('kis'),"25290","25294","Kisame"),
Character(seq('loc'),"27D04","27D08","Lee"),
Character(seq('miz'),"232F8","232FC","Mizuki"),
Character(seq('na9'),"24AA4","24AA8","Kyuubi Naruto"),
Character(seq('nar'),"2FAD4","2FAD8","Naruto"),
Character(seq('nej'),"25C0C","25C10","Neji"),
Character(seq('oro'),"27058","2705C","Orochimaru"),
Character(seq('sa2'),"269D4","269D8","Curse Mark Sasuke"),
Character(seq('sak'),"271C0","271C4","Sakura"),
Character(seq('sar'),"25444","25448","Hiruzen"),
Character(seq('sas'),"29754","29758","Sasuke"),
Character(seq('sik'),"26B7C","26B80","Shikamaru"),
Character(seq('sin'),"2590C","25910","Shino"),
Character(seq('sko'),"2650C","26510","Sakon"),
Character(seq('tay'),"28520","28524","Tayuya"),
Character(seq('tem'),"2A158","2A15C","Temari"),
Character(seq('ten'),"2B788","2B78C","Tenten"),
Character(seq('tsu'),"25B80","35B84","Tsunade"),
Character(seq('zab'),"234B0","234B4","Zabuza")



]