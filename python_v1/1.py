import os, os.path
import sys
from telethon import TelegramClient, events
# from PySide6.QtCore import *
from PySide6.QtCore import QTimer
# from PySide6.QtGui import *
from PySide6.QtGui import Qt, QPainter, QPen, QPixmap
# from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QProgressBar, QHBoxLayout, QScrollArea, QMainWindow, QFileDialog
from functools import partial
import asyncio
from pygame import mixer
import pygame
from moviepy.editor import VideoFileClip
import time
import subprocess

api_id = ""
api_hash = ""
client = TelegramClient('anon', api_id, api_hash)

width = 0
height = 0
mouse = ''
max_size_file = 10**5
g_name = ''
limit = 5
if not os.path.isdir("./tel"):
    os.makedirs("./tel")
if not os.path.isdir("./user"):
    os.makedirs("./user")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

async def main(msg='', ch=0, file=False):
    global max_size_file, limit
    await client.start()
    await client.connect()
    if file:
        await client.send_file(ch, msg)
    elif msg :
        await client.send_message(ch,msg)
    f_user = open('./tel/user.txt','a+', encoding="utf-8")
    try:
        f_user.truncate(0)
    except:
        pass
    async for dialog in client.iter_dialogs():
        chat_id = dialog.id
        if dialog.is_user and dialog.unread_count:

            f=open(f"./tel/{chat_id}.txt", "w", encoding="utf-8")
            try:
                f.truncate(0)
            except:
                pass

            try:
                f_media=open(f"./tel/{chat_id}media.txt", "a+", encoding="utf-8")
            except:
                f_media=open(f"./tel/{chat_id}media.txt", "w", encoding="utf-8")
            
            try:
                open(f'./tel/{chat_id}.jpg')
            except:
                try:
                    await client.download_profile_photo(chat_id, file=f'./tel/{chat_id}')
                except:
                    pass
            async for message in client.iter_messages(dialog.id, limit=limit):
                try:
                    try:
                        if message.media is not None:
                            if message.file.size < max_size_file:
                                if str(chat_id) + '-' + str(message.id) not in open(f"./tel/{chat_id}media.txt", "r", encoding="utf-8").read():
                                    f_media.write(str(chat_id) + '-' + str(message.id) + '\n')
                                    await client.download_media(message=message,file=f'./tel/{chat_id}{message.id}')
                    except:
                        try:
                            if message.media is not None:
                                if message.file.size < max_size_file:
                                    # f_media.write(str(chat_id) + '-' + str(message.id) + '\n')
                                    await client.download_media(message=message,file=f'./tel/{chat_id}{message.id}')
                        except:
                            pass
                    try:
                        f.write(message.text + '\n')
                        f_user.write(str(chat_id) + '-' + dialog.name + '\n')
                    except:
                        pass
                except:
                    pass
    try:
        f_user.close()
        f.close()
        f_media.close()
    except:
            pass
try:
    client.start()
    directory = "tel"
    parent_dir = "./"
    path = os.path.join(parent_dir, directory)  
    os.mkdir(path) 
except:
    pass

@client.on(events.NewMessage)
async def my_event_handler(chat_id,event):
    global max_size_file, limit
    if event.is_private:
        f=open(f"./tel/{chat_id}.txt", "w", encoding="utf-8")
        try:
            f_media=open(f"./tel/{chat_id}media.txt", "a+", encoding="utf-8")
        except:
            f_media=open(f"./tel/{chat_id}media.txt", "w", encoding="utf-8")
        async for message in client.iter_messages(chat_id, limit=limit):
                    print(str(chat_id) + '-' + str(message.id) not in open(f"./tel/{chat_id}media.txt", "r", encoding="utf-8").read())
                    try:
                        try:
                            if message.media is not None:
                                if message.file.size < max_size_file:
                                    if str(chat_id) + '-' + str(message.id) not in open(f"./tel/{chat_id}media.txt", "r", encoding="utf-8").read():
                                        f_media.write(str(chat_id) + '-' + str(message.id) + '\n')
                                        await client.download_media(message=message,file=f'./tel/{chat_id}{message.id}')
                        except:
                            try:
                                if message.media is not None:
                                    if message.file.size < max_size_file:
                                        f_media.write(str(chat_id) + '-' + str(message.id) + '\n')
                                        await client.download_media(message=message,file=f'./tel/{chat_id}{message.id}')
                            except:
                                pass
                        try:
                            f.write(message.text + '\n')
                        except:
                            pass
                    except:
                        pass
                    
                
        f.close()
        f_media.close()


