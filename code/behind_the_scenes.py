from typing import Dict, List
from users import User

# CONFIGURE LATER!
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

        # Team scores
        # DEFAULT 0(?)
        self.red_team_score: int = 0
        self.blue_team_score: int = 0

    #     # If bases are scored
        self.red_base_scored: bool = False
        self.blue_base_scored: bool = False
        self.game_event_actions: [str] = []
    
    def player_hit(self, equipment_shooter_code: int, equipment_hit_code: int) -> None:
        # Attributing points to a blue user
        for user in self.blue_users:
            # Check if id matches, and if player doesn't hit own teammate
            if user.equipment_ID == equipment_shooter_code and equipment_hit_code not in self.blue_user_equipment_ids:
                user.game_score += points_per_tag
                self.blue_team_score += points_per_tag
                for victim_user in self.red_users:
                    if victim_user.equipment_ID == equipment_hit_code:
                        shot_user: User = victim_user
                self.game_event_actions.append(f"{user.username} hit {shot_user.username}")
        
        # Attributing points to a red user
        for user in self.red_users:
            # Check if id matches, and if player doesn't hit own teammate
            if user.equipment_ID == equipment_shooter_code and equipment_hit_code not in self.red_user_equipment_ids:
                user.game_score += points_per_tag
                self.red_team_score += points_per_tag
                for victim_user in self.blue_users:
                    if victim_user.equipment_ID == equipment_hit_code:
                        shot_user: User = victim_user
                self.game_event_actions.append(f"{user.username} hit {shot_user.username}")

    def red_base_hit(self, equipment_shooter_code: int) -> None:
        for user in self.blue_users:
            # Check if id matches, and then add 100 points to the blue player and team
            if user.equipment_ID == equipment_shooter_code:
                user.game_score += points_per_base_hit
                self.blue_team_score += points_per_base_hit
                self.game_event_actions.append(f"{user.username} hit red base")

    def blue_base_hit(self, equipment_shooter_code: int) -> None:
        for user in self.red_users:
            # Check if id matches, and then add 100 points to the red player and team
            if user.equipment_ID == equipment_shooter_code:
                user.game_score += points_per_base_hit
                self.red_team_score += points_per_base_hit
                self.game_event_actions.append(f"{user.username} hit blue base")
