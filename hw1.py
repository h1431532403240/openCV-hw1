import tkinter as tk
import hw1_function as func

window = tk.Tk()
window.title('openCV')
window.geometry('600x800')

appmenu = tk.Menu(window)

filemenu = tk.Menu(appmenu, tearoff=0)
filemenu.add_command(
    label='開啟影像', command=lambda: func.open_image(window=window))
filemenu.add_command(label='儲存影像', command=lambda:   func.save_image())
appmenu.add_cascade(label='檔案(File)', menu=filemenu)

settingmenu = tk.Menu(appmenu, tearoff=0)
setting_color_space_menu = tk.Menu(settingmenu, tearoff=0)
settingmenu.add_command(
    label='設定ROI', command=lambda: func.set_roi(window=window))
settingmenu.add_command(
    label='顯示影像資訊', command=lambda: func.show_image_information())
setting_color_space_menu.add_command(
    label='RGB', command=lambda: func.change_color_space_rgb(window=window))
setting_color_space_menu.add_command(
    label='HSV', command=lambda: func.change_color_space_hsv(window=window))
setting_color_space_menu.add_command(
    label='灰階', command=lambda: func.change_color_space_gray(window=window))
settingmenu.add_cascade(label='改變色彩空間', menu=setting_color_space_menu)
appmenu.add_cascade(label='設定(Setting)', menu=settingmenu)

processingmenu = tk.Menu(appmenu, tearoff=0)
setting_filter_menu = tk.Menu(processingmenu, tearoff=0)
setting_filter_menu.add_command(
    label='均值濾波（Averaging Filter）', command=lambda: func.averaging_filter(window=window))
setting_filter_menu.add_command(
    label='高斯濾波（Gaussian Filter）', command=lambda: func.gaussian_filter(window=window))
setting_filter_menu.add_command(
    label='中值濾波（Median Filter）', command=lambda: func.median_filter(window=window))
setting_filter_menu.add_command(
    label='雙邊濾波（Bilateral Filter）', command=lambda: func.bilateral_filter(window=window))
setting_filter_menu.add_command(
    label='索貝爾濾波（Sobel Filter）', command=lambda: func.sobel_filter(window=window))
setting_filter_menu.add_command(
    label='拉普拉斯濾波（Laplacian Filter）', command=lambda: func.laplacian_filter(window=window))
processingmenu.add_cascade(label='鄰域處理', menu=setting_filter_menu)
processingmenu.add_command(label='影像二值化(Thresholding)',
                           command=lambda: func.thresholding(window=window))
processingmenu.add_command(label='直方圖等化(Histogram Equalization)',
                           command=lambda: func.histogram_equalization(window=window))
processingmenu.add_command(label='仿射轉換(Affine Transform)',
                           command=lambda: func.affine_transform(window=window))
processingmenu.add_command(label='透視投影轉換(Perspective Transform)',
                           command=lambda: func.perspective_transform(window=window))
appmenu.add_cascade(label='影像處理(Image Processing)', menu=processingmenu)

othermenu = tk.Menu(appmenu, tearoff=0)
othermenu.add_command(
    label='合併影像(Image Merge)', command=lambda: func.image_merge(window=window))
appmenu.add_cascade(label='其他功能(others)', menu=othermenu)

appmenu.add_command(label='離開(Quit)', command=lambda: exit())

window.config(menu=appmenu)

window.mainloop()
