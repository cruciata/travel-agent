"""
智能旅行规划Agent - ReAct架构核心实现
"""
import random
from typing import Dict, List, Any, Callable
from enum import Enum

class ActionStatus(Enum):
    """行动状态"""
    THINKING = "🧠 思考"
    ACTING = "🔧 行动"
    OBSERVING = "📊 结果"
    FINISHED = "✅ 完成"

class ReActAgent:
    """
    ReAct (Reasoning + Acting) 智能体
    循环: 思考 → 行动 → 观察 → 重复直到完成
    """
    
    def __init__(self, budget: int, points: List[str], days: int, food_enabled: bool):
        self.budget = budget
        self.points = points
        self.days = days
        self.food_enabled = food_enabled
        
        # 工具注册表
        self.tools: Dict[str, Callable] = {}
        
        # 执行历史
        self.history: List[Dict[str, Any]] = []
        
        # 收集的数据
        self.weather_data: Dict[str, Any] = {}
        self.crowd_data: Dict[str, Any] = {}
        self.route_data: Dict[str, Any] = {}
        self.time_data: Dict[str, Any] = {}
        self.food_data: Dict[str, Any] = {}
        
        print("=" * 60)
        print("🌍 智能旅行规划Agent已启动")
        print(f"💰 预算: {budget}元 | 📍 途经点: {points} | 📅 天数: {days}天")
        print(f"🍜 美食推荐: {'开启' if food_enabled else '关闭'}")
        print("=" * 60)
    
    def register_tool(self, name: str, func: Callable):
        """注册工具到Agent"""
        self.tools[name] = func
        print(f"[系统] 工具 '{name}' 已加载")
    
    def log_step(self, status: ActionStatus, content: str, details: Any = None):
        """记录执行步骤"""
        step = {
            "status": status,
            "content": content,
            "details": details
        }
        self.history.append(step)
        
        if details:
            print(f"{status.value}: {content}")
            print(f"   └── {details}")
        else:
            print(f"{status.value}: {content}")
    
    def think(self, thought: str):
        """思考步骤"""
        self.log_step(ActionStatus.THINKING, thought)
    
    def act(self, tool_name: str, **kwargs) -> Any:
        """执行工具"""
        if tool_name not in self.tools:
            raise ValueError(f"未知工具: {tool_name}")
        
        action_desc = f"调用 {tool_name}({', '.join([f'{k}={v}' for k, v in kwargs.items()])})"
        self.log_step(ActionStatus.ACTING, action_desc)
        
        # 执行工具
        result = self.tools[tool_name](**kwargs)
        
        self.log_step(ActionStatus.OBSERVING, f"{tool_name} 返回结果", result)
        
        return result
    
    def run(self) -> Dict[str, Any]:
        """
        运行ReAct循环
        根据用户输入智能决定调用哪些工具
        """
        print("\n" + "🔄" * 30)
        print("开始ReAct规划循环...")
        print("🔄" * 30 + "\n")
        
        # ========== Step 1: 规划路线 ==========
        self.think(
            f"用户有{len(self.points)}个景点需要在{self.days}天内游玩，"
            f"我需要先规划最优路线顺序。"
        )
        self.route_data = self.act("plan_route", points_list=self.points, days=self.days)
        optimized_route = self.route_data.get("route", self.points)
        
        # ========== Step 2: 查询天气 ==========
        self.think(
            f"路线已规划为: {' → '.join(optimized_route)}，"
            f"现在需要查询目的地的天气情况。"
        )
        # 使用第一个景点所在城市（简化处理）
        city = self._extract_city(optimized_route[0])
        self.weather_data = self.act("get_weather", city=city, days=self.days)
        
        # ========== Step 3: 查询各景点人流 ==========
        self.think(
            "需要了解各个景点的拥挤程度，以便合理安排时间。"
        )
        crowd_results = {}
        for point in optimized_route:
            result = self.act("get_crowd", attraction_name=point, date="today")
            crowd_results[point] = result
        self.crowd_data = crowd_results
        
        # 计算平均拥挤程度
        crowd_levels = [r.get("level", "适中") for r in crowd_results.values()]
        avg_crowd = self._average_crowd(crowd_levels)
        
        # ========== Step 4: 计算游玩时间 ==========
        self.think(
            f"已获取各景点人流情况，现在需要计算总游玩时间。"
            f"整体拥挤程度: {avg_crowd}"
        )
        self.time_data = self.act(
            "calculate_time", 
            route=optimized_route, 
            crowd_level=avg_crowd
        )
        
        # ========== Step 5: 美食推荐（可选） ==========
        self.food_data = {}
        if self.food_enabled:
            self.think(
                "用户开启了美食推荐，需要为每个景点推荐附近餐厅。"
            )
            food_results = {}
            for point in optimized_route:
                result = self.act("recommend_food", attraction_name=point)
                food_results[point] = result
            self.food_data = food_results
        else:
            self.think("用户未开启美食推荐，跳过此步骤。")
        
        # ========== 生成最终攻略 ==========
        self.think("所有数据收集完成，正在生成完整旅行攻略...")
        
        itinerary = self._generate_itinerary(optimized_route)
        
        self.log_step(ActionStatus.FINISHED, "旅行规划完成！")
        
        return {
            "budget": self.budget,
            "days": self.days,
            "route": optimized_route,
            "weather": self.weather_data,
            "crowd": self.crowd_data,
            "time": self.time_data,
            "food": self.food_data if self.food_enabled else None,
            "itinerary": itinerary,
            "total_cost_estimate": self._estimate_cost()
        }
    
    def _extract_city(self, attraction: str) -> str:
        """从景点名提取城市（简化版）"""
        city_map = {
            "故宫": "北京", "长城": "北京", "颐和园": "北京", "天安门": "北京",
            "外滩": "上海", "东方明珠": "上海", "迪士尼": "上海",
            "西湖": "杭州", "灵隐寺": "杭州",
            "兵马俑": "西安", "大雁塔": "西安",
        }
        return city_map.get(attraction, "北京")
    
    def _average_crowd(self, levels: List[str]) -> str:
        """计算平均拥挤程度"""
        score_map = {"稀疏": 1, "适中": 2, "拥挤": 3}
        scores = [score_map.get(l, 2) for l in levels]
        avg = sum(scores) / len(scores) if scores else 2
        
        if avg <= 1.5:
            return "稀疏"
        elif avg <= 2.5:
            return "适中"
        else:
            return "拥挤"
    
    def _generate_itinerary(self, route: List[str]) -> List[Dict]:
        """生成每日行程"""
        itinerary = []
        points_per_day = max(1, len(route) // self.days)
        
        for day in range(self.days):
            start_idx = day * points_per_day
            end_idx = min(start_idx + points_per_day, len(route))
            day_points = route[start_idx:end_idx]
            
            if not day_points:
                break
            
            day_plan = {
                "day": day + 1,
                "attractions": day_points,
                "weather": self.weather_data.get("forecast", [{}])[day] if self.weather_data.get("forecast") else {},
                "estimated_time": self.time_data.get("time_per_attraction", {}).get(day_points[0], 3),
            }
            
            if self.food_enabled and self.food_data:
                day_plan["food"] = {p: self.food_data.get(p, {}) for p in day_points}
            
            itinerary.append(day_plan)
        
        # 如果有剩余景点，加到最后一天
        remaining = len(route) - sum(len(d["attractions"]) for d in itinerary)
        if remaining > 0 and itinerary:
            itinerary[-1]["attractions"].extend(route[-remaining:])
        
        return itinerary
    
    def _estimate_cost(self) -> Dict[str, int]:
        """估算费用"""
        base_cost = len(self.points) * 50  # 门票
        food_cost = self.days * 150 if self.food_enabled else self.days * 80
        transport_cost = len(self.points) * 30
        
        return {
            "tickets": base_cost,
            "food": food_cost,
            "transport": transport_cost,
            "total": base_cost + food_cost + transport_cost,
            "within_budget": (base_cost + food_cost + transport_cost) <= self.budget
        }
