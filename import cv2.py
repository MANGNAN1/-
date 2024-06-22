import cv2
import pyautogui
import numpy as np
import os
import keyboard  # keyboard 모듈 임포트
import time
import pygetwindow as gw  # pygetwindow 모듈 임포트

# 특정 창의 제목
target_window_title = "祖큡aster Online"

# 특정 창에서 클릭할 좌표들 (창 내부 좌표)
click_points = [
    (1001, 179),
    (772, 70)
]

def find_and_press_keys(image_filename, target_window):
    # 이미지 파일의 경로
    image_path = os.path.join(os.path.dirname(__file__), image_filename)
    
    # 템플릿 이미지 로드 (흑백으로 변환)
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Cannot find image file: {image_path}")

    w, h = template.shape[::-1]

    print(f"스크립트를 시작합니다. 이미지 '{image_filename}'를 찾습니다.")

    while True:
        # 특정 창이 활성화되었는지 확인
        if target_window.isActive:
            # 창의 위치와 크기 얻기
            window_rect = target_window._getWindowRect()
            window_x, window_y, window_width, window_height = window_rect

            # 이미지 검색을 위해 창 내부 영역 캡처
            screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)  # RGB를 흑백으로 변환

            # 화면에서 이미지 찾기
            res = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            # 이미지를 찾았을 때 동작
            if len(loc[0]) > 0:
                for pt in zip(*loc[::-1]):
                    # 이미지의 중심을 클릭 포인트로 사용
                    center_x = window_x + pt[0] + w // 2
                    center_y = window_y + pt[1] + h // 2

                    # 키 입력: 순서대로 1, F1, 3 입력 (간격 1초)
                    pyautogui.typewrite(['1', 'f1', '3'], interval=1)

                    print(f"이미지 '{image_filename}'를 찾았습니다. 키 입력을 완료했습니다.")

                    # 클릭 좌표 순서대로 클릭
                    perform_click_sequence(target_window)

        # 페이지다운(PgDn) 버튼이 눌리면 스크립트 종료
        if keyboard.is_pressed('pagedown'):
            print("사용자에 의해 프로그램이 종료되었습니다.")
            break

def perform_click_sequence(target_window):
    # 특정 창에서 클릭할 좌표들을 순서대로 클릭
    if target_window.isActive:
        window_rect = target_window._getWindowRect()
        window_x, window_y, _, _ = window_rect
        
        for point in click_points:
            click_x, click_y = point
            pyautogui.click(window_x + click_x, window_y + click_y)
            time.sleep(1)  # 클릭 후 잠시 대기

def main():
    print(f"프로그램을 시작합니다. '{target_window_title}' 창에서만 동작합니다. F9를 누르면 이미지 검색을 시작합니다.")

    # 특정 창 인식
    target_window = gw.getWindowsWithTitle(target_window_title)
    if len(target_window) == 0:
        raise Exception(f"Could not find window with title '{target_window_title}'")
    elif len(target_window) > 1:
        raise Exception(f"Found multiple windows with title '{target_window_title}'")
    else:
        target_window = target_window[0]

    while True:
        if keyboard.is_pressed('f9'):
            image_filename = "1.png"  # 검색할 이미지 파일명을 '1.png'로 설정
            find_and_press_keys(image_filename, target_window)
            print("이미지 검색이 완료되었습니다. F9를 다시 눌러 재시작할 수 있습니다.")
            time.sleep(1)  # 잠시 대기 후 다시 시작할 수 있도록 함

if __name__ == "__main__":
    main()
