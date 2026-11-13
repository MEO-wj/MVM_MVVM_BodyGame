import cv2
import numpy as np

def normalize_light(image):
    mean = np.array(cv2.mean(image)[0:3], dtype=np.float32)
    gain = np.clip(128 / np.maximum(mean, 1), 0.1, 3)
    result = np.clip(image.astype(np.float32) * gain, 0, 255)
    result = result.astype(np.uint8)

    return result

def clean_mask(mask):
    # 定义椭圆形滤波器
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # 开运算去除环境噪声
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # 闭运算去除主体噪声
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # 获取所有连通域的信息
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    if count > 1:
        # 取面积最大的连通域
        largest = 1 + stats[1:, cv2.CC_STAT_AREA].argmax()
        # 将连通域覆盖的像素涂上白色（置255）
        mask = np.uint8(labels == largest) * 255
    return mask

def segment(image):
    # 光照归一化
    light_corrected = normalize_light(image)
    # 转换色彩空间
    ycrcb = cv2.cvtColor(light_corrected, cv2.COLOR_BGR2YCrCb)
    # 提取遮罩
    mask = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
    mask = clean_mask(mask)
    return mask

if __name__ == "__main__":
    img = cv2.imread("Picture1.png")
    result = segment(img)
    cv2.imshow("origin", img)
    cv2.imshow("result", result)
    cv2.waitKey(0)
    