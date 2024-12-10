def tickets_cleaning(
    tickets, 
    getontime='GetOnTime', 
    getofftime='GetOffTime', 
    getonstop='GetOnStop', 
    getoffstop='GetOffStop', 
    getonseq='GetOnSeq', 
    getoffseq='GetOffSeq'):
    """
    清理票證資料，篩選出符合條件的票證並輸出統計結果。
    """
    # 原始票證數量
    import pandas as pd
    import os 
    original_count = len(tickets)

    # 建立篩選條件
    valid_conditions = (
        (tickets[getontime] < tickets[getofftime]) &  # 上車時間早於下車時間
        (tickets[getonstop] != tickets[getoffstop]) &  # 上下車站不同
        (tickets[getonseq] < tickets[getoffseq])  # 上下車序正確
    )

    # 檢查每個條件的異常數量
    late_count = (tickets[getontime] >= tickets[getofftime]).sum()
    same_stop_count = (tickets[getonstop] == tickets[getoffstop]).sum()
    seq_error_count = (tickets[getonseq] >= tickets[getoffseq]).sum()
    

    # 篩選出符合條件的票證
    cleaned_tickets = tickets[valid_conditions]
    canuse_count = len(cleaned_tickets)

    # 統計結果
    output = {
        '原始票證數量': original_count,
        '資料正常':canuse_count, 
        '資料異常 - 上車晚於下車': late_count,
        '資料異常 - 同站上下車': same_stop_count,
        '資料異常 - 上下車次序錯誤': seq_error_count
    }

    correctrate = round((canuse_count / original_count) * 100, 1)
    return cleaned_tickets, output, correctrate

def date_defined(tickets, getontime_columns='GetOnTime', date_turn_holiday=None, date_turn_workday=None):
    """
    定義平日或假日的判斷函式。

    :param tickets: 包含日期的 DataFrame。
    :param getontime_columns: 欲判斷的日期欄位名稱（預設為 'GetOnTime'）。
    :param date_turn_holiday: 清單，包含平日調為假日的日期。
    :param date_turn_workday: 清單，包含假日調為平日的日期。
    :return: DataFrame，新增 IsWorkday 欄位。
    """
    import pandas as pd

    # 初始化預設值
    if date_turn_holiday is None:
        date_turn_holiday = []
    if date_turn_workday is None:
        date_turn_workday = []

    # 確保日期清單為 datetime 格式
    date_turn_holiday = pd.to_datetime(date_turn_holiday)
    date_turn_workday = pd.to_datetime(date_turn_workday)

    # 判斷日期是否為平日或假日
    def is_workday(date):
        if date in date_turn_holiday:
            return 0  # 平日調為假日
        elif date in date_turn_workday:
            return 1  # 假日調為平日
        elif date.weekday() < 5:  # 平日（週一至週五）
            return 1
        else:  # 假日（週六、週日）
            return 0

    # 新增 IsWorkday 欄位
    tickets['IsWorkday'] = pd.to_datetime(tickets[getontime_columns]).apply(is_workday)
    tickets['DataYearMonth'] = pd.to_datetime(tickets[getontime_columns]).dt.strftime('%Y%m') #.astype('int64')
    return tickets


def getDaysCount(startdate, enddate, date_turn_holiday, date_turn_workday):
    """
    計算每個月的假日與平日數量

    Parameters:
    startdate (int): 起始日期 (格式：YYYYMMDD)
    enddate (int): 結束日期 (格式：YYYYMMDD)
    date_turn_holiday (list): 補假、國定假日、颱風天 (格式：YYYYMMDD)
    date_turn_workday (list): 補班 (格式：YYYYMMDD)

    Returns:
    pd.DataFrame: 每月假日與平日數，包含欄位 DataYearMonth, Holiday, Workday
    """
    import pandas as pd
    from datetime import datetime

    # 將日期轉換為 datetime 格式
    start_date = datetime.strptime(str(startdate), "%Y%m%d")
    end_date = datetime.strptime(str(enddate), "%Y%m%d")
    date_turn_holiday = [datetime.strptime(str(d), "%Y%m%d") for d in date_turn_holiday]
    date_turn_workday = [datetime.strptime(str(d), "%Y%m%d") for d in date_turn_workday]

    # 建立日期範圍
    date_range = pd.date_range(start=start_date, end=end_date)

    # 計算每一天是否為平日/假日
    data = []
    for date in date_range:
        is_weekend = date.weekday() >= 5  # 星期六、日為週末
        is_holiday = date in date_turn_holiday  # 是否為補假
        is_workday = date in date_turn_workday  # 是否為補班

        # 判斷是否為假日
        if is_weekend or is_holiday:
            if not is_workday:  # 若週末/假日不是補班
                is_holiday_final = True
            else:
                is_holiday_final = False
        else:
            is_holiday_final = False

        # 判斷是否為平日
        is_workday_final = not is_holiday_final

        data.append({
            "Date": date,
            "Holiday": is_holiday_final,
            "Workday": is_workday_final
        })

    # 將資料轉為 DataFrame
    df = pd.DataFrame(data)

    # 提取年月
    df["DataYearMonth"] = df["Date"].dt.strftime("%Y%m")

    # 計算每月的假日與平日數
    result = df.groupby("DataYearMonth").agg(
        Holiday=("Holiday", "sum"),
        Workday=("Workday", "sum")
    ).reset_index()

    return result

