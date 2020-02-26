class MoveData:
    def __init__(self,data):
        self.hitbox_location = []
        self.sync_timer_location = []
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

        self.update(data)

    def update(self,data):




