# 公車營運績效分析

最後將我們蒐集到的資料結合Tableau進行BI儀表板的製作，成果如下：

## 1. 營運基本績效的探討
左側的象限圖為投入產出分析比較圖表：在公車的分析上，我們可以用每日班次代表投入，每公里載客視為我們的報酬，並且以平均值劃分四個象限。
右側則顯示為原始公車營運統計相關的原始資料。

圖片中的概念為：
1. 第一象限：高投入高報酬
2. 第二象限：低投入高報酬
3. 第三象限：低投入低報酬，建議可透過「最大站間量」檢討車型是否轉換或進行混和調度，並透過「每班次載客」進行減班
4. 第四象限：高投入低報酬，需透過「每班次載客」進行減班進行減班
![image](https://github.com/user-attachments/assets/5d6c03a3-3164-46b9-a8cf-86e52e57a05b)

## 2. 調整路線各個班次的載客狀況
這邊使用的資料為「票證資料」，所以理論上的票證人次會**小於或等於**第一頁的搭乘人次，因搭乘人次可能以現金付款，或是在票證資料清洗中清除了部分資料異常的數據。<br>
左側的表格與第一頁的象限圖相同，可點擊象限中的圖表，可快速右側的路線載客狀況。<br>
各路線每個班次的上車人次，可以視為「該班次的載客人數」，透過每個月分的平均統計，可以得出該月份特定班次的平均搭乘人次。<br>

使用說明：
1. 篩選認定為績效較差的班次門檻（例如將每班次載客8人視為門檻值，在實務上可考慮車型、月平均資料進行比較)
2. 於「是否進行篩選」選擇「是」，即可以顯示不滿足門檻值的所有班次
3. 這些不滿足門檻值的路線可能為績效較差的路線，可以視情況列為潛在減班班次。

![image](https://github.com/user-attachments/assets/79b8cf94-f68f-4a96-8d28-a2f61fbcaa9f)
![image](https://github.com/user-attachments/assets/18873398-ef3f-402d-8eba-26219ed0414a)

