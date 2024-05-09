import numpy as np
import cv2
import pytesseract as pytesseract

def reselect_y_coordinates(coordinates_lst):
    coordinates_lst = sorted(coordinates_lst)
    bag = []
    result = []
    for i in coordinates_lst:
        if len(bag) == 0:
            bag.append(i)
        else:
            if i-bag[-1] ==1:               
                bag.append(i)
            else:
                if len(bag) >=5:            
                    result.append(bag[-1])  
                bag.clear()
                bag.append(i)
    return result

def reselect_x_coordinates(coordinates_lst):
    coordinates_lst = sorted(coordinates_lst)
    bag = []
    result = []
    for i in coordinates_lst:
        if len(bag) == 0:
            bag.append(i)
        else:
            if i-bag[-1] ==1:
                bag.append(i)
            else:
                if len(bag) >=3:
                    result.append(bag[-1])
                bag.clear()
                bag.append(i)
    return result




image = cv2.imread('11226-2.png')

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cv2.imwrite('output/gray.jpg', gray)

kernel_size = 3
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
cv2.imwrite('output/blur_gray.jpg', gray)

low_threshold = 50
high_threshold = 150
masked_edges = cv2.Canny(blur_gray, low_threshold, high_threshold, 3)
cv2.imwrite('output/masked_edges.jpg', masked_edges)

rho = 1
theta = np.pi/180
threshold = 100
min_line_length = 10
max_line_gap = 1
lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
lines_image = np.copy(image)*0
lines_image_pure = np.copy(image)*0

verti_lst = []
horiz_lst = []

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    #  計算斜率
    slope = (y2-y1)/(x2-x1)
    
    #  判斷斜率篩選出垂直線與水平線
    if slope == -1*np.inf:
        cv2.line(lines_image_pure,(x1,y1),(x2,y2),(0,255,0),1)
        verti_lst.append(x1)
    
    if slope == 0:
        cv2.line(lines_image_pure,(x1,y1),(x2,y2),(0,255,0),1)
        horiz_lst.append(y1)

    # x, y, w, h = cv2.boundingRect(line[0])
    # roi = image[y:y+h, x:x+w]
    # # OCR 文字识别
    # captured_text = pytesseract.image_to_string(roi, lang='chi_tra')
    # print(captured_text)

cv2.imwrite('output/lines_image.jpg', lines_image)
cv2.imwrite('output/lines_image_pure.jpg', lines_image_pure)

# color_edges = np.dstack((masked_edges, masked_edges, masked_edges))
# combo = cv2.addWeighted(color_edges, 0.8, lines_image, 1, 0) 
# cv2.imwrite('output/combo.jpg', combo)

horiz_lst = sorted(horiz_lst)
verti_lst = sorted(verti_lst)

print(horiz_lst)
print(verti_lst)

# crop_img = image[0:100,0:800]
# cv2.imwrite('output/crop_img.png', crop_img)
# crop_img2 = image[0:100,800:1600]
# cv2.imwrite('output/crop_img2.png', crop_img2)
# crop_img3 = image[100:300,0:800]
# cv2.imwrite('output/crop_img3.png', crop_img3)



gray2 = cv2.cvtColor(lines_image_pure, cv2.COLOR_RGB2GRAY)
cv2.imwrite('output/gray2.jpg', gray2)

blur_gray2 = cv2.GaussianBlur(gray2, (kernel_size, kernel_size), 0)
cv2.imwrite('output/blur_gray2.jpg', gray2)

masked_edges2 = cv2.Canny(blur_gray2, low_threshold, high_threshold, 3)
cv2.imwrite('output/masked_edges2.jpg', masked_edges2)

# 轮廓检测
# contours, _ = cv2.findContours(masked_edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# index = 0
# # 遍历每个轮廓
# for contour in contours:
#     # 计算轮廓的边界框
#     x, y, w, h = cv2.boundingRect(contour)

#     # 提取轮廓内的图像区域
#     roi = image[y:y+h, x:x+w]
#     cv2.imwrite('output/roi' + str(index) + '.jpg', roi)
#     index += 1
#     # OCR 文字识别
#     extracted_text = pytesseract.image_to_string(roi, lang='chi_tra_vert')

#     if extracted_text != '':
#         print("Text in this contour:", extracted_text.strip())