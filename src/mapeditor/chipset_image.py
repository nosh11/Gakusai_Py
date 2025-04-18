from common.game_map import ChipSet
import cv2

def get_chip_image(chipset: ChipSet, chip_id: int):
    """
    チップセットから指定されたチップの画像を取得する関数
    :param chipset: チップセットのIDまたはパス
    :param chip_id: チップのID
    :return: チップの画像のパス
    """
    path = chipset.chipset_image_path
    # デバッグ用にパスを出力して確認
    print(f"Attempting to load image from path: {path}")
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # 画像が読み込めない場合はエラーを返す
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")
    # チップのサイズを取得 (仮に16x16とする)
    chip_width = 16
    chip_height = 16
    # チップの位置を計算
    x = (chip_id % (image.shape[1] // chip_width)) * chip_width
    y = (chip_id // (image.shape[1] // chip_width)) * chip_height
    # チップの画像を切り出す
    chip_image = image[y:y + chip_height, x:x + chip_width]
    return chip_image