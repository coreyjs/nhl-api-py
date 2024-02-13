from nhlpy.api.query.builder import QueryBase


class ShootCatches(QueryBase):
    def __init__(self, shoot_catch: str):
        """

        :param shoot_catch: L, R
        """
        self.shoot_catch = shoot_catch
        self.shoot_catch_q = "shootsCatches"
