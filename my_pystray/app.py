from pystray import Icon, MenuItem, Menu
from PIL import Image
import time
import threading
import schedule


class TaskTray:
    def __init__(self, image):
        self.status = False

        # アイコンの画像
        image = Image.open(image)
        # 右クリックで表示されるメニュー
        menu = Menu(
            MenuItem('Task', self.do_task),
            MenuItem('Exit', self.stop_program),
        )

        self.icon = Icon(name='nameTray', title='titleTray', icon=image, menu=menu)

    def do_task(self):
        print('実行しました。')

    def run_schedule(self):
        # 5秒毎にタスクを実行する。
        schedule.every(5).seconds.do(self.do_task)
        # status が True である間実行する。
        while self.status:
            schedule.run_pending()
            time.sleep(1)

    def stop_program(self, icon):
        self.status = False

        # 停止
        self.icon.stop()

    def run_program(self):
        self.status = True

        # スケジュールの実行
        task_thread = threading.Thread(target=self.run_schedule)
        task_thread.start()

        # 実行
        self.icon.run()


if __name__ == '__main__':
    system_tray = TaskTray(image="app.jpg")
    system_tray.run_program()
