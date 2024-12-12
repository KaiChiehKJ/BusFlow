# 1. 拆解公車路線的函數
import geopandas as gpd
import pandas as pd
import os
from shapely.geometry import Point, LineString

def split_line(line):
    """將長的 LineString 拆解為多個小段"""
    coords = list(line.coords)
    segments = []
    for i in range(len(coords) - 1):
        segment = LineString([coords[i], coords[i + 1]])
        segments.append(segment)
    return segments

# 2. 找出最近的路線段的函數
def find_nearest_segment(point, line_segments):
    """找出站點與所有路線段中距離最近的那條路線段"""
    min_distance = float('inf')
    nearest_segment = None
    for segment in line_segments:
        distance = point.distance(segment)
        if distance < min_distance:
            min_distance = distance
            nearest_segment = segment
    return nearest_segment

# 3. 主函數：將路線與站點結合
def get_busroute_segment(busroute_select, seq_select, seq_seq_col):
    """
    這個函數會拆解公車路線，並將每個站點黏貼到最近的路線段上，
    最後依據站點的自定義順序欄位排序並建立每段路線的 GeoDataFrame。

    :param busroute_select: 包含公車路線的 GeoDataFrame
    :param seq_select: 包含公車站點的 GeoDataFrame
    :param seq_seq_col: 指定用於排序的站點順序欄位名稱
    :return: 每段路線的 GeoDataFrame (gdf_segments)
    """
    
    # 1. 拆解 busroute_select 中的路線資料
    busroute_select['geometry'] = busroute_select['geometry'].apply(
        lambda x: split_line(x) if isinstance(x, LineString) else x
    )
    
    # 2. 將站點與最近的路線段進行匹配
    seq_select['nearest_segment'] = seq_select['geometry'].apply(
        lambda point: find_nearest_segment(point, busroute_select['geometry'][0])
    )
    
    # 3. 依據 seq_seq_col 排序站點
    seq_select = seq_select.sort_values(by=seq_seq_col)
    
    # 4. 創建每段路線的 GeoDataFrame
    segments = []
    for i in range(len(seq_select) - 1):
        start_stop = seq_select.iloc[i]
        end_stop = seq_select.iloc[i + 1]
        
        # 連接兩個站點
        segment = {
            'StartSeq': start_stop[seq_seq_col],
            'EndSeq': end_stop[seq_seq_col],
            'geometry': LineString([start_stop['geometry'], end_stop['geometry']])
        }
        segments.append(segment)
    
    # 創建 GeoDataFrame 來儲存每段路線
    gdf_segments = gpd.GeoDataFrame(segments, geometry='geometry', crs="EPSG:4326")
    gdf_segments = gdf_segments[gdf_segments['StartSeq'] < gdf_segments['EndSeq']].reset_index(drop = True)
    gdf_segments = gdf_segments.sort_values(['StartSeq', 'EndSeq'])
    gdf_segments['OD'] = gdf_segments['StartSeq'].astype(str) + "-" + gdf_segments['EndSeq'].astype(str)
    return gdf_segments
