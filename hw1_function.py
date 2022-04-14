import tkinter as tk
import cv2 as cv
from tkinter import filedialog
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np
import math

file_path_open = ''
file_path_save = ''
original_img = cv
cv2image = cv
all_mouse = []


def show_image(window):
    global cv2image
    size = cv2image.shape
    window.geometry('%dx%d' % (size[1], size[0]))
    img = cv.cvtColor(cv2image, cv.COLOR_BGR2RGB)
    imgTk = ImageTk.PhotoImage(Image.fromarray(img))
    lbl_2 = tk.Label(window, image=imgTk)
    lbl_2.image = imgTk
    lbl_2.grid(column=0, row=0, sticky='nw')


# 開啟影像
def open_image(window):
    global file_path_open
    global original_img
    global cv2image

    # 開啟視窗選擇檔案
    file_path_open = filedialog.askopenfilename(title=u'選擇檔案',
                                                filetypes=(("png file", "*.png"),
                                                           ("jpg file", "*.jpg"),
                                                           ("jpeg file", "*.jpeg")))

    if file_path_open is None:
        return

    original_img = cv.imread(file_path_open)
    cv2image = original_img
    show_image(window)


# 儲存影像
def save_image():
    global file_path_save
    global cv2image

    if cv2image is None:
        return

    # 開啟視窗選擇檔案儲存位置
    file_path_save = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path_save is None:
        return

    # 寫入檔案
    cv.imwrite(file_path_save, cv2image)


# 設置影像roi
def set_roi(window):
    global original_img
    global cv2image

    if original_img is None:
        return

    r = cv.selectROI(original_img, False)

    if int(max(r)) != 0:
        original_img = original_img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        cv2image = original_img
        cv.destroyAllWindows()
        show_image(window)
    else:
        cv.destroyAllWindows()
        tk.messageBox.showerror("選取失敗", "請重新選擇")


# 顯示影像資訊
def show_image_information():
    global original_img

    if original_img is None:
        return

    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist = cv.calcHist([original_img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])

    size = original_img.shape
    plt.title("height: %f\nweight: %f" % (size[0], size[1]))
    plt.show()


# 變更影像空間RGB
def change_color_space_rgb(window):
    global original_img
    global cv2image

    if original_img is None:
        return

    cv2image = cv.cvtColor(original_img, cv.COLOR_BGR2RGB)
    show_image(window)


# 變更影像空間HSV
def change_color_space_hsv(window):
    global original_img
    global cv2image

    if original_img is None:
        return

    cv2image = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)
    show_image(window)


# 變更影像空間gray
def change_color_space_gray(window):
    global original_img
    global cv2image

    if original_img is None:
        return

    cv2image = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
    show_image(window)


# 均值濾波
def averaging_filter(window):
    global original_img
    global cv2image
    cv2image = cv.blur(original_img, (11, 11))
    show_image(window)


# 高斯濾波
def gaussian_filter(window):
    global original_img
    global cv2image
    cv2image = cv.GaussianBlur(original_img, (11, 11), -1)
    show_image(window)


# 中值濾波
def median_filter(window):
    global original_img
    global cv2image
    cv2image = cv.medianBlur(original_img, 11)
    show_image(window)


# 雙邊濾波
def bilateral_filter(window):
    global original_img
    global cv2image
    img_bi = cv.bilateralFilter(original_img, 9, 5, 5)
    img_bi2 = cv.bilateralFilter(original_img, 9, 50, 50)
    img_bi3 = cv.bilateralFilter(original_img, 9, 100, 100)
    cv2image = cv.hconcat([img_bi, img_bi2, img_bi3])
    show_image(window)


# 索貝爾濾波
def sobel_filter(window):
    global original_img
    global cv2image
    x = cv.Sobel(original_img, cv.CV_16S, 1, 0)
    y = cv.Sobel(original_img, cv.CV_16S, 0, 1)
    abs_x = cv.convertScaleAbs(x)  # 轉回uint8
    abs_y = cv.convertScaleAbs(y)
    img_sobel = cv.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    cv2image = cv.hconcat([abs_x, abs_y, img_sobel])
    show_image(window)


# 拉普拉斯濾波
def laplacian_filter(window):
    global original_img
    global cv2image
    gray_lap = cv.Laplacian(original_img, cv.CV_16S, ksize=3)
    cv2image = cv.convertScaleAbs(gray_lap)
    show_image(window)


