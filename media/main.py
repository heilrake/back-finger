import cv2
import os


def normalize_fingerprint(image):
    # Конвертувати відбиток пальця в чорно-біле зображення
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Застосувати порогову фільтрацію для виділення контуру пальця
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Знайти контури на пороговому зображенні
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Вибрати найбільший контур (очікується, що це буде контур пальця)
    largest_contour = max(contours, key=cv2.contourArea)

    # Отримати описовий прямокутник для найбільшого контуру
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Обрізати зображення за межами описового прямокутника
    cropped_image = image[y:y + h, x:x + w]

    # Змінити масштаб зображення на певний розмір (наприклад, 300x300)
    resized_image = cv2.resize(cropped_image, (300, 300))

    return resized_image

def checkUser(source_image_path):
    source_image = cv2.imread(source_image_path)
    score = 0
    file_name = None
    image = None
    kp1, kp2, mp = None, None, None

    for file in os.listdir("./media/images/"):
        target_image = cv2.imread("./media/images/" + file)

        # Нормалізувати відбитки пальців
        #source_image = normalize_fingerprint(source_image)
        #target_image = normalize_fingerprint(target_image)
        cv2.imshow('image', source_image)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(source_image, None)
        kp2, des2 = sift.detectAndCompute(target_image, None)
        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10),dict()).knnMatch(des1, des2, k=2)
        # точки які знаходяться на однаковій відстані
        mp = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                mp.append(p)
        keypoints = 0
        if len(kp1) <= len(kp2):
            keypoints = len(kp1)
        else:
            keypoints = len(kp2)

        if len(mp) / keypoints * 100 > score:
            score = len(mp) / keypoints * 100
            file_name = file
            image = cv2.drawMatches(source_image, kp1, target_image, kp2, mp, None)
            image = cv2.resize(image, None, fx=2.5, fy=2.5)
            cv2.imwrite( './media/check_img.BMP', image)

    return score, file_name

