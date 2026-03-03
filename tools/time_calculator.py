"""
时间计算工具
"""
import random
from typing import Dict, Any, List

# 各景点基础游玩时间（小时）
BASE_TIME = {
    "故宫": 4,
    "长城": 5,
    "颐和园": 3,
    "天安门": 1,
    "天坛": 2,
    "圆明园": 3,
    "恭王府": 2,
    "鸟巢": 1.5,
    "水立方": 1.5,
    "外滩": 2,
    "东方明珠": 3,
    "迪士尼": 8,
    "豫园": 2,
    "西湖": 4,
    "灵隐寺": 2,
    "雷峰塔": 1.5,
    "宋城": 4,
    "兵马俑": 3,
    "大雁塔": 2,
    "华清池": 2,
    "城墙": 3,
}

# 拥挤度影响系数
CROWD_MULTIPLIER = {
    "稀疏": 1.0,
    "适中": 1.3,
    "拥挤": 1.8
}

def calculate_time(route: List[str], crowd_level: str) -> Dict[str, Any]:
    """
    计算游玩总时间
    
    Args:
        route: 路线上的景点列表
        crowd_level: 整体拥挤程度 (稀疏/适中/拥挤)
    
    Returns:
        包含时间计算结果的字典
    """
    multiplier = CROWD_MULTIPLIER.get(crowd_level, 1.3)
    
    time_per_attraction = {}
    total_base_time = 0
    
    for attraction in route:
        base = BASE_TIME.get(attraction, 2)
        adjusted = base * multiplier
        
        # 添加一些随机性 (±15%)
        variation = random.uniform(0.85, 1.15)
        final_time = round(adjusted * variation, 1)
        
        time_per_attraction[attraction] = final_time
        total_base_time += final_time
    
    # 添加交通时间（每个景点之间约30-60分钟）
    transport_time = max(0, (len(route) - 1)) * 0.75  # 平均45分钟
    
    # 添加休息、用餐时间
    break_time = len(route) * 0.5  # 每个景点后休息30分钟
    
    total_time = total_base_time + transport_time + break_time
    
    # 转换为天数
    days_needed = total_time / 8  # 按每天8小时活动计算
    
    return {
        "attractions": route,
        "crowd_level": crowd_level,
        "time_per_attraction": time_per_attraction,
        "total_attraction_time": round(total_base_time, 1),
        "transport_time": round(transport_time, 1),
        "break_time": round(break_time, 1),
        "total_time": round(total_time, 1),
        "total_hours": int(total_time),
        "days_needed": round(days_needed, 1),
        "feasible": days_needed <= len(route) * 0.8,  # 粗略判断是否可行
        "suggestion": _get_time_suggestion(total_time, len(route))
    }

def _get_time_suggestion(total_hours: float, num_attractions: int) -> str:
    """根据总时间给出建议"""
    avg_time = total_hours / num_attractions if num_attractions > 0 else 0
    
    if avg_time >= 4:
        return "行程安排较紧，建议适当删减景点或延长游玩天数"
    elif avg_time >= 3:
        return "行程较为充实，注意合理安排休息时间"
    elif avg_time >= 2:
        return "行程节奏适中，体验与效率兼顾"
    else:
        return "行程较为宽松，有充足时间深度体验"
