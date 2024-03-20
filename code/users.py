class User:
    rownum: int 
    equipment_ID: int
    user_ID: int
    username: str
    game_score: int
    team: str
    has_hit_base: bool
    
    # from UserInterface UI get this information in row form
    def __init__(self, rownum, equipment_ID, user_ID, username,team) -> None:
        self.rownum = rownum
        self.equipment_ID = equipment_ID
        self.user_ID = user_ID
        self.team=team
        self.username = username
        self.game_score = 10
        self.has_hit_base = False

    # String representation of User object
    # Print on a single string
    def __str__(self) -> str:
        return f"Username: {self.username}\nEquipment ID: {self.equipment_ID}\nUser ID: {self.user_ID}\nTeam: {self.team}\nGame Score: {self.game_score}\nHas Hit Base: {self.has_hit_base}\n\n"
    