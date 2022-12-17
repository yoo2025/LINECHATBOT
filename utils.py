import os
from urllib import response
from xml.dom.minidom import Identified
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"
"""
#爬蟲
class findPKMname(PKM):
    
    def info(self):
        
        response = requests.get("https://wiki.52poke.com/wiki/" + self.name)
        
        soup = BeautifulSoup(response.text,"html.parser")
       
        ch_name = soup.find("span",{"style":"font-size:1.5em"}).getText()
    
        return ch_name

    def battle():
        response = requests.get("https://gamewith.jp/pokemon-sv/article/show/375162")

        soup = BeautifulStoneSoup(response.text,"html.parser")
        name=""
        id=""
        content = ""

        id = soup.find("span",{"class":"PokemonTeraraid_item__detail__strong_a3BOs"}).getText()
        name = soup.find("p",{"style":"margin-right: 8px;"}).getText()

        content = f"{name} {id}"

        return name
  """      


def info(name):
        
    response = requests.get("https://wiki.52poke.com/wiki/" + name)
        
    soup = BeautifulSoup(response.text,"html.parser")
       
    ch_name = soup.find("span",{"style":"font-size:1.5em"}).getText()
    jp_name = soup.find("span",{"lang":"ja"}).getText()

    content = f"{ch_name} {jp_name}"
    return content



def types(name):
        
    response = requests.get("https://wiki.52poke.com/wiki/" + name)
        
    soup = BeautifulSoup(response.text,"html.parser")
    
    type = soup.find("span",{"class":"type-box-9-text"}).getText()
    return type

def weakness(type):

    response = requests.get("https://wiki.52poke.com/wiki/" + type + "（属性）" )

    soup = BeautifulSoup(response.text,"html.parser")

    weak = soup.find("span",{"class":"type-box-9-text"}).getText()
        
    return weak
def id(name):
    response = requests.get("https://wiki.52poke.com/wiki/" + name)
        
    soup = BeautifulSoup(response.text,"html.parser")
    id = ""
    id = soup.find("th",{"style":"width:20%; font-size:1.5em"}).getText()
    return id
"""
def moves_attack(id):
    response = requests.get("https://pokemon.gameinfo.io/zh-tw/pokemon/" + id)
        
    soup = BeautifulSoup(response.text,"html.parser")
    
    moves = soup.find("table",{"class":"moveset elite"}).getText()
    
    if len(moves):
        moves = soup.find("div",{"class":"moves compact"}).getText()
    return moves

def moves_defend(id):
    response = requests.get("https://pokemon.gameinfo.io/zh-tw/pokemon/" + id)
        
    soup = BeautifulSoup(response.text,"html.parser")

    moves = soup.find_all("table",{"class":"moveset elite"})

    content=""
    for move in moves:
        content = move.text

    if bool(content):
        moves = soup.find_all("table",{"class":"moveset"})
        for move in moves:
            content = move.text

    return content
"""
def fast_moves(id):
    response = requests.get("https://pokemon.gameinfo.io/zh-tw/pokemon/" + id)
        
    soup = BeautifulSoup(response.text,"html.parser")
    
    moves = soup.find("table",{"class":"moves"}).getText()
    
    return moves

def main_moves(id):
    response = requests.get("https://pokemon.gameinfo.io/zh-tw/pokemon/" + id)
        
    soup = BeautifulSoup(response.text,"html.parser")

    moves = soup.find_all("table",{"class":"moves"})

    content=""
    for move in moves:
        content = move.text

    return content

def isChinese(word):
    for ch in word:
        if '\u4e00' > ch or ch > '\u9fff':
            return False
    return True
