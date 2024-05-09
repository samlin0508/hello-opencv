import cv2 as cv
import pytesseract as pytesseract

avatar = cv.imread("input/line_avatar_yellow_480.png")
avatar_in_gray = cv.cvtColor(avatar, cv.COLOR_BGR2GRAY)
avatar_in_gaussian_blur = cv.GaussianBlur(avatar_in_gray, (5,5), 0)
avatar_in_canny = cv.Canny(avatar_in_gaussian_blur, 100, 150)
captured_text = pytesseract.image_to_string(avatar_in_canny, lang='eng')
print(captured_text)