async def g_handler():
    global g_name
    if g_name:
        async for dialog in client.iter_dialogs():
            if g_name and g_name in dialog.name and dialog.unread_count:
                chat_id = str(dialog.id).replace('-','~')
                f_user = open('./tel/user.txt','a+', encoding="utf-8")
                f=open(f"./tel/{chat_id}.txt", "w", encoding="utf-8")
                try:
                    open(f'./tel/{chat_id}.jpg')
                except:
                    try:
                        await client.download_profile_photo(int(chat_id.replace('~','-')), file=f'./tel/{chat_id}')
                    except:
                        pass

                async for message in client.iter_messages(dialog.id, limit=10):
                        try:
                            f.write(message.text + '\n')
                            f_user.write(chat_id + '-' + dialog.name + '\n')
                            print('*****************************',chat_id)
                        except:
                            pass
                f.close()
                f_user.close()

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.counter = 0
        self.n = 100 
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)
    def initUI(self):
        # layout to display splash scrren frame
        layout = QVBoxLayout()
        self.setLayout(layout)
        # splash screen frame
        self.frame = QFrame()
        layout.addWidget(self.frame)
        # splash screen title
        self.title_label = QLabel(self.frame)
        self.title_label.setObjectName('title_label')
        self.title_label.resize(690, 120)
        self.title_label.move(0, 5) # x, y
        self.title_label.setText('Splash Screen')
        self.title_label.setAlignment(Qt.AlignCenter)
        # splash screen title description
        self.description_label = QLabel(self.frame)
        self.description_label.resize(690, 40)
        self.description_label.move(0, self.title_label.height())
        self.description_label.setObjectName('desc_label')
        self.description_label.setText('<b>Splash Screen PyQt-5</b>')
        self.description_label.setAlignment(Qt.AlignCenter)
        # splash screen pogressbar
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, 180) # self.description_label.y()+130
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)
        # spash screen loading label
        self.loading_label = QLabel(self.frame)
        self.loading_label.resize(self.width() - 10, 50)
        self.loading_label.move(0, self.progressBar.y() + 70)
        self.loading_label.setObjectName('loading_label')
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setText('Loading...')
    def loading(self):
        # set progressbar value
        self.progressBar.setValue(self.counter)
        # stop progress if counter
        # is greater than n and
        # display main window app
        if self.counter >= self.n:
            self.timer.stop()
            self.close()
            time.sleep(1)
            self.WindowApp = Widget()
            self.WindowApp.show()
        self.counter += 1


