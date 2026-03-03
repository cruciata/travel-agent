"""
美食推荐工具
"""
import random
from typing import Dict, Any, List

# 景点附近美食数据库
FOOD_DATABASE = {
    "故宫": [
        {"name": "四季民福烤鸭店", "type": "北京菜", "rating": 4.8, "price": 180, "distance": 800, "signature": "挂炉烤鸭、宫保鸡丁", "recommendation": "景观位可看到故宫东华门"},
        {"name": "老北京炸酱面大王", "type": "老北京小吃", "rating": 4.5, "price": 45, "distance": 600, "signature": "炸酱面、豆汁焦圈", "recommendation": "正宗老北京味道"},
        {"name": "景山花园餐厅", "type": "创意菜", "rating": 4.6, "price": 220, "distance": 500, "signature": "宫廷菜、创意京菜", "recommendation": "环境优雅，适合下午茶"},
    ],
    "长城": [
        {"name": "长城脚下公社餐厅", "type": "融合菜", "rating": 4.4, "price": 150, "distance": 2000, "signature": "烤羊腿、农家菜", "recommendation": "爬完长城后的完美补给"},
        {"name": "八达岭特色农家院", "type": "农家菜", "rating": 4.2, "price": 80, "distance": 3000, "signature": "炖柴鸡、贴饼子", "recommendation": "体验地道农家风味"},
        {"name": "长城第一楼", "type": "中餐", "rating": 4.0, "price": 120, "distance": 1500, "signature": "长城特色宴", "recommendation": "位置便利，菜品丰富"},
    ],
    "颐和园": [
        {"name": "听鹂馆饭庄", "type": "宫廷菜", "rating": 4.7, "price": 280, "distance": 300, "signature": "满汉全席、宫廷点心", "recommendation": "颐和园内的百年老店"},
        {"name": "西贝莜面村", "type": "西北菜", "rating": 4.5, "price": 95, "distance": 1200, "signature": "莜面、烤羊排", "recommendation": "服务热情，上菜快"},
        {"name": "绿茶餐厅", "type": "江浙菜", "rating": 4.3, "price": 85, "distance": 1500, "signature": "面包诱惑、绿茶烤鸡", "recommendation": "性价比高，环境好"},
    ],
    "天安门": [
        {"name": "全聚德", "type": "北京菜", "rating": 4.4, "price": 250, "distance": 1000, "signature": "挂炉烤鸭", "recommendation": "百年老字号，仪式感强"},
        {"name": "东来顺", "type": "涮羊肉", "rating": 4.5, "price": 150, "distance": 800, "signature": "涮羊肉、烧饼", "recommendation": "正宗清真涮肉"},
        {"name": "护国寺小吃", "type": "北京小吃", "rating": 4.3, "price": 35, "distance": 600, "signature": "豌豆黄、驴打滚", "recommendation": "一次性尝遍北京小吃"},
    ],
    "天坛": [
        {"name": "天坛福宴", "type": "北京菜", "rating": 4.4, "price": 140, "distance": 700, "signature": "天坛素斋、京味菜", "recommendation": "环境清幽"},
        {"name": "南门涮肉", "type": "涮羊肉", "rating": 4.6, "price": 120, "distance": 900, "signature": "手切鲜羊肉", "recommendation": "天坛南门老字号"},
        {"name": "锦馨豆汁", "type": "北京小吃", "rating": 4.0, "price": 25, "distance": 500, "signature": "豆汁、焦圈", "recommendation": "勇敢尝试老北京早餐"},
    ],
    "外滩": [
        {"name": "外滩茂悦大酒店", "type": "西餐", "rating": 4.8, "price": 450, "distance": 200, "signature": "景观晚餐、牛排", "recommendation": "无敌江景，浪漫首选"},
        {"name": "南翔馒头店", "type": "上海菜", "rating": 4.5, "price": 60, "distance": 800, "signature": "小笼包", "recommendation": "老字号，蟹粉小笼必点"},
        {"name": "沈大成", "type": "上海小吃", "rating": 4.4, "price": 40, "distance": 600, "signature": "条头糕、双酿团", "recommendation": "经典上海点心"},
    ],
    "西湖": [
        {"name": "楼外楼", "type": "杭帮菜", "rating": 4.5, "price": 180, "distance": 200, "signature": "西湖醋鱼、东坡肉", "recommendation": "西湖边的百年名楼"},
        {"name": "外婆家", "type": "杭帮菜", "rating": 4.4, "price": 70, "distance": 500, "signature": "茶香鸡、麻婆豆腐", "recommendation": "性价比之王"},
        {"name": "知味观", "type": "杭州小吃", "rating": 4.6, "price": 55, "distance": 800, "signature": "小笼包、猫耳朵", "recommendation": "杭州人从小吃到大的味道"},
    ],
    "兵马俑": [
        {"name": "临潼印象", "type": "陕西菜", "rating": 4.4, "price": 85, "distance": 2000, "signature": "葫芦鸡、臊子面", "recommendation": "临潼本地特色"},
        {"name": "老孙家", "type": "陕西小吃", "rating": 4.3, "price": 40, "distance": 3000, "signature": "羊肉泡馍、肉夹馍", "recommendation": "西安老字号"},
        {"name": "兵马俑餐厅", "type": "中餐", "rating": 4.0, "price": 70, "distance": 1000, "signature": "陕西面食", "recommendation": "参观完直接用餐"},
    ],
}

