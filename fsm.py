from sqlite3 import Row
from symbol import term
from transitions.extensions import GraphMachine
from utils import send_text_message,send_button_message, send_image_message,types,info,types,weakness,id,fast_moves,main_moves,isChinese
from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import pandas as pd
from opencc import OpenCC
import re

#global variable
game=""
name=""

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def is_going_to_pkm_input(self,event):
        return True

    def on_enter_pkm_input(self,event):
        send_text_message(event.reply_token,"輸入想查詢的寶可夢名稱或者\n輸入fsm查看狀態圖")

    def is_going_to_fsm_graph(self,event):
        text = event.message.text
        if  (text == 'fsm'):
            return True
        return False

    def on_enter_fsm_graph(self,event):
        send_image_message(event.reply_token, 'https://ppt.cc/faAJjx@.png')
        self.go_back()

    def is_going_to_greeting(self, event):
        global name
        name = event.message.text
        return isChinese(name)
    
    def on_enter_greeting(self,event):
        title = '輸入遊戲版本'
        text = '朱紫 或者 Pokemon_GO'
        btn = [
                MessageTemplateAction(
                    label = '朱紫',
                    text = '朱紫'
                    ),
                MessageTemplateAction(
                    label = 'Pokemon Go',
                    text = 'Pokemon Go'
                    )
            ]
        url = 'https://ppt.cc/f0e7Yx@.png'
        send_button_message(event.reply_token, title, text, btn, url)
        
    def is_going_to_scarlet_violet(self,event):
        text = event.message.text
        if  (text == '朱紫'):
            return True
        return False

    def is_going_to_pokemon_go(self,event):
        text = event.message.text
        if  text == 'Pokemon Go':
            return True
        return False

    def on_enter_scarlet_violet(self,event):
        title = '輸入要查詢的內容'
        text = '要查詢甚麼呢'
        btn = [
                MessageTemplateAction(
                    label = '太晶戰',
                    text = '太晶戰'
                    ),
                MessageTemplateAction(
                    label = '屬性',
                    text = '屬性'
                    ),
                MessageTemplateAction(
                    label = '弱點',
                    text = '弱點'
                    ),
                MessageTemplateAction(
                    label = '效果絕佳',
                    text = '效果絕佳'
                    ),
            ]
        url = 'https://p2.bahamut.com.tw/B/2KU/39/8c604ef6167f002f06dd3ab5b91iynn5.JPG?v=1667291433638'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_pokemon_go(self,event):
        title = '輸入要查詢的內容'
        text = '要查詢甚麼呢'
        btn = [
                MessageTemplateAction(
                    label = '招式',
                    text = '招式'
                    ),
                MessageTemplateAction(
                    label = '屬性',
                    text = '屬性'
                    ),
                MessageTemplateAction(
                    label = '弱點',
                    text = '弱點'
                    ),
                MessageTemplateAction(
                    label = '效果絕佳',
                    text = '效果絕佳'
                    ),    
            ]
        url = 'https://lh3.googleusercontent.com/sj2boAS_HdWprBMjJkbJxOtR4V7P89q8kk7pqX35hi-QN1JfFuJBXnfnqo1pOB0CYbRJRXpm2PApAxhyRRgCI0-vOwNVQAbWBffWwYKEs9zx=s0'
        send_button_message(event.reply_token, title, text, btn, url)

    
    def is_going_to_battle(self,event):
        text = event.message.text
        if  (text == '太晶戰'):
            return True
        return False

    def on_enter_battle(self,event):
        send_text_message(event.reply_token,"https://gamewith.jp/pokemon-sv/article/show/375162")
        self.go_back()

    def is_going_to_type(self,event):
        text = event.message.text
        if  (text == '屬性'):
            return True
        return False

    def on_enter_type(self,event):
        global name
        pkm_type = types(name)
        pkm_type = OpenCC('s2t').convert(pkm_type)
        send_text_message(event.reply_token,pkm_type)
        self.go_back()

    def is_going_to_weakness(self,event):
        text = event.message.text
        if  (text == '弱點'):
            return True
        return False
    
    def on_enter_weakness(self,event):
        global name
        pkm_type = types(name)
        pkm_type = OpenCC('s2t').convert(pkm_type)
        row = 0
        if pkm_type == "一般":
            row = 0
        elif pkm_type == "火":
            row = 1
        elif pkm_type == "水":
            row = 2
        elif pkm_type == "草":
            row = 3
        elif pkm_type == "電":
            row = 4
        elif pkm_type == "格鬥":
            row = 5
        elif pkm_type == "毒":
            row = 6
        elif pkm_type == "地面":
            row = 7
        elif pkm_type == "飛行":
            row = 8
        elif pkm_type == "超能力":
            row = 9
        elif pkm_type == "蟲":
            row = 10
        elif pkm_type == "岩石":
            row = 11
        elif pkm_type == "幽靈":
            row = 12
        elif pkm_type == "冰":
            row = 13
        elif pkm_type == "龍":
            row = 14
        elif pkm_type == "惡":
            row = 15
        elif pkm_type == "鋼":
            row = 16
        elif pkm_type == "妖精":
            row = 17
        df = pd.read_excel("屬性克制表.xlsx")
        weak = df.at[row,"弱點"]
        send_text_message(event.reply_token,weak)
        self.go_back()

    def is_going_to_good_at(self,event):
        text = event.message.text
        if  (text == '效果絕佳'):
            return True
        return False
    
    def on_enter_good_at(self,event):
        global name
        pkm_type = types(name)
        pkm_type = OpenCC('s2t').convert(pkm_type)
        row = 0
        if pkm_type == "一般":
            row = 0
        elif pkm_type == "火":
            row = 1
        elif pkm_type == "水":
            row = 2
        elif pkm_type == "草":
            row = 3
        elif pkm_type == "電":
            row = 4
        elif pkm_type == "格鬥":
            row = 5
        elif pkm_type == "毒":
            row = 6
        elif pkm_type == "地面":
            row = 7
        elif pkm_type == "飛行":
            row = 8
        elif pkm_type == "超能力":
            row = 9
        elif pkm_type == "蟲":
            row = 10
        elif pkm_type == "岩石":
            row = 11
        elif pkm_type == "幽靈":
            row = 12
        elif pkm_type == "冰":
            row = 13
        elif pkm_type == "龍":
            row = 14
        elif pkm_type == "惡":
            row = 15
        elif pkm_type == "鋼":
            row = 16
        elif pkm_type == "妖精":
            row = 17
        df = pd.read_excel("屬性克制表.xlsx")
        good = df.at[row,"效果絕佳"]
        send_text_message(event.reply_token,good)
        self.go_back()

    def is_going_to_moves(self,event):
        text = event.message.text
        if  (text == '招式'):
            return True
        return False

    def on_enter_moves(self,event):
        title = '選擇作戰型態'
        text = '攻擊型 防守型'
        btn = [
                MessageTemplateAction(
                    label = '快速技能',
                    text = '快速技能'
                    ),
                MessageTemplateAction(
                    label = '主要技能',
                    text = '主要技能'
                    ),    
            ]
        url = 'https://p2.bahamut.com.tw/B/2KU/03/94f2d50eeaca838f2033a302101780r5.JPG?w=1000'
        send_button_message(event.reply_token, title, text, btn, url)
        
    """
    def is_going_to_attack(self,event):
        text = event.message.text
        if  (text == '攻擊型'):
            return True
        return False

    def on_enter_attack(self,event):
        pkm_id = id(name)
        termed_id = pkm_id[1:]
        content = moves_attack(termed_id)
        send_text_message(event.reply_token,content)
 
    def is_going_to_defend(self,event):
        text = event.message.text
        if  (text == '防守型'):
            return True
        return False

    def on_enter_defend(self,event):
        pkm_id = id(name)
        termed_id = pkm_id[1:]
        content = moves_defend(termed_id)
        send_text_message(event.reply_token,content)
"""
    def is_going_to_fast_moves(self,event):
        text = event.message.text
        if  (text == '快速技能'):
            return True
        return False

    def on_enter_fast_moves(self,event):
        pkm_id = id(name)
        termed_id = pkm_id[1:]
        content = fast_moves(termed_id)
        send_text_message(event.reply_token,content)
        self.go_back()
        
    def is_going_to_main_moves(self,event):
        text = event.message.text
        if  (text == '主要技能'):
            return True
        return False 

    def on_enter_main_moves(self,event):
        pkm_id = id(name)
        termed_id = pkm_id[1:]
        content = main_moves(termed_id)
        send_text_message(event.reply_token,content)
        self.go_back()

    
