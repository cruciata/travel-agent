"""
景点人流查询工具
"""
import random
from typing import Dict, Any

# 热门景点基础人流数据
CROWD_BASE = {
    "故宫": 3,      # 基础拥挤度 (1-5)
    "长城": 4,
    "颐和园": 2,
    "天安门": 4,
    "天坛": 2,
    "圆明园": 2,
    "恭王府": 2,
    "鸟巢": 1,
    "水立方": 1,
    "外滩": 3,
    "东方明珠": 3,
    "迪士尼": 5,
    "豫园": 3,
    "西湖": 3,
    "灵隐寺": 3,
    "雷峰塔": 2,
    "宋城": 3,
    "兵马俑": 4,
    "大雁塔": 3,
    "华清池": 2,
    "城墙": 2,
}

def get_crowd(attraction_name: str, date: str = "today") -> Dict[str, Any]:
    """
    查询指定景点的人流情况
    
    Args:
        attraction_name: 景点名称
        date: 日期 (默认today)
    
    Returns:
        包含人流信息的字典
    """
    # 获取基础拥挤度
    base = CROWD_BASE.get(attraction_name, 2)
    
    # 添加随机波动 (-1 到 +1)
    variation = random.randint(-1, 1)
    crowd_score = max(1, min(5, base + variation))
    
    # 映射到文字描述
    level_map = {
        1: "稀疏",
        2: "稀疏",
        3: "适中",
        4: "拥挤",
        5: "拥挤"
    }
    
    level = level_map[crowd_score]
    
    # 等待时间估算（分钟）
    wait_times = {
        1: (0, 5),
        2: (5, 15),
        3: (15, 30),
        4: (30, 60),
        5: (45, 90)
    }
    wait_range = wait_times[crowd_score]
    estimated_wait = random.randint(wait_range[0], wait_range[1])
    
    # 最佳游览时间建议
    best_times = _get_best_times(crowd_score)
    
    return {
        "attraction": attraction_name,
        "level": level,
        "score": crowd_score,  # 1-5
        "estimated_wait_minutes": estimated_wait,
        "best_visit_time": best_times,
        "suggestion": _get_crowd_suggestion(crowd_score)
    }

def _get_best_times(crowd_score: int) -> list:
    """根据拥挤度返回最佳游览时间"""
    if crowd_score >= 4:
        return ["08:00-09:00 开馆时段", "16:00-17:00 闭馆前"]
    elif crowd_score >= 3:
        return ["09:00-10:00", "15:00-16:00"]
    else:
        return ["全天适宜"]

def _get_crowd_suggestion(crowd_score: int) -> str:
    """根据拥挤度给出建议"""
    suggestions = {
        1: "人流稀少，可深度游览，尽情享受",
        2: "人流较少，体验良好，适合拍照",
        3: "人流适中，正常游览，建议提前预约",
        4: "人流较多，建议错峰出行，耐心等待",
        5: "人流密集，建议早到或改期，做好排队准备"
    }
    return suggestions.get(crowd_score, "建议提前规划")
