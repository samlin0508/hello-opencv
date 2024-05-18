import cv2 as cv
import pytesseract as pytesseract

avatar = cv.imread("input/test6.png")

avatar_in_gray = cv.cvtColor(avatar, cv.COLOR_BGR2GRAY)
cv.imwrite('output/avatar_in_gray.jpg', avatar_in_gray)

avatar_in_gaussian_blur = cv.GaussianBlur(avatar_in_gray, (5,5), 0)
cv.imwrite('output/avatar_in_gaussian_blur.jpg', avatar_in_gaussian_blur)

avatar_in_canny = cv.Canny(avatar_in_gaussian_blur, 100, 200)
cv.imwrite('output/avatar_in_canny.jpg', avatar_in_canny)

(thresh, thresholded_image) = cv.threshold(avatar_in_gray, 128, 255, cv.THRESH_OTSU)
cv.imwrite('output/thresholded_image.jpg', thresholded_image)

captured_text = pytesseract.image_to_string(avatar_in_gray, lang='chi_tra')
boxes = pytesseract.image_to_boxes(avatar_in_gray)

for line in boxes.splitlines():
    axis = line.split(' ')
    x, y, w, h = int(axis[1]), int(axis[2]), int(axis[3]), int(axis[4])
    cv.rectangle(avatar, (x, avatar.shape[0] - y), (w, avatar.shape[0] - h), (0, 0, 255), 2)

print(captured_text)
cv.imwrite('output/test6-rounded.jpg', avatar)