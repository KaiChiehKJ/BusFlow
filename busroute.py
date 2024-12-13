def snap_points_to_line(stops_gdf, routes_gdf, 
                        route_routename_col, route_direction_col, 
                        seq_routename_col, seq_direction_col, 
                        seq_lat_col, seq_lng_col):
    """
    將公車站點 (stops_gdf) 投影到公車路線 (routes_gdf) 上，並動態帶入欄位名稱。
    Parameters:
        stops_gdf (GeoDataFrame): 包含公車站點的 GeoDataFrame。
        routes_gdf (GeoDataFrame): 包含公車路線的 GeoDataFrame。
        route_routename_col (str): 路線名稱欄位名稱。
        route_direction_col (str): 路線方向欄位名稱。
        seq_routename_col (str): 站點路線名稱欄位名稱。
        seq_direction_col (str): 站點方向欄位名稱。
        seq_lat_col (str): 站點緯度欄位名稱。
        seq_lng_col (str): 站點經度欄位名稱。
    Returns:
        GeoDataFrame: 更新後的公車站點 GeoDataFrame，其中 geometry 已投影到路線。
    """
    import geopandas as gpd
    from shapely.geometry import Point
    snapped_points = []

    for _, stop in stops_gdf.iterrows():
        # 找到與站點路線名稱和方向相符的路線
        matching_route = routes_gdf[(routes_gdf[route_routename_col] == stop[seq_routename_col]) & 
                                    (routes_gdf[route_direction_col] == stop[seq_direction_col])]

        if not matching_route.empty:
            # 取出該路線的 geometry
            line = matching_route.iloc[0].geometry
            # 計算站點投影到該路線的最近點
            snapped_point = line.interpolate(line.project(stop.geometry))
            snapped_points.append(snapped_point)
        else:
            # 如果沒有匹配的路線，保持原點
            snapped_points.append(stop.geometry)

    # 更新站點的 geometry
    stops_gdf = stops_gdf.copy()
    stops_gdf['geometry'] = snapped_points
    stops_gdf[seq_lat_col] = stops_gdf.geometry.y
    stops_gdf[seq_lng_col] = stops_gdf.geometry.x
    return stops_gdf