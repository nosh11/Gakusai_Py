from common.model.game_map import ChipSet
from common.consts.screen_settings import CHIP_SIZE
import cv2

from PyQt6.QtGui import QImage

def get_chip_image(chipset: ChipSet, chip_id: int) -> QImage:
    """
    チップセットから指定されたチップの画像を取得する関数
    :param chipset: チップセットのIDまたはパス
    :param chip_id: チップのID
    :return: チップの画像のパス
    """
    path = chipset.chipset_image_path
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # 画像が読み込めない場合はエラーを返す
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")
    # チップのサイズを取得 (仮に16x16とする)
    # チップの位置を計算
    x = (chip_id % (image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    y = (chip_id // (image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    # チップの画像を切り出す
    chip_image = image[y:y + CHIP_SIZE, x:x + CHIP_SIZE]

    # チップの画像を4倍に拡大
    chip_image = cv2.resize(chip_image, (CHIP_SIZE * 4, CHIP_SIZE * 4), interpolation=cv2.INTER_NEAREST)

    # OpenCVのBGR形式からQtのRGB形式に変換
    chip_image = cv2.cvtColor(chip_image, cv2.COLOR_BGR2RGB)
    # OpenCVの画像をQImageに変換
    height, width, channel = chip_image.shape
    bytes_per_line = channel * width
    # QImageの形式を指定 (RGB888)
    q_image = QImage(chip_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    # QImageを返す
    return q_image