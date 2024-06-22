import pyautogui
import cv2
import numpy as np
import keyboard
import time
import pygetwindow as gw

# PyAutoGUI 설정
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# 이미지 파일 경로 설정
image_path = '1.png'

# 클릭할 좌표 설정 (절대 좌표)
coordinates = [(1229, 215), (1455, 317), (1229, 215), (1455, 317), (1229, 215), (1455, 317)]  # 변경된 좌표

# 특정 창 이름
window_title = '祖큡aster Online'

def click_coordinates(coordinates):
    for coord in coordinates:
        click_x, click_y = coord
        pyautogui.click(click_x, click_y)
        print(f'좌표 클릭: ({click_x}, {click_y})')
        time.sleep(0.2)  # 클릭 사이 딜레이

def find_and_click(image_path, coordinates):
    # 스크린샷 찍기
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # 이미지 파일 불러오기
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f'이미지 파일을 찾을 수 없습니다: {image_path}')
        return False
    
    # 이미지 서치
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    
    if len(loc[0]) > 0:
        print('이미지 찾음!')
        click_coordinates(coordinates)  # coordinates를 전달
        return True
    else:
        print('이미지 찾기 실패')
        return False

def get_window(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        return windows[0]
    else:
        print(f'{window_title} 창을 찾을 수 없습니다.')
        return None

def main():
    print('프로그램 시작. F9 키를 누르면 작동합니다.')
    
    while True:
        # F9 키가 눌리면 루프 시작
        if keyboard.is_pressed('F9'):
            print('F9 키 입력됨, 이미지 서치 및 클릭 시작.')
            while True:
                if find_and_click(image_path, coordinates):
                    time.sleep(2)  # 작업 후 대기 시간
                else:
                    time.sleep(1)  # 이미지 못 찾을 때 대기 시간
                
                # 프로그램 중지 (Page Down 키 누름) 체크
                if keyboard.is_pressed('page down'):
                    print('Page Down 키 입력됨, 프로그램 종료.')
                    break
            
            break  # F9 루프 종료 후 프로그램 종료

if __name__ == '__main__':
    main()
