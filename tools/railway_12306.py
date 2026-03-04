"""
12306 火车票实时查询模块
提供列车时刻表、票价、余票查询功能
"""
import requests
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 12306 API 基础地址
BASE_URL = "https://kyfw.12306.cn"

# 城市车站代码映射（常用城市）
STATION_CODES = {
    "北京": "BJP",
    "北京西": "BXP",
    "北京南": "VNP",
    "上海": "SHH",
    "上海虹桥": "AOH",
    "上海南": "SNH",
    "广州": "GZQ",
    "广州南": "IZQ",
    "深圳": "SZQ",
    "深圳北": "IOQ",
    "杭州": "HZH",
    "杭州东": "HGH",
    "南京": "NJH",
    "南京南": "NKH",
    "武汉": "WHN",
    "武汉站": "WHN",
    "成都": "CDW",
    "成都东": "ICW",
    "重庆": "CQW",
    "重庆北": "CUW",
    "西安": "XAY",
    "西安北": "EAY",
    "郑州": "ZZF",
    "郑州东": "ZAF",
    "长沙": "CSQ",
    "长沙南": "CWQ",
    "天津": "TJP",
    "天津西": "TXP",
    "济南": "JNK",
    "济南西": "JGK",
    "青岛": "QDK",
    "青岛北": "QHK",
    "沈阳": "SYT",
    "沈阳北": "SBT",
    "大连": "DLT",
    "哈尔滨": "HBB",
    "哈尔滨西": "VAB",
    "长春": "CCT",
    "石家庄": "SJP",
    "太原": "TYV",
    "兰州": "LZJ",
    "乌鲁木齐": "WAR",
    "昆明": "KMM",
    "贵阳": "GIW",
    "南宁": "NNZ",
    "合肥": "HFH",
    "南昌": "NCG",
    "福州": "FZS",
    "厦门": "XMS",
    "厦门北": "XKS",
}


def get_station_code(city: str) -> Optional[str]:
    """获取城市车站代码"""
    # 直接匹配
    if city in STATION_CODES:
        return STATION_CODES[city]
    
    # 尝试匹配带"站"字的
    if city + "站" in STATION_CODES:
        return STATION_CODES[city + "站"]
    
    # 尝试匹配省会城市的主要车站
    major_stations = {
        "北京": "BJP",
        "上海": "SHH",
        "广州": "GZQ",
        "深圳": "SZQ",
        "杭州": "HZH",
        "南京": "NJH",
        "武汉": "WHN",
        "成都": "CDW",
        "重庆": "CQW",
        "西安": "XAY",
        "郑州": "ZZF",
        "长沙": "CSQ",
        "天津": "TJP",
        "济南": "JNK",
        "青岛": "QDK",
        "沈阳": "SYT",
        "大连": "DLT",
        "哈尔滨": "HBB",
        "长春": "CCT",
        "石家庄": "SJP",
        "太原": "TYV",
        "兰州": "LZJ",
        "乌鲁木齐": "WAR",
        "昆明": "KMM",
        "贵阳": "GIW",
        "南宁": "NNZ",
        "合肥": "HFH",
        "南昌": "NCG",
        "福州": "FZS",
        "厦门": "XMS",
    }
    
    return major_stations.get(city)


def query_12306_trains(from_city: str, to_city: str, date: str = None) -> Dict:
    """
    查询12306列车信息
    
    Args:
        from_city: 出发城市
        to_city: 到达城市
        date: 日期，格式YYYY-MM-DD，默认为明天
    
    Returns:
        查询结果字典
    """
    if date is None:
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    from_code = get_station_code(from_city)
    to_code = get_station_code(to_city)
    
    if not from_code or not to_code:
        return {
            "success": False,
            "error": f"暂不支持该城市查询: {from_city if not from_code else to_city}",
            "trains": []
        }
    
    try:
        # 构建查询URL
        url = f"{BASE_URL}/otn/leftTicket/queryZ"
        params = {
            "leftTicketDTO.train_date": date,
            "leftTicketDTO.from_station": from_code,
            "leftTicketDTO.to_station": to_code,
            "purpose_codes": "ADULT"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
        }
        
        # 发送请求
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"查询失败，状态码: {response.status_code}",
                "trains": []
            }
        
        data = response.json()
        
        if data.get("httpstatus") != 200 or not data.get("data"):
            return {
                "success": False,
                "error": "未找到列车信息或接口暂时不可用",
                "trains": []
            }
        
        # 解析列车数据
        trains = []
        train_list = data["data"].get("result", [])
        
        for train_info in train_list[:10]:  # 只取前10条
            train = parse_train_info(train_info)
            if train:
                trains.append(train)
        
        return {
            "success": True,
            "date": date,
            "from": from_city,
            "to": to_city,
            "train_count": len(trains),
            "trains": trains
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "查询超时，请稍后重试",
            "trains": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"查询异常: {str(e)}",
            "trains": []
        }


