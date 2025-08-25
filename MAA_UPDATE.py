import time
import win32gui
import win32con
import win32api
import comtypes
import comtypes.client

# UI Automation常量
UIA_ControlTypePropertyId = 30003
UIA_NamePropertyId = 30005
UIA_ButtonControlTypeId = 50000

# 初始化COM
comtypes.CoInitialize()
# 获取UI Automation客户端
UIAutomationClient = comtypes.client.GetModule('UIAutomationCore.dll')
IUIAutomation = comtypes.client.CreateObject(
    '{ff48dba4-60ef-4201-aa87-54103eef594e}',  # CUIAutomation的CLSID
    interface=UIAutomationClient.IUIAutomation
)

def find_window_startswith(prefix):
    """查找以指定前缀开头的窗口"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text.startswith(prefix):
                windows.append((hwnd, window_text))
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def get_button_position_by_text(hwnd, text):
    """通过文字查找按钮位置"""
    # 获取窗口的UI Automation元素
    element = IUIAutomation.ElementFromHandle(hwnd)
    
    # 创建条件：查找名称包含指定文本的按钮控件
    name_condition = IUIAutomation.CreatePropertyCondition(
        UIA_NamePropertyId, text
    )
    button_condition = IUIAutomation.CreatePropertyCondition(
        UIA_ControlTypePropertyId, UIA_ButtonControlTypeId
    )
    # 组合条件：名称匹配且为按钮类型
    condition = IUIAutomation.CreateAndCondition(
        name_condition, button_condition
    )
    
    # 在窗口内查找匹配的控件
    button_element = element.FindFirst(
        UIAutomationClient.TreeScope_Descendants, condition
    )
    
    if button_element:
        # 获取控件的边界矩形
        rect = button_element.CurrentBoundingRectangle
        # 计算中心点
        x = (rect.left + rect.right) // 2
        y = (rect.top + rect.bottom) // 2
        return (x, y)
    else:
        # 尝试更宽松的查找条件 - 只根据名称查找
        name_only_condition = IUIAutomation.CreatePropertyCondition(
            UIA_NamePropertyId, text
        )
        any_element = element.FindFirst(
            UIAutomationClient.TreeScope_Descendants, name_only_condition
        )
        
        if any_element:
            rect = any_element.CurrentBoundingRectangle
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2
            return (x, y)
    return None

def main():
    print("MAA窗口自动化点击程序")
    print("========================")
    
    # 检查是否存在以"MAA"开头的窗口
    maa_windows = find_window_startswith("MAA")
    
    if not maa_windows:
        print("未找到以'MAA'开头的窗口，请确保窗口已打开")
        return
    
    print(f"找到 {len(maa_windows)} 个以'MAA'开头的窗口")
    # 使用第一个找到的窗口
    hwnd, title = maa_windows[0]
    print(f"使用窗口: {title}")
    
    # 激活主窗口
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    
    # 获取窗口位置和大小
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    
    print(f"窗口位置: ({x}, {y}), 大小: ({width} x {height})")
    
    # 定义按钮及其默认位置
    buttons = {
        "设置": (x + 699, y + 43),
        "更新设置": (x + 68, y + 465),
        "资源更新": (x + 570, y + 401)
    }
    
    # 依次处理每个按钮
    for button_text, default_pos in buttons.items():
        print(f"\n准备点击'{button_text}'按钮")
        
        # 尝试通过文字获取按钮位置
        button_pos = get_button_position_by_text(hwnd, button_text)
        
        if button_pos is None:
            button_pos = default_pos
            print(f"使用预设位置: {button_pos}")
        else:
            print(f"找到按钮位置: {button_pos}")
        
        # 移动鼠标到按钮位置
        win32api.SetCursorPos(button_pos)
        time.sleep(0.1)
        
        # 点击按钮
        print(f"正在点击'{button_text}'按钮...")
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, button_pos[0], button_pos[1], 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, button_pos[0], button_pos[1], 0, 0)
        
        # 等待1秒钟
        time.sleep(1)
    
    print("所有操作已完成")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")
        print("请确保已安装所需依赖库:")
        print("pip install pywin32 comtypes")