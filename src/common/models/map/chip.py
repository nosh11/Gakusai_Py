class Chip:
    def __init__(self, id: int, passable: bool, durability: int, layer: int, **kwargs):
        """
        チップの基本情報を表現するクラス
        :param passable: 通行可能かどうか
        :param durability: 耐久値 (-1: イミュータブル, 0以上: 壊れるまでの攻撃回数)
        :param layer: レイヤー (数値が高いほど上に表示)
        """
        self.id: int = id
        self.passable = passable
        self.durability = durability
        self.layer = layer