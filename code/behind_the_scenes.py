from typing import Dict, List
from users import User

points_per_tag: int = 10
points_per_base_hit: int = 100

class theGame:
    def __init__(self, users_raw: Dict[str, List[User]]) -> None:

        self.blue_users = users_raw["blue"]
        self.red_users = users_raw["red"]

        # Red equipment IDs LIST!
        self.red_user_equipment_ids = []
        for user in self.red_users:
            self.red_user_equipment_ids.append(user.equipment_ID)

        # Blue equipment IDs  LIST!
        self.blue_user_equipment_ids = []
        for user in self.blue_users:
            self.blue_user_equipment_ids.append(user.equipment_ID)

        # Team scores, set to default of zero
        self.red_team_score: int = 0
        self.blue_team_score: int = 0

    #     # If bases are scored
        self.red_base_scored: bool = False
        self.green_base_scored: bool = False
        self.game_event_list = []
    
