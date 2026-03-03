"""
路线规划工具
"""
import random
from typing import Dict, Any, List

# 景点距离数据库（简化版，单位：公里）
DISTANCE_MATRIX = {
    "故宫": {"长城": 65, "颐和园": 18, "天安门": 2, "天坛": 5, "圆明园": 20, "恭王府": 4, "鸟巢": 10, "水立方": 10},
    "长城": {"故宫": 65, "颐和园": 50, "天安门": 67, "天坛": 70, "圆明园": 55, "恭王府": 66, "鸟巢": 60, "水立方": 60},
    "颐和园": {"故宫": 18, "长城": 50, "天安门": 20, "天坛": 23, "圆明园": 3, "恭王府": 12, "鸟巢": 12, "水立方": 12},
    "天安门": {"故宫": 2, "长城": 67, "颐和园": 20, "天坛": 3, "圆明园": 22, "恭王府": 4, "鸟巢": 11, "水立方": 11},
    "天坛": {"故宫": 5, "长城": 70, "颐和园": 23, "天安门": 3, "圆明园": 25, "恭王府": 7, "鸟巢": 13, "水立方": 13},
    "圆明园": {"故宫": 20, "长城": 55, "颐和园": 3, "天安门": 22, "天坛": 25, "恭王府": 16, "鸟巢": 14, "水立方": 14},
    "恭王府": {"故宫": 4, "长城": 66, "颐和园": 12, "天安门": 4, "天坛": 7, "圆明园": 16, "鸟巢": 10, "水立方": 10},
    "鸟巢": {"故宫": 10, "长城": 60, "颐和园": 12, "天安门": 11, "天坛": 13, "圆明园": 14, "恭王府": 10, "水立方": 0.5},
    "水立方": {"故宫": 10, "长城": 60, "颐和园": 12, "天安门": 11, "天坛": 13, "圆明园": 14, "恭王府": 10, "鸟巢": 0.5},
    # 上海
    "外滩": {"东方明珠": 2, "迪士尼": 25, "豫园": 3},
    "东方明珠": {"外滩": 2, "迪士尼": 24, "豫园": 4},
    "迪士尼": {"外滩": 25, "东方明珠": 24, "豫园": 26},
    "豫园": {"外滩": 3, "东方明珠": 4, "迪士尼": 26},
    # 杭州
    "西湖": {"灵隐寺": 8, "雷峰塔": 3, "宋城": 15},
    "灵隐寺": {"西湖": 8, "雷峰塔": 9, "宋城": 12},
    "雷峰塔": {"西湖": 3, "灵隐寺": 9, "宋城": 14},
    "宋城": {"西湖": 15, "灵隐寺": 12, "雷峰塔": 14},
    # 西安
    "兵马俑": {"大雁塔": 40, "华清池": 8, "城墙": 35},
    "大雁塔": {"兵马俑": 40, "华清池": 35, "城墙": 8},
    "华清池": {"兵马俑": 8, "大雁塔": 35, "城墙": 32},
    "城墙": {"兵马俑": 35, "大雁塔": 8, "华清池": 32},
}

def plan_route(points_list: List[str], days: int) -> Dict[str, Any]:
    """
    规划最优旅游路线
    
    使用贪心算法（最近邻）优化路线顺序
    
    Args:
        points_list: 途经点列表
        days: 游玩天数
    
    Returns:
        包含最优路线和分组信息的字典
    """
    if not points_list:
        return {"route": [], "days": days, "groups": [], "total_distance": 0}
    
    if len(points_list) == 1:
        return {
            "route": points_list,
            "days": days,
            "groups": [points_list],
            "total_distance": 0
        }
    
    # 使用贪心算法优化路线
    optimized = _optimize_route(points_list)
    
    # 按天数分组
    points_per_day = max(1, len(optimized) // days)
    groups = []
    
    for i in range(days):
        start_idx = i * points_per_day
        end_idx = min(start_idx + points_per_day, len(optimized))
        group = optimized[start_idx:end_idx]
        if group:
            groups.append(group)
    
    # 如果有剩余景点，加到最后一天
    all_grouped = [p for g in groups for p in g]
    remaining = [p for p in optimized if p not in all_grouped]
    if remaining and groups:
        groups[-1].extend(remaining)
    
    # 计算总距离
    total_distance = _calculate_total_distance(optimized)
    
    return {
        "route": optimized,
        "days": days,
        "groups": groups,
        "total_distance": total_distance,
        "points_per_day": points_per_day,
        "strategy": _get_strategy(days, len(optimized))
    }

def _optimize_route(points: List[str]) -> List[str]:
    """使用贪心算法优化路线顺序"""
    if len(points) <= 2:
        return points
    
    # 从第一个点开始
    remaining = points[1:].copy()
    route = [points[0]]
    
    while remaining:
        current = route[-1]
        # 找到最近的未访问点
        nearest = min(remaining, key=lambda p: _get_distance(current, p))
        route.append(nearest)
        remaining.remove(nearest)
    
    return route

def _get_distance(point1: str, point2: str) -> float:
    """获取两点间距离"""
    if point1 == point2:
        return 0
    
    # 查表
    if point1 in DISTANCE_MATRIX and point2 in DISTANCE_MATRIX[point1]:
        return DISTANCE_MATRIX[point1][point2]
    
    if point2 in DISTANCE_MATRIX and point1 in DISTANCE_MATRIX[point2]:
        return DISTANCE_MATRIX[point2][point1]
    
    # 默认值（随机生成一个合理的距离）
    return random.randint(5, 30)

def _calculate_total_distance(route: List[str]) -> float:
    """计算路线总距离"""
    total = 0
    for i in range(len(route) - 1):
        total += _get_distance(route[i], route[i + 1])
    return round(total, 1)

def _get_strategy(days: int, points: int) -> str:
    """给出路线策略建议"""
    ratio = points / days
    
    if ratio <= 1:
        return "深度游策略：每天1个景点，体验充分"
    elif ratio <= 2:
        return "舒适游策略：每天1-2个景点，节奏适中"
    elif ratio <= 3:
        return "标准游策略：每天2-3个景点，注意体力分配"
    else:
        return "紧凑游策略：景点较多，建议优先选择重点游览"
