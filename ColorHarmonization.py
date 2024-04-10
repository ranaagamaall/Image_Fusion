from enum import Enum
import numpy as np
import cv2
import skimage


class CH(Enum):
    NOTHING = 0
    BRIGHTNESS_WHOLE = 1
    BRIGHTNESS_OBJ = 2


class Color_Harmonization:
    def __init__(self, background, foreground, mask, method: CH = CH.BRIGHTNESS_WHOLE):
        self.background = background
        self.foreground = cv2.resize(
            foreground, (background.shape[1], background.shape[0]))
        self.mask = cv2.resize(
            mask, (background.shape[1], background.shape[0]))
        self.mask = self.mask == self.mask.max()
        self.mask_3d = self.mask[..., np.newaxis]
        self.method = method

    def harmonize(self):
        if self.method == CH.BRIGHTNESS_WHOLE:
            self.foreground = self._brightness_adjustment_whole()
        if self.method == CH.BRIGHTNESS_OBJ:
            self.foreground = self._brightness_adjustment_object()

        mask = self.mask == self.mask.max()
        if mask.ndim == 2:
            mask = self.mask[..., np.newaxis]

        if self.foreground.max() <= 1:
            self.foreground = self.foreground * 255

        if self.background.max() <= 1:
            self.background = self.background * 255

        return np.where(mask, self.foreground, self.background).astype(np.uint8)

    def _brightness_adjustment_whole(self):
        background_avg_v = skimage.color.rgb2hsv(self.background)[
            :, :, 2].mean()
        foreground_avg_v = skimage.color.rgb2hsv(self.foreground)[
            :, :, 2].mean()
        foreground_hsv = skimage.color.rgb2hsv(self.foreground)
        foreground_hsv[:, :, 2] = foreground_hsv[:, :, 2] * \
            (background_avg_v / foreground_avg_v)

        return skimage.color.hsv2rgb(foreground_hsv)

    def _brightness_adjustment_object(self):
        background = self.background * self.mask_3d
        background_avg_v = skimage.color.rgb2hsv(
            background)[:, :, 2].sum() / (self.mask == self.mask.max()).sum()
        foreground = self.foreground * self.mask_3d
        foreground_avg_v = skimage.color.rgb2hsv(
            foreground)[:, :, 2].sum() / (self.mask == self.mask.max()).sum()
        foreground_hsv = skimage.color.rgb2hsv(foreground)
        foreground_hsv[:, :, 2] = foreground_hsv[:, :, 2] * \
            (background_avg_v / foreground_avg_v)

        return skimage.color.hsv2rgb(foreground_hsv)
