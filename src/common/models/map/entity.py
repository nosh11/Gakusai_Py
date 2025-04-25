class Entity:
    def __init__(self, entity_type: str, name: str, position: list, **kwargs):
        """
        エンティティ (敵やオブジェクト) を表現するクラス
        :param entity_type: エンティティの種類 (enemy, other)
        :param name: エンティティの名前
        :param init_x: 初期位置のX座標
        :param init_y: 初期位置のY座標
        """
        self.entity_type = entity_type
        self.name = name
        self.position = position  # [x, y]のリスト形式で位置を保持