import cv2
from pathlib import Path
import os


def getImgSize(img):

    image = cv2.imread(img)
    print(image.shape)


def resizeImg(img, targetSize, save_file=False):
    toPath = Path(img)
    width, height = int(targetSize)
    dim = (width, height)

    image = cv2.imread(img)

    interpolation_method = ""
    if image.shape[0] / image.shape[1] == 1:
        if image.shape[0] >= targetSize:
            interpolation_method = cv2.INTER_AREA
        else:
            interpolation_method = cv2.INTER_CUBIC
    else:
        bigger_dim = max(image[0], image[1])
        if bigger_dim >= targetSize:  # ?? shirking
            interpolation_method = cv2.INTER_AREA
        else:
            interpolation_method = cv2.INTER_CUBIC
    print("interpolation_method: ", interpolation_method)

    resize = cv2.resize(image, dim, interpolation=interpolation_method)
    if save_file:
        savePath = f"tests/outputs/resize/{toPath.stem}_resize{targetSize}.png"
        if os.path.exists("tests/outputs/resize/"):
            cv2.imwrite(savePath, resize)
        else:
            os.mkdir("tests/outputs/resize/")
            cv2.imwrite(savePath, resize)
    else:
        return resize


def toGreyScale(img, save_file=False):
    toPath = Path(img)
    image = cv2.imread(img)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if save_file:
        grey_path = "tests/outputs/grey/"
        savePath = f"tests/outputs/grey/{toPath.stem}_greyscale.png"
        if os.path.exists(grey_path):
            cv2.imwrite(savePath, grey)
        else:
            os.mkdir(grey_path)
            cv2.imwrite(savePath, grey)
    else:
        return grey


def flipImg(img, axis, save_file=False):
    toPath = Path(img)
    image = cv2.imread(img)
    flip = cv2.flip(image, axis)
