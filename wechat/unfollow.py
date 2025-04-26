# 在屏幕指定位置右键点击

import pyautogui
import time

def unfollow_wechat_contact():
    """
    自动执行微信取消关注联系人的操作
    
    操作步骤：
    1. 在指定位置右键点击
    2. 等待菜单出现并点击相应选项
    3. 确认取消关注操作
    """
    # 指定屏幕位置
    position = (155, 169)

    # 右键点击
    pyautogui.rightClick(position[0], position[1])

    # 等待菜单出现
    time.sleep(0.2)

    # 点击取消关注选项
    pyautogui.moveTo(207, 262)
    pyautogui.click()

    # 等待确认对话框出现
    time.sleep(0.2)

    # 点击确认按钮
    pyautogui.moveTo(1293, 816)
    pyautogui.click()

    # 等待1秒
    time.sleep(0.2)

if __name__ == "__main__":
    # 给用户5秒时间切换到正确的窗口
    print("请在5秒内切换到微信窗口...")
    for i in range(1000):  
        unfollow_wechat_contact()