def getMagnification(
    tickets, 
    tickets_routename_col, 
    tickets_yearmonth_col, 
    operation, 
    operation_routename_col, 
    operation_yearmonth_col, 
    operation_passengers_col
):
    """
    計算票證數據與運營數據的放大倍率。

    Parameters:
    tickets (pd.DataFrame): 票證數據
    tickets_routename_col (str): 票證數據中的路線名稱列
    tickets_yearmonth_col (str): 票證數據中的年月列
    operation (pd.DataFrame): 運營數據
    operation_routename_col (str): 運營數據中的路線名稱列
    operation_yearmonth_col (str): 運營數據中的年月列
    operation_passengers_col (str): 運營數據中的乘客數量列

    Returns:
    pd.DataFrame: 包含票證數、運營乘客數與放大倍率的數據表
    """
    import pandas as pd 
    # 聚合票證數據
    tickets_agg = (
        tickets.groupby([tickets_routename_col, tickets_yearmonth_col])
        .size()
        .reset_index(name='Tickets')
        .rename(columns={tickets_routename_col: 'RouteName', tickets_yearmonth_col: 'DataYearMonth'})
    )

    # 聚合運營數據
    operation_agg = (
        operation.groupby([operation_routename_col, operation_yearmonth_col])
        .agg({operation_passengers_col: 'sum'})
        .reset_index()
        .rename(columns={operation_routename_col: 'RouteName', operation_yearmonth_col: 'DataYearMonth', operation_passengers_col: 'Passengers'})
    )

    # 合併數據並計算放大倍率
    tickets_magnification = pd.merge(tickets_agg, operation_agg, on=['RouteName', 'DataYearMonth'], how='left')
    tickets_magnification['Magnification'] = (tickets_magnification['Passengers'] / tickets_magnification['Tickets']).round(3)

    # 填充缺失值並排序
    tickets_magnification = tickets_magnification.fillna(0)
    tickets_magnification = tickets_magnification.sort_values(
        ['DataYearMonth', 'Magnification', 'RouteName'], ascending=[True, False, True]
    ).reset_index(drop=True)

    return tickets_magnification

def tickets_match_shift(tickets, shifts, routename_col = "ROUTE_NAME" ,getontime_col='GETON_DATE', direction_col='DIRECTION'):
    """
    將刷卡資料匹配到最接近的班次。

    參數:
        tickets (DataFrame): 包含刷卡資料的 DataFrame。
        shifts (DataFrame): 包含班次資料的 DataFrame。
        getontime_col (str): 表示刷卡時間的欄位名稱，默認為 'GETON_DATE'。
        direction_col (str): 表示方向的欄位名稱，默認為 'DIRECTION'。

    返回:
        DataFrame: 加入 "Matched_Shift" 欄位的刷卡資料 DataFrame。
    """
    import pandas as pd
    # 轉換時間欄位格式
    tickets[getontime_col] = pd.to_datetime(tickets[getontime_col])
    shifts["Shift"] = pd.to_datetime(shifts["Shift"], format="%H:%M:%S").dt.time

    # 定義函數來匹配班次
    def match_shift(row, available_shifts):
        geton_time = row[getontime_col].time()
        available_shifts = sorted(available_shifts)
        for i in range(len(available_shifts)):
            if geton_time < available_shifts[i]:  # 比最早的 Shift 早
                return available_shifts[max(0, i - 1)]  # 返回上一個班次（或第一個班次）
        return available_shifts[-1]  # 晚於所有班次，返回最後一個班次

    # 匹配班次的主要邏輯
    matched_shifts = []
    for _, ticket in tickets.iterrows():
        # 找到對應的班次
        route_shifts = shifts[
            (shifts["RouteName"] == ticket[routename_col]) &
            (shifts["IsWorkday"] == ticket["IsWorkday"]) &
            (shifts["Direction"] == ticket[direction_col])
        ]["Shift"].tolist()

        # 如果有班次，匹配
        if route_shifts:
            matched_shift = match_shift(ticket, route_shifts)
            matched_shifts.append(matched_shift)
        else:
            matched_shifts.append(None)  # 如果沒有匹配的班次

    # 新增匹配結果欄位
    tickets["Matched_Shift"] = matched_shifts
    return tickets