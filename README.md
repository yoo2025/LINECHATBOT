# 寶可夢資料查詢

##  前言
寶可夢系列是個陪伴大家從小到大的遊戲，從最早的紅/綠寶石，到現在最新的朱/紫，每一代都會推出新的寶可夢，現在總共有1008種寶可夢，因此在遊戲中時常會碰到忘記某隻寶可夢的屬性或者弱點，所以想設計一個LINECHATBOT來協助玩家能夠更輕鬆地玩遊戲，可以輕鬆的查到所需的資訊。

## 構想
藉由使用者輸入的寶可夢名稱，去到對應的網站找出所需的資訊。

## 環境
### ● python 3.9

## 技術
- Beautifulsoup4
    - 爬取各網站所需的資料
- Pandas
    - 在excel檔中查詢資料

## 使用教學
### 1. 安裝 pipenv
        pip install pipenv
### 2. 安裝所需套件
        pipenv install --three
### 3. 修改.env內容，並填入以下兩個資訊
- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
### 4. 安裝 ngrok
<https://ngrok.com/>
### 5. 運行 ngrok 在本地執行LINECHATBOT
        ngrok http 8000
### 6. 執行 app.py
        pipenv run python app.py
## FSM
![](https://i.imgur.com/cfSUGm0.png) <br>

## 使用說明
### 第一步
- 輸入任意文字<br>
![](https://i.imgur.com/JSyLBlV.png)<br>
### 第二步
- 輸入 **寶可夢名稱** 或者 輸入 **fsm** 查看狀態圖<br>
![](https://i.imgur.com/MF6XMAx.png) <br>
![](https://i.imgur.com/Zig4Wor.png) <br>
### 第三步
- 選擇遊戲版本 朱/紫 or Pokemon Go <br>
![](https://i.imgur.com/JdRaqAQ.png) <br>
### 第四步
- 選擇要查詢的內容<br>
**Pokemon Go** <br>
![](https://i.imgur.com/yU3Sdho.png) <br>
**朱/紫** <br>
![](https://i.imgur.com/Q8c9A4E.png) <br>
### 第五步
- 選擇查詢內容的細項 <br>
![](https://i.imgur.com/AnAixGb.png) <br>
## 使用範例
![](https://i.imgur.com/8G5unC3.jpg) <br>

## State 說明
- user: 輸入任意文字開始查詢寶可夢資料
- pkm_input: 輸入想查詢的寶可夢名稱 或者 輸入fsm查看狀態圖
- greeting: 顯示遊戲版本選單
- fsm_graph: 展示狀態圖
- scarlet_violet: 寶可夢朱/紫的功能選單
- pokemon_go: Pokemon Go的功能選單
- battle: 回傳 朱/紫 太晶戰的網站
- type: 回傳該寶可夢屬性
- weakness: 回傳該寶可夢的弱點
- good_at: 回傳該寶可夢打甚麼屬性處於優勢
- moves: 進入查詢推薦技能選單
- fast_moves: 推薦的快速攻擊
- main_moves: 推薦的主要攻擊