# 通用餐厅（当景点不在数据库时使用）
GENERIC_RESTAURANTS = [
    {"name": "本地特色餐厅", "type": "当地菜", "rating": 4.3, "price": 100, "distance": 800, "signature": "特色招牌菜", "recommendation": "口碑不错的本地餐厅"},
    {"name": "美食街大排档", "type": "小吃", "rating": 4.1, "price": 50, "distance": 500, "signature": "各类小吃", "recommendation": "体验当地烟火气"},
    {"name": "连锁快餐店", "type": "快餐", "rating": 4.0, "price": 40, "distance": 300, "signature": "快捷方便", "recommendation": "赶时间的好选择"},
]

def recommend_food(attraction_name: str) -> Dict[str, Any]:
    """
    为指定景点推荐附近餐厅
    
    Args:
        attraction_name: 景点名称
    
    Returns:
        包含餐厅推荐列表的字典
    """
    # 获取该景点的餐厅列表，如果没有则使用通用餐厅
    restaurants = FOOD_DATABASE.get(attraction_name, GENERIC_RESTAURANTS)
    
    # 添加一些随机性，调整评分和价格（±5%）
    varied_restaurants = []
    for r in restaurants:
        varied = r.copy()
        varied["rating"] = round(min(5.0, varied["rating"] + random.uniform(-0.2, 0.2)), 1)
        varied["price"] = int(varied["price"] * random.uniform(0.9, 1.1))
        varied_restaurants.append(varied)
    
    # 按评分排序
    varied_restaurants.sort(key=lambda x: x["rating"], reverse=True)
    
    # 计算平均消费
    avg_price = sum(r["price"] for r in varied_restaurants) // len(varied_restaurants)
    
    return {
        "attraction": attraction_name,
        "recommendations": varied_restaurants[:3],
        "average_price": avg_price,
        "cuisine_types": list(set(r["type"] for r in varied_restaurants)),
        "suggestion": _get_food_suggestion(avg_price)
    }

def _get_food_suggestion(avg_price: int) -> str:
    """根据平均价格给出建议"""
    if avg_price >= 200:
        return "附近以高档餐厅为主，建议提前预订"
    elif avg_price >= 100:
        return "餐饮选择多样，丰俭由人"
    elif avg_price >= 50:
        return "性价比较高，适合大众消费"
    else:
        return "以小吃快餐为主，经济实惠"