class Widget(QWidget):
    def __init__(self, parent=None):
        global width, height
        super(Widget, self).__init__(parent)
        width = self.screen().geometry().width()
        height = self.screen().geometry().height()
        
        
        # self.scroll.resize(int(0.526 * width), int(0.638 * height))
        # self.scroll.move(int(0.021 * width), int(0.169 * height))
        # self.setStyleSheet("background-color: #1917c6;")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.main_widget1 = QWidget()
        self.main_widget1.setStyleSheet("background-color: #0d0d0d;")
        self.main_widget2 = QWidget()
        self.main_widget2.setStyleSheet("background-color: #33373B;")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.main_widget1, 2)
        self.layout.addWidget(self.main_widget2, 5)

        self.setLayout(self.layout)

        button1 = QPushButton('Refresh', self.main_widget1)
        button1.move(int(0.04 * width), int(0.84 * height))
        button1.resize(int(0.18 * width), int(0.043 * height))
        button1.setStyleSheet("""QPushButton {background-color: #feff2d;font-size:24px}
                                QPushButton:pressed {
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #dadbde, stop: 1 #f6f7fa);
                                }""")
        button1.clicked.connect(self.show_contacts)
        button1.show()

        label1x = QLabel('Enter name of channel or group :', self.main_widget1)
        label1x.setStyleSheet(f'font-size: {int(0.0115 * width)}px;color: #fefffc')
        label1x.resize(int(0.2 * width), int(0.039 * height))
        label1x.move(int(0.005 * width), int(0.73 * height))
        # label1.setStyleSheet("""color: #fefffc """)
        label1x.show()

        self.edit_line11x = QLineEdit(self.main_widget1)
        self.edit_line11x.move(int(0.17 * width), int(0.73 * height))
        self.edit_line11x.resize(int(0.1 * width), int(0.039 * height))
        self.edit_line11x.textChanged.connect(self.group_name)
        self.edit_line11x.setStyleSheet("""color: #fff651 ;background-color: #001cfc""")
        self.edit_line11x.show()

        label1 = QLabel('Maximum File Size For Download: ', self.main_widget1)
        label1.setStyleSheet(f'font-size: {int(0.0115 * width)}px;color: #fefffc')
        label1.resize(int(0.22 * width), int(0.039 * height))
        label1.move(int(0.02 * width), int(0.79 * height))
        # label1.setStyleSheet("""color: #fefffc """)
        label1.show()

        self.edit_line11 = QLineEdit(self.main_widget1)
        self.edit_line11.move(int(0.19 * width), int(0.79 * height))
        self.edit_line11.resize(int(0.071 * width), int(0.039 * height))
        self.edit_line11.textChanged.connect(self.max_size)
        self.edit_line11.setStyleSheet("""color: #fff651 ;background-color: #001cfc""")
        self.edit_line11.show()

        ex = QLabel(self.main_widget1)
        ex.move(int(0.003* width), int(0.87 * height))
        ex.setStyleSheet('''border-image: url(''' + resource_path('./ex.png').replace('\\', '/') + ''')''')
        ex.resize(30, 30)
        ex.mousePressEvent = partial(self.ex)
        ex.show()       
        
    def ex(self, n):
        exit()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.5)
        painter.setBrush(Qt.blue)
        painter.setPen(QPen(Qt.blue))   
        painter.drawRect(self.rect())

    def max_size(self, n):
        global max_size_file
        try:
            max_size_file = eval(n)
        except:
            pass
    
    def group_name(self, n):
        global g_name
        try:
            g_name = n
        except:
            pass

    def show_contacts(self):

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.run_until_complete(g_handler())
        # loop.run_until_complete(delete_loading(loading, movie))

        f = open('./tel/user.txt', encoding="utf-8")
        usr = f.readlines() 
        f.close()
        num_usr = len(usr)
        self.scroll = QScrollArea(self.main_widget1)
        self.scroll.resize(int(0.2755 * width), int(0.7 * height))
        self.scroll.move(int(0.001 * width), int(0.001 * height))
        self.contact_win = QWidget(self.main_widget1)
        self.contact_win.resize(int(0.274 * width), int(num_usr * 0.065 * height))
        self.contact_win.move(int(0.021 * width), int(0.169 * height))
        j = 0
        check_list = list()
        for i in reversed(usr):
            if not i in check_list:
                check_list.append(i)
                prof = QLabel(self.contact_win)
                pix = QPixmap(resource_path('./tel/{}.jpg'.format(str(i).split('-')[0])).replace('\\', '/'))
                pix = pix.scaled(50, 50, Qt.KeepAspectRatio) 
                prof.setPixmap(pix)
                # prof.resize(int(0.046 * width), int(0.06 * height))
                prof.move(int(0.01 * width), int(j * 0.07 * height + 10))
                prof.mousePressEvent = partial(self.do_something, str(i).split('-')[0] + ".jpg", int(0.02 * width), int(j * 0.07 * height + 10))
                prof.show()

                button1 = QPushButton(str(i).split('-')[1].replace('\n',''), self.contact_win)
                button1.move(int(0.06 * width), int(j * 0.07 * height + 10))
                button1.resize(int(0.18 * width), int(0.05 * height))
                button1.setStyleSheet("""QPushButton {background-color: #000592; color: yellow;font-size:20px;}
                                        QPushButton:pressed {
                                        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                    stop: 0 #dadbde, stop: 1 #f6f7fa);
                                        }""")
                button1.clicked.connect(partial(self.show_message, str(i).split('-')[0]))
                button1.show()
                j += 1
        self.scroll.setWidget(self.contact_win)
        self.scroll.show()
        
    def show_message(self, chat_id):
        if '~' in chat_id:
            chat_id = int(chat_id.replace('~','-'))
        else:
            chat_id = int(chat_id)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(my_event_handler(chat_id, events.NewMessage.Event))
        f=open(f"./tel/{chat_id}.txt", "r", encoding="utf-8")
        text = f.read()
        try:
            self.label_message.close()
            self.send_edit.close()
            self.send_label.close()
            self.send_button.close()
            self.window_mesg.close()
            self.window_med.close()
            self.main_window_mesg.close()
        except:
            pass
        
        self.main_window_mesg = QWidget(self.main_widget2)
        self.main_window_mesg.resize(int(0.7 * width), int(0.89 * height))
        self.main_window_mesg.show()
        self.window_mesg = QWidget(self.main_window_mesg)
        self.window_mesg.resize(int(0.528 * width), int(0.86 * height + len(text.split('\n')) * 0.035 * height))
        self.window_med = QWidget(self.main_window_mesg)
        self.window_med.resize(int(0.1 * width), int(0.85 * height))

        scroll = QScrollArea(self.main_window_mesg)
        scroll.resize(int(0.495 * width), int(0.86 * height))
        

        scroll2 = QScrollArea(self.main_window_mesg)
        scroll2.resize(int(0.49 * width), int(0.86 * height))

        self.layout = QHBoxLayout()
        self.layout.addWidget(scroll2, 1)
        self.layout.addWidget(scroll, 4)
        self.main_window_mesg.setLayout(self.layout)
        

        path = f"./tel/"
        dir_list = os.listdir(path)
        new_list = list()
        try:
            for i in self.img_list:
                i.close()
        except:
            pass
        self.img_list = list()
        for i in dir_list:
            if str(chat_id) in i and '.txt' not in i:
                new_list.append(i)
        self.window_med.resize(int(0.1 * width), int(0.57 * height + len(new_list) * 0.09 * height))
        for i in range(len(new_list)):
            if '.jpg' in new_list[i] or '.png' in new_list[i]:
                img = QLabel(self.window_med)
                # pix = QPixmap(f'./tel/{new_list[i]}')
                # pix = pix.scaled(75, 75, Qt.KeepAspectRatio)
                img.move(int(0.003* width), int(0.013 * height + i * 0.10 * height))
                img.setStyleSheet('''border-image: url(''' + resource_path('./tel/').replace('\\', '/') + new_list[i] + ''')''')
                img.resize(75, 75)
                img.mousePressEvent = partial(self.do_something, new_list[i], int(0.003* width), int(0.013 * height + i * 0.07 * height))
                img.show()
                self.img_list.append(img)
            if '.oga' in new_list[i] or '.mp3' in new_list[i]:
                voice = QPushButton(self.window_med)
                voice.move(int(0.003* width), int(0.013 * height + i * 0.10 * height))
                voice.setStyleSheet('''border-image: url(''' + resource_path('./p.png').replace('\\', '/') + ''')''')
                voice.resize(80, 80)
                voice.clicked.connect(partial(self.do_somethong2, new_list[i], voice))
                voice.show()
            if '.mp4' in new_list[i]:
                video = QPushButton(self.window_med)
                video.move(int(0.003* width), int(0.013 * height + i * 0.10 * height))
                video.setStyleSheet('''border-image: url(''' + resource_path('./v3.png').replace('\\', '/') + ''')''')
                video.resize(75, 75)
                video.clicked.connect(partial(self.do_somethong3, new_list[i]))
                video.show()
            if '.pdf' in new_list[i] :
                pdf = QPushButton(self.window_med)
                pdf.move(int(0.003* width), int(0.013 * height + i * 0.10 * height))
                pdf.setStyleSheet('''border-image: url(''' + resource_path('./pdf.png').replace('\\', '/') + ''')''')
                pdf.resize(75, 75)
                pdf.clicked.connect(partial(self.do_somethong4, new_list[i]))
                pdf.show()


        self.label_message = QLabel(text, self.window_mesg)
        # path = r'E:/music/Music/03. Darkside.mp3'
        # url = bytearray(QUrl.fromLocalFile(path).toEncoded()).decode()
        # text = "<a href={}>Reference Link> </a>".format(url)
        # self.label_message.setText(text)
        self.label_message.setStyleSheet(f'font-size: {int(0.015 * width)}px;color : #FFF8C4')
        self.label_message.resize(int(0.525 * width), int(0.8 * height + len(text.split('\n')) * 0.035 * height))
        # self.label_message.move(int(0.008 * width), int(0.009 * height))
        self.label_message.setAlignment(Qt.AlignLeft)
        self.label_message.setOpenExternalLinks(True)
        self.label_message.setWordWrap(True)
        self.label_message.show()

        self.send_edit = QLineEdit(self.main_window_mesg)
        self.send_edit.move(int(0.19 * width), int(0.81 * height))
        self.send_edit.resize(int(0.44 * width), int(0.06 * height))
        self.send_edit.setStyleSheet(f'color:#ffffff; background-color: #5c0076;')
        self.send_edit.textChanged.connect(self.message_will_send)
        self.send_edit.show()

        self.send_button = QPushButton(self.main_window_mesg)
        # pix = QPixmap('./send.png')
        # pix = pix.scaled(75, 75, Qt.KeepAspectRatio)
        self.send_button.move(int(0.632 * width), int(0.793 * height))
        self.send_button.setStyleSheet('''border-image: url(''' + resource_path('./send.png').replace('\\', '/') + ''')''')
        self.send_button.resize(65, 65)
        self.send_button.clicked.connect(partial(self.send_message_to_user, chat_id))
        self.send_button.show()

        self.brw_btn1 = QPushButton( self.main_window_mesg)
        self.brw_btn1.setStyleSheet('''border-image: url(''' + resource_path('./lin.png').replace('\\', '/') + ''')''')
        self.brw_btn1.resize(40, 40)
        self.brw_btn1.move(int(0.15 * width), int(0.818 * height))
        self.brw_btn1.clicked.connect(partial(self.browse_xlsx_1, chat_id))
        self.brw_btn1.show()

        scroll.setWidget(self.window_mesg)
        scroll.show()
        scroll2.setWidget(self.window_med)
        scroll2.show()

    def browse_xlsx_1(self, chat_id):
        MainWindow = QMainWindow()
        self.loc1 = showDialog(MainWindow)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(self.loc1, chat_id, file=True))

    def send_message_to_user(self, chat_id):
        # asyncio.run(run())
        # asyncio.run(main())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(self.message_, chat_id))

        pre_text = self.label_message.text()
        self.label_message.setText(pre_text + '\n' + self.message_)
        self.message_ = ''
        self.send_edit.clear()

    def message_will_send(self, n):
        self.message_ = n

    def mouseReleaseEvent(self, e):
        global mouse
        mouse = 'release'
        try:
            self.image.close()
        except:
            pass

    def do_something(self, chat_id, x, y, event):
        global mouse
        if event.button() == Qt.LeftButton:
            mouse = 'press'
            self.image = QLabel(self.main_widget2)
            # self.show_error.setText('successfully')
            pix = QPixmap(f'./tel/{chat_id}')
            pix = pix.scaled(600, 800,Qt.KeepAspectRatio) 
            self.image.setPixmap(pix)
            # self.show_error.setStyleSheet(f'font-size: {int(0.02 * width)}px'
            #                                 f'; color:black;'
            #                                 f'background: red;border-radius: 10px;'
            #                                 f'font: italic;')
            self.image.move(int(0.1 * width), int(0.02 * height))
            
            # self.show_error.setAlignment(Qt.AlignLeft)
            self.image.show()

    def do_somethong2(self, dirf, voice):
        filename = './tel/' + dirf
        mixer.init()
        if mixer.music.get_busy():
            mixer.music.load(filename)
            mixer.music.set_volume(0.7)
            mixer.music.pause()
            voice.setStyleSheet('''border-image: url(''' + resource_path('./p.png').replace('\\', '/') + ''')''')
            voice.resize(80, 80)
        else:
            mixer.music.load(filename)
            mixer.music.set_volume(0.7)
            mixer.music.play()
            voice.setStyleSheet('''border-image: url(''' + resource_path('./pd.png').replace('\\', '/') + ''')''')
            voice.resize(80, 80)

    def do_somethong3(self, dirf):
        filename = './tel/' + dirf
        clip = VideoFileClip(filename)
        clip.preview()
        
        pygame.quit()
        # video = cv2.VideoCapture(filename)
        # success, video_image = video.read()
        # fps = video.get(cv2.CAP_PROP_FPS)

        # window = pygame.display.set_mode(video_image.shape[1::-1])
        # pygame.display.set_caption('video')
        # clock = pygame.time.Clock()

        # run = success
        # while run:
        #     clock.tick(fps)
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             run = False
            
        #     success, video_image = video.read()
        #     if success:
        #         video_surf = pygame.image.frombuffer(
        #             video_image.tobytes(), video_image.shape[1::-1], "BGR")
        #     else:
        #         run = False
        #     window.blit(video_surf, (0, 0))
        #     pygame.display.flip()

        # pygame.quit()

    def do_somethong4(self, dirf):
        subprocess.Popen([dirf],shell=True)

