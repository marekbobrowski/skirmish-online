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
        all_players = self.session.player_cache.all_players()

        self.db = pandas.DataFrame(columns=["x", "y", "z"], dtype=float)
        for player in all_players:
            self.update_position(player)

        self.redis = None  # will garbage collect redis connection
        self.player_cache = None  # will garbage collect player cache as well

    def update_position(self, player_position):
        """
        Updates player position in cache
        """
        self.db.at[player_position.id] = {
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
            self.db.index[
                (self.db["x"] >= player_position.x - x_range)
                & (self.db["x"] <= player_position.x + x_range)
                & (self.db["y"] >= player_position.y - y_range)
                & (self.db["y"] <= player_position.y + y_range)
                & (self.db["z"] >= player_position.z - z_range)
                & (self.db["z"] <= player_position.z + z_range)
            ].tolist()
        ) - {player_position.id}
        return list(result)
