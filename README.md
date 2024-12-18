# 公車營運績效分析

## 項目說明
為公車績效分析，並且找出各公車路線營運績效破口的程式碼，並且包含展示Tableau視覺化儀表板的內容。 <br>
主要的程式碼如下列三個，需要依序進行執行： <br>
1. prepare.ipynb：用於公車動態網站的班表爬蟲，可以針對循環班次、單向路線進行切分。因該網站為內嵌網站，無法直接抓取原始api資料，因此選擇以selenium模擬使用者行為，建立平日及假日班表。
2. busroute.ipynb：將完整路段的公車線型圖檔，依據每個路線的公車站序資料依序切分，並轉換為每個路線的逐條公車站點路線資料；可用於後續計算行駛里程長度、站間量視覺畫應用。
3. main.ipynb：比對營運資料、電子票證刷卡資料進行計算，並且依據上車時間比對班表資料，推測每一筆刷卡資料對應的班別，以進行更細部的計算。

本次開發的其他次要套件：
1. busroute.py：公車路線切分、公車站點比對路線。
2. tickets_cleaning.py：包含資料清洗、每月日期天數計算(扣除國定假日)、票證放大率、營運績效指標計算、班表比對等功能。

## 安裝步驟
因本專案的資料涉及個資無法提供，但欲使用相關的路線資料，可以至TDX官網進行下載路線資料，以及函文請示相關資料。 <br>
需要確保目錄架構為： <br>
project_name/ <br>
├── code/ <br>
│   ├── prepare.ipynb      # 公車動態網站班表爬蟲 <br>
│   ├── busroute.ipynb     # 公車路線切分與轉換 <br>
│   └── main.ipynb         # 營運資料、票證資料的比對與計算 <br>
│   ├── busroute.py        # 公車路線切分與站點比對 <br>
│   ├── tickets_cleaning.py # 資料清洗、票證放大率、營運績效指標計算 <br>
├── input/ <br>
│   ├── tickets.csv        # 原始票證資料 <br>
│   ├── operation.csv      # 原始營運資料 <br>
│   └── seq.csv            # 公車站序資料 <br>
├── requirements.txt       # 用於安裝依賴包的列表 <br>
└── README.md              # 項目的說明文件 <br>


## Tableau 儀表板展示
將我們蒐集到的資料結合Tableau進行BI儀表板的製作，成果如下：
### 1. 各營運業者的營運績效探討
1. 上方的折線圖，可以作為初步資料檢核的步驟，因為可以透過點選各項指標，確定是否符合先驗知識中的趨勢；亦可能找出可能缺失的資料。
2. 因各業者的經營路線、經營策略不同，因此需要進行個別輔導以及給予建議，因此會將各項指標分開查看。
（以搭乘人次作為示範，但實際上可切換多項指標）
![image](https://github.com/user-attachments/assets/b2eef205-7514-403a-9f9a-ce23b31f6cc8)


### 2. 投入產出分析的探討
左側的象限圖為投入產出分析比較圖表：在公車的分析上，我們可以用每日班次代表投入，每公里載客視為我們的報酬，並且以平均值劃分四個象限。
右側則顯示為原始公車營運統計相關的原始資料。

圖片中的概念為：
1. 第一象限：高投入高報酬
2. 第二象限：低投入高報酬
3. 第三象限：低投入低報酬，建議可透過「最大站間量」檢討車型是否轉換或進行混和調度，並透過「每班次載客」進行減班
4. 第四象限：高投入低報酬，需透過「每班次載客」進行減班進行減班
![image](https://github.com/user-attachments/assets/93ff6740-9479-40a5-bf27-2bda1101dc02)


### 3. 調整路線各個班次的載客狀況
這邊使用的資料為「票證資料」，所以理論上的票證人次會 <font color=#800000>小於或等於</font> 第一頁的搭乘人次，因搭乘人次可能以現金付款，或是在票證資料清洗中清除了部分資料異常的數據。（若需要可以進行票證的放大，但目前並無特別針對票證進行放大。）<br>
左側的表格與第一頁的象限圖相同，可點擊象限中的圖表，可快速右側的路線載客狀況。<br>
各路線每個班次的上車人次，可以視為「該班次的載客人數」，透過每個月分的平均統計，可以得出該月份特定班次的平均搭乘人次。<br>
<br>
使用說明：
1. 篩選認定為績效較差的班次門檻（例如將每班次載客8人視為門檻值，在實務上可考慮車型、月平均資料進行比較)
2. 於「是否進行篩選」選擇「是」，即可以顯示不滿足門檻值的所有班次
3. 這些不滿足門檻值的路線可能為績效較差的路線，可以視情況列為潛在減班班次。
4. 優先查看營運月報每班次載客人數較差的路線，確認是否其路線每班次都表現低於預期（可能部分路線集中於特定班次）
![image](https://github.com/user-attachments/assets/d70e0acf-4acb-4ef5-97dd-0ccee8eb717f)
![image](https://github.com/user-attachments/assets/787d1c18-50b6-425e-90b6-ae6b3c89bbd4)


### 4. 站間量
站間量的定義為公車站與公車站之間，車上的乘客數量；計算方式為比對班次、站序累加（上車人數 - 下車人數)的數量。
<br>
使用說明：
1. 可以點選有興趣的班次營運狀況，下方的站間量會顯示站與站之間的站間量。
2. 若全部都為8人以下，可以考慮更換為"9人座中型巴士"；若為16人以下，可以考慮混和調度2輛以上中巴。(因中型巴士不需要大型職業駕駛執照，可以釋出人力）<br>如果全部都是4人以下，以營運立場建議退場，或交由其他公車繞駛，或是以「小黃計程車」進行預約式營運
3. 如果部分路線的站間量都在1人以下，可以建議裁撤該段路線。
![image](https://github.com/user-attachments/assets/e44eaa99-43cc-4cca-886c-2d92d7b095e4)

## 貢獻者指引
* email:timothychang.kj@gmail.com
* https://linkedin.com/in/timothychang.kj

## 授權信息
MIT License

Copyright (c) 2024 TimothyChang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

NOTE: Data related to this project is not included and is not provided for public use. Please refer to the respective data sources for more information.




