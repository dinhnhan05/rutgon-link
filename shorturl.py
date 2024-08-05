import requests
import os
import time
from datetime import datetime
from termcolor import colored

HISTORY_FILE_PATH = '/sdcard/download/duanpython/link_history.txt'

os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    banner = """
     __        _______ _     ____ ___  __  __ _____ 
    \\ \\      / / ____| |   / ___/ _ \\|  \\/  | ____|
     \\ \\ /\\ / /|  _| | |  | |  | | | | |\\/| |  _|  
      \\ V  V / | |___| |__| |__| |_| | |  | | |___ 
       \\_/\\_/  |_____|_____\\____\\___/|_|  |_|_____|
    """
    
    info_text = """
    Link Shortener Tool
    Phiên bản: v1.0
    Admin: Nguyễn Đình Nhân
    Contact: t.me/kiryosdinhnhan
    """

    border = '═' * (max(len(line) for line in info_text.split('\n')) + 4)
    
    delay = 0.04

    clear_screen()
    for line in banner.split('\n'):
        print(colored(line, 'cyan'))
        time.sleep(delay)
        
    print(colored(border, 'yellow'))
    for line in info_text.split('\n'):
        print(colored(f'║ {line.ljust(len(border) - 4)} ║', 'yellow'))
    print(colored(border, 'yellow'))
    time.sleep(0.4)

    print("Sử dụng lệnh 'help' để xem danh sách lệnh 📚")
    time.sleep(0.5)

def show_help():
    help_text = """
    {0}{1}
    help - Hiện danh sách lệnh
    short <link> - Rút gọn link
    history - Hiện danh sách link đã rút gọn từ file txt đã lưu
    exit - Thoát tool
    """.format(
        colored("Danh sách các lệnh:", "red"),
        ""
    )
    print(help_text)

def shorten_url(link_to_shorten):
    try:
        api_url = f'http://tinyurl.com/api-create.php?url={link_to_shorten}'
        response = requests.get(api_url)
        
        if response.status_code == 200:
            short_url = response.text
            print(f'Link đã được rút gọn: {short_url}')
            
            with open(HISTORY_FILE_PATH, 'a') as file:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f'Thời gian: {current_time} - Link gốc: {link_to_shorten} - Link đã rút gọn: {short_url}\n')
        else:
            print('Có lỗi xảy ra, vui lòng kiểm tra đã đúng định dạng link chưa!?')
    except Exception as e:
        print(f'Đã xảy ra lỗi: {e}')

def show_history():
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as file:
            history = file.read()
        if history:
            print(f'Lịch sử các link đã rút gọn:\n{history}')
        else:
            print('Chưa có link nào được rút gọn.')
    else:
        print('Chưa có link nào được rút gọn.')

def main():
    show_banner()
    while True:
        command = input(colored("=> Nhập lệnh: ", 'light_green', attrs=["bold"])).strip()
        
        if command == 'help':
            show_help()
        elif command.startswith('short'):
            parts = command.split(' ', 1)
            if len(parts) == 1:
                print("Vui lòng thêm link đằng sau lệnh 'short'. Ví dụ: short https://example.com")
            else:
                link_to_shorten = parts[1].strip()
                if link_to_shorten:
                    shorten_url(link_to_shorten)
                else:
                    print("Vui lòng thêm link đằng sau lệnh 'short'. Ví dụ: short https://example.com")
        elif command == 'history':
            show_history()
        elif command == 'exit':
            print("Thông báo❗Đã dừng tool, cảm ơn đã sử dụng tool.")
            break
        else:
            print("Lệnh không hợp lệ. Vui lòng thử lại.")

if __name__ == '__main__':
    main()