# 影像二值化
def thresholding(window):
    global original_img
    global cv2image
    thr = 127
    gra = 255

    if original_img is None:
        return

    cv2image = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)

    # 開啟新視窗
    cv.namedWindow('Imgae_Thresholding')

    # 新增Trackbar
    cv.createTrackbar('Threshold', 'Imgae_Thresholding', 0, 127, update)
    cv.createTrackbar('Gray-Scale Value', 'Imgae_Thresholding', 0, 255, update)

    # 執行二值化
    while True:
        thr = cv.getTrackbarPos('Threshold', 'Imgae_Thresholding')
        gra = cv.getTrackbarPos('Gray-Scale Value', 'Imgae_Thresholding')
        ret, mask = cv.threshold(cv2image, thr, gra, cv.THRESH_BINARY)
        cv.imshow('Imgae_Thresholding', mask)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2image = mask
    show_image(window)
    cv.destroyAllWindows()


# 仿射轉換
def affine_transform(window):
    global original_img
    global cv2image
    size = original_img.shape
    row = size[0]
    col = size[1]

    if original_img is None:
        return

    pts1 = np.float32([[0, 0], [0, row], [col, 0]])

    # 開啟新視窗
    cv.namedWindow('Affine_Transform')

    # 新增Trackbar
    cv.createTrackbar('a(x)', 'Affine_Transform', 0, col, update)
    cv.createTrackbar('a(y)', 'Affine_Transform', 0, row, update)
    cv.createTrackbar('b(x)', 'Affine_Transform', 0, col, update)
    cv.createTrackbar('b(y)', 'Affine_Transform', 0, row, update)
    cv.createTrackbar('c(x)', 'Affine_Transform', 0, col, update)
    cv.createTrackbar('c(y)', 'Affine_Transform', 0, row, update)

    # 執行仿射轉換
    while True:
        ax = cv.getTrackbarPos('a(x)', 'Affine_Transform')
        ay = cv.getTrackbarPos('a(y)', 'Affine_Transform')
        bx = cv.getTrackbarPos('b(x)', 'Affine_Transform')
        by = cv.getTrackbarPos('b(y)', 'Affine_Transform')
        cx = cv.getTrackbarPos('c(x)', 'Affine_Transform')
        cy = cv.getTrackbarPos('c(y)', 'Affine_Transform')
        pts2 = np.float32([[ax, ay], [bx, by], [cx, cy]])
        M = cv.getAffineTransform(pts1, pts2)
        img_aff = cv.warpAffine(original_img, M, (col, row))
        cv.imshow('Affine_Transform', img_aff)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2image = img_aff
    show_image(window)
    cv.destroyAllWindows()

# 透視投影轉換
def perspective_transform(window):
    global original_img
    global cv2image
    global all_mouse
    all_mouse = []

    if original_img is None:
        return

    # 開啟新視窗
    cv.namedWindow('Perspective_Transform')
    cv.imshow('Perspective_Transform', original_img)

    while True:
        cv.setMouseCallback('Perspective_Transform', OnMouseAction)
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break

    cv.destroyAllWindows()
    h = (math.sqrt((abs(all_mouse[0][0]-all_mouse[1][0])**2)+(abs(all_mouse[0][1]-all_mouse[1][1]))**2)+
        math.sqrt((abs(all_mouse[2][0]-all_mouse[3][0])**2)+(abs(all_mouse[2][1]-all_mouse[3][1]))**2))/2
    w = (math.sqrt((abs(all_mouse[1][0]-all_mouse[2][0])**2)+(abs(all_mouse[1][1]-all_mouse[2][1]))**2)+
        math.sqrt((abs(all_mouse[3][0]-all_mouse[0][0])**2)+(abs(all_mouse[3][1]-all_mouse[0][1]))**2))/2
    h = math.ceil(h)
    w = math.ceil(w)
    pts1 = np.float32([all_mouse[0], all_mouse[3], all_mouse[2], all_mouse[1]])
    pts2 = np.float32([[0, 0], [0, w], [h, w], [h, 0]])
    M = cv.getPerspectiveTransform(pts1, pts2)
    cv2image = cv.warpPerspective(original_img, M, (h, w))
    show_image(window)
    cv.destroyAllWindows()


def OnMouseAction(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        all_mouse.append([x, y])


# 直方圖等化
def histogram_equalization(window):
    global cv2image

    if cv2image is None:
        return

    change_color_space_gray(window)

    plt.figure(1)
    plt.hist(cv2image.ravel(), 256, [0, 256])
    img_eq = cv.equalizeHist(cv2image)
    plt.hist(img_eq.ravel(), 256, [0, 256])
    plt.show()


def update(x):
    pass
