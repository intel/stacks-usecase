"""find similar images"""

import numpy as np
from skimage.metrics import structural_similarity as _ssim


class Similarity:
    """utility class to identify if two images are similar or not."""

    @staticmethod
    def _resize(img: np.ndarray, shape=[480, 480]) -> np.ndarray:
        return np.resize(img, shape)

    def __init__(self, img1: np.ndarray, img2: np.ndarray) -> None:
        self.img1 = self._resize(img1).astype(np.float32)
        self.img2 = self._resize(img2).astype(np.float32)

    def mae(self, beta: float = 150.0) -> bool:
        """use mean absolute error to identify if 2 images are similar.

        beta is a hand tuned threshold difference between the images.

        Args:
            beta(float): error threshold, default is 234.0
        Returns:
            bool, True if image is similar, Flase if not
        """

        err: float = np.sum(self.img1 - self.img2)
        err = abs(err / 256)
        if err > beta:
            return False
        return True

    def l2(self, beta: float = 3000.0) -> bool:
        """use euclidean distance to identify if 2 images are similar.

        beta is a hand tuned threshold difference between the images.

        Args:
            beta(float): error threshold, default is 234.0
        Returns:
            bool, True if image is similar, Flase if not
        """

        err = np.sqrt(np.sum(np.square(self.img1 - self.img2)))
        if err > beta:
            return False
        return True

    def ssim(self, alpha=0.92):
        """structural similarity index image.

        Args:
            alpha(float): similarity index threshold, default is 0.92
        Returns:
            bool, True if image is similar, Flase if not
        """
        idx = _ssim(self.img1, self.img2, data_range=self.img2.max() - self.img2.min())
        if idx < alpha:
            return False
        return True


if __name__ == "__main__":
    from PIL import Image

    arr = lambda img: np.array(img)
    # add images(img1, img2) to local dir , stock images are not provided
    img1 = arr(Image.open("img1.jpg"))
    img2 = arr(Image.open("img2.jpg"))
    ss0 = Similarity(img1, img2)
    print("img1, img2")
    ss0.mae()
    ss0.ssim()
    ss0.l2()
