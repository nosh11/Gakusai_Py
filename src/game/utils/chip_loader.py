import cv2
from common.consts.screen_settings import CHIP_SIZE
from game.consts.screen_settings import ZOOMED_CHIP
from game.scenes.utils.image_manager import convert_opencv_img_to_pygame


def get_chip_image(chipset_image, chip_id: int):
    x = (chip_id % (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    y = (chip_id // (chipset_image.shape[1] // CHIP_SIZE)) * CHIP_SIZE
    chip_image = chipset_image[y:y + CHIP_SIZE, x:x + CHIP_SIZE]
    chip_image = cv2.resize(chip_image, (ZOOMED_CHIP, ZOOMED_CHIP), interpolation=cv2.INTER_NEAREST)
    return convert_opencv_img_to_pygame(chip_image)