def parse_train_info(train_str: str) -> Optional[Dict]:
    """解析12306返回的列车信息字符串"""
    try:
        parts = train_str.split("|")
        if len(parts) < 35:
            return None
        
        train_no = parts[3]  # 车次号
        from_station_code = parts[6]
        to_station_code = parts[7]
        start_time = parts[8]  # 出发时间
        arrive_time = parts[9]  # 到达时间
        duration = parts[10]  # 历时
        
        # 各种座位余票信息
        business_class = parts[32] or "--"  # 商务座
        first_class = parts[31] or "--"  # 一等座
        second_class = parts[30] or "--"  # 二等座
        soft_sleeper = parts[23] or "--"  # 软卧
        hard_sleeper = parts[28] or "--"  # 硬卧
        hard_seat = parts[29] or "--"  # 硬座
        no_seat = parts[26] or "--"  # 无座
        
        # 判断是否有票
        def check_ticket(ticket_str):
            if ticket_str in ["--", "*", "", None]:
                return "无"
            if ticket_str == "有":
                return "有票"
            try:
                num = int(ticket_str)
                return f"{num}张" if num > 0 else "无"
            except:
                return ticket_str
        
        return {
            "train_no": train_no,
            "from": from_station_code,
            "to": to_station_code,
            "start_time": start_time,
            "arrive_time": arrive_time,
            "duration": duration,
            "tickets": {
                "商务座": check_ticket(business_class),
                "一等座": check_ticket(first_class),
                "二等座": check_ticket(second_class),
                "软卧": check_ticket(soft_sleeper),
                "硬卧": check_ticket(hard_sleeper),
                "硬座": check_ticket(hard_seat),
                "无座": check_ticket(no_seat),
            }
        }
    except Exception:
        return None


def get_train_price(from_city: str, to_city: str, train_no: str = None) -> Dict:
    """
    获取火车票价格（估算）
    
    由于12306价格查询接口较复杂，这里根据距离和车型给出估算价格
    """
    # 基础价格表（参考价格）
    price_table = {
        # 高铁/动车
        "G": {"二等座": 0.45, "一等座": 0.75, "商务座": 1.5},  # 每公里价格（元）
        "D": {"二等座": 0.35, "一等座": 0.55, "商务座": 1.1},
        "C": {"二等座": 0.40, "一等座": 0.65, "商务座": 1.3},
        # 普速列车
        "Z": {"硬座": 0.15, "硬卧": 0.30, "软卧": 0.50},
        "T": {"硬座": 0.13, "硬卧": 0.28, "软卧": 0.45},
        "K": {"硬座": 0.11, "硬卧": 0.25, "软卧": 0.40},
        "其他": {"硬座": 0.10, "硬卧": 0.22, "软卧": 0.35},
    }
    
    # 计算距离（需要导入travel_costs中的函数）
    try:
        from .travel_costs import calculate_distance
        distance = calculate_distance(from_city, to_city)
    except:
        distance = 500  # 默认500公里
    
    # 根据车次判断车型
    train_type = "G" if train_no and train_no.startswith("G") else \
                 "D" if train_no and train_no.startswith("D") else \
                 "C" if train_no and train_no.startswith("C") else \
                 "Z" if train_no and train_no.startswith("Z") else \
                 "T" if train_no and train_no.startswith("T") else \
                 "K" if train_no and train_no.startswith("K") else "其他"
    
    prices = price_table.get(train_type, price_table["其他"])
    
    result = {}
    for seat_type, price_per_km in prices.items():
        # 基础价格 + 距离价格
        base_price = max(int(distance * price_per_km), 20)
        result[seat_type] = base_price
    
    return {
        "train_no": train_no,
        "distance": distance,
        "train_type": train_type,
        "prices": result
    }


def format_train_info(train: Dict) -> str:
    """格式化列车信息为字符串"""
    tickets = train.get("tickets", {})
    
    # 找出有票的座位类型
    available_seats = []
    for seat_type, count in tickets.items():
        if count not in ["无", "--"]:
            available_seats.append(f"{seat_type}:{count}")
    
    seat_info = " | ".join(available_seats) if available_seats else "暂无余票"
    
    return f"🚄 {train['train_no']} | {train['start_time']}开 → {train['arrive_time']}到 | 历时{train['duration']} | {seat_info}"


# 便捷的查询函数
def search_trains(from_city: str, to_city: str, date: str = None) -> str:
    """
    搜索列车并返回格式化结果
    
    Returns:
        格式化的列车信息字符串
    """
    result = query_12306_trains(from_city, to_city, date)
    
    if not result["success"]:
        return f"❌ 查询失败: {result.get('error', '未知错误')}"
    
    trains = result["trains"]
    if not trains:
        return f"📅 {result['date']} {from_city} → {to_city}\n未找到列车信息"
    
    output = [f"📅 {result['date']} {from_city} → {to_city} 共{len(trains)}趟列车\n"]
    
    for i, train in enumerate(trains[:5], 1):  # 只显示前5趟
        output.append(format_train_info(train))
    
    return "\n".join(output)


if __name__ == "__main__":
    # 测试
    print(search_trains("北京", "上海"))
