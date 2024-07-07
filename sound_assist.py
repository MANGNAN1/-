import pyautogui
import cv2
import numpy as np
import keyboard
import time
import pygetwindow as gw
import logging
import winsound
import sys
import os

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# PyAutoGUI 설정
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# 실행 파일 경로와 이미지 파일 경로 설정
if getattr(sys, 'frozen', False):
    # 실행 파일에서 실행 중일 때
    current_path = sys._MEIPASS
else:
    # 스크립트에서 실행 중일 때
    current_path = os.path.abspath(os.path.dirname(__file__))

# 이미지 파일 경로
image_path = os.path.join(current_path, '1.png')
window_title = '겻큡aster Online'

# 이미지 파일이 존재하는지 확인
if not os.path.exists(image_path):
    logging.error(f'이미지 파일을 찾을 수 없습니다: {image_path}')
    sys.exit(1)

def find_image_and_alert(image_path, threshold=0.8):
    try:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            logging.error(f'이미지 파일을 찾을 수 없습니다: {image_path}')
            return False
        
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        
        if len(loc[0]) > 0:
            logging.info('이미지 찾음!')
            winsound.Beep(1000, 600)  # 주파수 1000Hz, 1초 동안 소리 재생
            return True
        else:
            logging.info('이미지 찾기 실패')
            return False
    except Exception as e:
        logging.error(f'find_image_and_alert에서 오류 발생: {e}')
        return False

def get_window(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            return windows[0]
        else:
            logging.error(f'{window_title} 창을 찾을 수 없습니다.')
            return None
    except Exception as e:
        logging.error(f'get_window에서 오류 발생: {e}')
        return None

def main():
    logging.info('프로그램 시작. F9 키를 누르면 작동합니다.')
    
    while True:
        if keyboard.is_pressed('F9'):
            logging.info('F9 키 입력됨, 이미지 서치 및 알림 시작.')
            while True:
                if find_image_and_alert(image_path):
                    time.sleep(2)
                else:
                    time.sleep(1)
                
                if keyboard.is_pressed('page down'):
                    logging.info('Page Down 키 입력됨, 프로그램 종료.')
                    break
            break

if __name__ == '__main__':
    main()
