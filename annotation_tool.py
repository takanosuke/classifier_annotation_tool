from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageOps
import os
import json
#----------------------------------------------------------------------
# 設定項目
images_dir = ".\\images" # 画像フォルダのパス
json_path  = ".\\result.json" # 出力(json)ファイルのパス
classes = ["犬","猫","鳥","猿","羊","狼","狸","不明"] # 分類するクラス
image_width = 800 # 表示画像の幅
image_height = 450 # 表示画像の高さ
#----------------------------------------------------------------------
class MainWindow():
    #----------------
    def __init__(self, main, args):
        self.current_image_num = 0 # 開始画像位置の設定
        self.main = main
        self.images_dir = args["images_dir"]
        self.json_path = args["json_path"]
        self.classes = args["classes"]
        self.image_width = args["width"]
        self.image_height = args["height"]
        self.images_list = os.listdir(self.images_dir)
        self.images_num = len(self.images_list)
        self.img = []
        self.kyboard_str = "123456789qwertyuiopasdfghjklzxcvbnm"
        self.init_window()
        self.init_shortcuts()
    #----------------
    def init_window(self):
        # フォントの設定
        font_label_class = font.Font(size=20, weight='bold')
        font_label_index = font.Font(size=15)
        # タイトルの設定
        self.main.title(u"アノテーションツール")
        # 画像を表示するキャンバスを作る
        self.canvas = Canvas(self.main,width=self.image_width,height=self.image_height)
        self.canvas.grid(row=0, column=0, columnspan=7, rowspan=1)
        # 次の画像を表示するボタン
        self.button_next = Button(
            self.main, text="Next (→)", command=self.onNextButton, height=3)
        self.button_next.grid(row=2, column=5, pady=10, sticky='nsew')
        self.button_back = Button(
            self.main, text="Back (←)", command=self.onBackButton, height=3)
        self.button_back.grid(row=2, column=1, pady=10, sticky='nsew')
        # クラスを決定するボタン
        self.button_class = []
        for i, c in enumerate(self.classes):
            key = self.kyboard_str[i] if i < 35 else ""
            self.button_class.append(Button(self.main, text="{} ({})".format(c,key), command=self.labeling(class_num=i), width=10))
            self.button_class[i].grid(row=(i//7)+3, column=i%7, padx=5, pady=10, sticky='nsew')
        # ラベルの内容の初期化
        self.message_image_index = StringVar()
        self.message_image_class = StringVar()
        self.set_message()
        # クラスを表示するラベル
        self.label_image_class = Label(self.main, textvariable=self.message_image_class, width=50, font=font_label_class, background='#CCDDDD')
        self.label_image_class.grid(row=1, columnspan=7)
        # 現在の画像番号を表示するラベル
        self.label_image_index = Label(self.main, textvariable=self.message_image_index, font=font_label_index)
        self.label_image_index.grid(row=2, column=3, pady=10, sticky='nsew')
        # 最初の画像をセット
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.set_image()
    def init_shortcuts(self):
        self.main.focus_set()
        self.main.bind('<Key-Right>', self.onNextButton)
        self.main.bind('<Key-Left>', self.onBackButton)
        for i in list(range(len(self.button_class))):
            if i < 35:
                self.main.bind("<Key-{}>".format(self.kyboard_str[i]), self.labeling(i))
    def set_message(self):
        self.message_image_index.set("{}/{}".format(str(self.current_image_num+1),str(self.images_num)))
        self.message_image_class.set("{}".format(self.get_class_name(self.images_list[self.current_image_num])))
    def set_image(self,e=None):
        img = Image.open(os.path.join(self.images_dir,self.images_list[self.current_image_num]))
        img = img.resize((self.image_width,self.image_height), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img)
    def get_class_name(self, img_path):
        data = self.load_json()
        if img_path in data:
            return self.classes[data[img_path]]
        else:
            return "No Label"
    def onNextButton(self,e=None):
        # 一つ進む
        self.current_image_num += 1
        # 最初の画像に戻る
        if self.current_image_num == self.images_num:
            self.current_image_num = 0
        # 表示画像を更新
        self.set_image()
        self.set_message()
    def onBackButton(self,e=None):
        # 一つ戻る
        self.current_image_num -= 1
        # 最後の画像へ
        if self.current_image_num == -1:
            self.current_image_num = self.images_num - 1
        # 表示画像を更新
        self.set_image()
        self.set_message()
    def labeling(self, class_num):
        def x(e=None):
            img_path =self.images_list[self.current_image_num]
            self.update_json(img_path, class_num)
            self.set_message()
        return x
    def load_json(self):
        data = {}
        try:
            data = json.load(open(self.json_path,'r'))
        except json.JSONDecodeError as e:
            pass
        except FileNotFoundError as e:
            with open(self.json_path, 'w'):
                pass
        return data
    def update_json(self,img_path, class_num):
        data = self.load_json()
        data[img_path] = class_num
        json.dump(data, open(self.json_path,'w'),indent=4)
#----------------------------------------------------------------------

root = Tk()
args = {"images_dir":images_dir, "json_path":json_path, "classes":classes, "width":image_width, "height":image_height}
MainWindow(root,args)
root.mainloop()