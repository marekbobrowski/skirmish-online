import pandas


class PlayerPositionCache:
    def __init__(self, session):
        """
        PlayerPositionCache is cache of user positions.

        It provides easy searching for nearby players
        in rectangular areas and then allows to narrow
        down the search
        """
        self.session = session
        self.all_positions = pandas.DataFrame(columns=["x", "y", "z"], dtype=float)

    def update_position(self, player_position):
        """
        Updates player position in cache
        """
        self.all_positions.at[player_position.id] = {
            "x": player_position.x,
            "y": player_position.y,
            "z": player_position.z,
        }

    def get_nearby(self, player_position, x_range, y_range, z_range):
        """
        Searches in rectangular area for nearby players
        to given player_position
        """
        result = set(
            self.all_positions.index[
                (self.all_positions["x"] >= player_position.x - x_range)
                & (self.all_positions["x"] <= player_position.x + x_range)
                & (self.all_positions["y"] >= player_position.y - y_range)
                & (self.all_positions["y"] <= player_position.y + y_range)
                & (self.all_positions["z"] >= player_position.z - z_range)
                & (self.all_positions["z"] <= player_position.z + z_range)
            ].tolist()
        ) - {player_position.id}
        return list(result)
