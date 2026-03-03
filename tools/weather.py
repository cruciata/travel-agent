"""
天气查询工具
"""
import random
from typing import Dict, Any

# 模拟天气数据库
WEATHER_CONDITIONS = ["晴", "多云", "阴", "小雨", "中雨", "雷阵雨"]
TEMPERATURE_RANGES = {
    "北京": (15, 28),
    "上海": (18, 30),
    "杭州": (16, 29),
    "西安": (14, 27),
    "成都": (17, 26),
    "广州": (22, 32),
    "深圳": (23, 31),
}

def get_weather(city: str, days: int) -> Dict[str, Any]:
    """
    查询指定城市未来几天的天气
    
    Args:
        city: 城市名称
        days: 天数
    
    Returns:
        包含天气信息的字典
    """
    temp_range = TEMPERATURE_RANGES.get(city, (15, 28))
    
    forecast = []
    for i in range(days):
        condition = random.choice(WEATHER_CONDITIONS)
        temp_high = random.randint(temp_range[0], temp_range[1])
        temp_low = temp_high - random.randint(5, 12)
        
        forecast.append({
            "day": i + 1,
            "condition": condition,
            "temp_high": temp_high,
            "temp_low": temp_low,
            "humidity": random.randint(40, 85),
            "wind": random.choice(["微风", "3级", "4级", "5级"]),
            "uv": random.choice(["弱", "中等", "强"]),
            "suggestion": _get_weather_suggestion(condition)
        })
    
    # 判断整体天气是否适合出行
    rainy_days = sum(1 for f in forecast if "雨" in f["condition"])
    
    return {
        "city": city,
        "days": days,
        "overall": "适宜出行" if rainy_days <= 1 else "注意防雨",
        "rainy_days": rainy_days,
        "forecast": forecast
    }

def _get_weather_suggestion(condition: str) -> str:
    """根据天气给出建议"""
    suggestions = {
        "晴": "阳光明媚，适合户外活动，注意防晒",
        "多云": "天气舒适，非常适合旅游",
        "阴": "凉爽舒适，适合长时间户外活动",
        "小雨": "记得带伞，雨景别有一番风味",
        "中雨": "建议调整行程，安排室内活动",
        "雷阵雨": "注意避雨，关注天气变化"
    }
    return suggestions.get(condition, "注意天气变化")
