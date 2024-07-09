from pyautogui import screenshot
import time
from PIL import ImageGrab
import os
import codecs
import re
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

import pyautogui

import numpy

def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)

# 判断两个颜色是否接近
def is_similar_color(c1, c2):
    for i in range(3):
        if abs(c1[i] - c2[i]) > 80:
            return False
    return True

def lab_distance(color1, color2):
    """
    计算两个RGB颜色在Lab颜色空间中的距离
    :param color1: 第一个颜色，格式为 (R, G, B)
    :param color2: 第二个颜色，格式为 (R, G, B)
    :return: Lab颜色空间中的距离
    """
    color1_rgb = sRGBColor(*color1, is_upscaled=True)
    color2_rgb = sRGBColor(*color2, is_upscaled=True)

    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)

    return delta_e_cie2000(color1_lab, color2_lab)


# 获取指定区域指定颜色的截图，默认全部颜色保存
def screenshot_area(area, img_name, rgb):
    # area = (980, 640, 1067, 665)  # 这里是设置截图范围的区域
    shot = ImageGrab.grab(area)
    # 保留指定颜色
    if rgb != (0, 0, 0):
        for x in range(shot.size[0]):
            for y in range(shot.size[1]):
                pix_rgb = shot.getpixel((x, y))
                distance = lab_distance(pix_rgb, rgb)
                # print(f"两个颜色在Lab颜色空间中的距离是: {distance}")
                if distance >= 20.0:
                    shot.putpixel((x, y), (0, 0, 0))

    shot.save(img_name)


# 获取指定图片内容
def parse_content(img, lang="chi_sim"):
    cmd = "tesseract " + img + " output -l " + lang + " --psm 6"
    os.system(cmd)
    with codecs.open("output.txt", encoding="utf-8") as f:
        for line in f:
            # 去掉换行符
            line = line.strip()
            if len(line) > 0:
                return line

# 获取指定区域的数值
def parse_num_area(area, rgb):
    key = ""
    screenshot_area(area, "screenshot.png", rgb)
    content = parse_content("screenshot.png", "eng+chi_sim")
    if content:
        print(content)
        # 替换长横线
        content = content.replace("—", "-")
        content = content.replace("一 ", "-")
        print(content)

        # 从content获取带正负号的数值
        pattern = r"-?\d+.?\d+"
        nums = re.findall(pattern, content, re.S)
        print(nums)

        if nums:
            # 将数组中的内容拼接成字符串
            key = "".join(nums)
    return key

# 获取指定区域中文
def parse_chi_area(area, rgb):
    key = ""
    screenshot_area(area, "screenshot.png", rgb)
    content = parse_content("screenshot.png")
    if content:
        # print(content)
        chi_obj = re.findall(r"[\u4e00-\u9fa5]+", content, re.S)
        if chi_obj:
            # 将数组中的内容拼接成字符串
            key = "".join(chi_obj)
    return key


# 获取多个位置的内容
def parse_chi_areas(areas):
    content = []
    for area in areas:
        key = parse_chi_area(area, (0, 0, 0))
        content.append(key)
    return content


# 每秒钟执行一次
while True:
    # content = parse_content_area((774, 638, 1171, 665))
    # content = parse_content_area((881, 363, 998, 386)) # 山前灵凤
    # key, value = parse_content_area((891, 170, 967, 199))  # 灵脉
    content = parse_chi_areas(((891, 170, 967, 199), (881, 363, 998, 386)))
    print(content)

    if content[0] == "灵脉":
        if content[1] == "当前灵凤":
            value_red = parse_num_area((774, 638, 1171, 665), (190, 86, 72))
            value_green = parse_num_area((774, 638, 1171, 665), (23, 119, 44))
            if not value_red and not value_green:
                pyautogui.click(789, 894)  # 遗忘
                time.sleep(0.5)

            if value_green :
                print("替换")
                pyautogui.click(1080, 894)  # 替换
            else:
                print("遗忘")
                pyautogui.click(789, 894)  # 遗忘
        else:
            print("召唤")
            pyautogui.click(936, 890)

    # content = parse_content_area((884, 879, 982, 909))
    # print(content)
    # time.sleep(1)

# tesseract img out -l chi_sim+eng --psm 6