def showDialog(self):
        MainWindow = QMainWindow()
        fname, _ = QFileDialog.getOpenFileName(MainWindow, 'Open file', "", 'All files (*.*)')
        return fname


if __name__ == "__main__":
    app = QApplication()
    w = Widget()
    w.setWindowState(Qt.WindowMaximized)
    # w.resize(1000,700)
    width = w.screen().geometry().width()
    height = w.screen().geometry().height()


    w.show()
    with open('style.qss', 'w') as f:
        f.write("""
        QListWidget {
            color: #FFFFFF;
            background-color: #33373B;
            }

            QListWidget::item {
            height: 50px;
            }

            QListWidget::item:selected {
            background-color: #2ABf9E;
            }

            /*QLabel {*/
            /*    background-color: #FFFFFF;*/
            /*    qproperty-alignment: AlignCenter*/
            /*}*/

            QTreeWidget {
            color: #FFFFFF;
            background-color: #33373B;
            font-size: 18px;
            }

            QTreeWidget::item:selected {
            background-color: #2ABf9E;
            }

            QLabel{
            color: #33373B;
            background-color: None;
            }

            QLineEdit {
            border: 2px solid gray;
            border-radius: 10px;
            padding: 0 8px;
            background: greenyellow;
            selection-background-color: darkgray;
            font-size: 18px;
            }

            QLineEdit[echoMode="2"] {
            lineedit-password-character: 9679;
            }

            QLineEdit:read-only {
            background: lightblue;
            }

            QPushButton {
            border: 2px solid #8f8f91;
            border-radius: 10px;
            background-color: #2ABf9E;
            min-width: 50px;
            }

            QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #dadbde, stop: 1 #f6f7fa);
            }

            QPushButton:flat {
            border: none; /* no border for a flat push button */
            }

            QPushButton:default {
            border-color: navy; /* make the default button prominent */
            }

            QScrollBar:vertical {
            border: blue;
            background: orangered;
            border-radius: 10px;
            }

            QScrollBar:horizontal {
            border: blue;
            background: blue;
            border-radius: 10px;
            }
        """)

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    
    sys.exit(app.exec())
    
    
