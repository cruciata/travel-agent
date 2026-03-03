# 🌍 智能旅行规划Agent

基于ReAct (Reasoning + Acting) 架构的智能旅行规划系统，能够根据用户需求自动规划最优路线、查询天气人流、推荐美食。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 特性

- 🧠 **ReAct架构** - 智能思考+行动循环，每一步清晰可见
- 🗺️ **路线优化** - 基于贪心算法自动规划最优游览顺序
- 🌤️ **天气查询** - 实时天气预报和出行建议
- 👥 **人流预测** - 景点拥挤程度分析和错峰建议
- 🍜 **美食推荐** - 智能推荐附近高分餐厅
- ⏱️ **时间规划** - 精确计算游玩和交通时间
- 🎨 **友好界面** - 基于Streamlit的美观Web界面

## 📁 项目结构

```
travel-agent/
├── main.py              # ReActAgent核心类
├── tools/
│   ├── __init__.py
│   ├── weather.py       # 天气查询工具
│   ├── crowd.py         # 人流查询工具
│   ├── route.py         # 路线规划工具
│   ├── time_calculator.py # 时间计算工具
│   └── food.py          # 美食推荐工具
├── app.py               # Streamlit Web界面
├── requirements.txt     # 依赖列表
├── README.md            # 项目说明
└── .gitignore          # Git忽略文件
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/[your-username]/travel-agent.git
cd travel-agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
streamlit run app.py
```

然后在浏览器中打开 `http://localhost:8501`

## 📖 使用指南

### Web界面使用

1. 在左侧侧边栏输入您的旅行配置：
   - 💰 **预算**：旅行总预算（元）
   - 📍 **景点**：选择想去的景点（支持多选和自定义）
   - 📅 **天数**：计划游玩天数
   - 🍜 **美食推荐**：是否开启美食推荐

2. 点击 **"开始智能规划"** 按钮

3. 观察Agent的ReAct执行过程：
   - 🧠 思考步骤
   - 🔧 行动步骤
   - 📊 结果观察

4. 获取完整的旅行攻略，包括：
   - 优化后的游览路线
   - 每日天气预报
   - 景点人流分析
   - 附近美食推荐
   - 费用明细估算

### 程序化使用

```python
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food

# 创建Agent实例
agent = ReActAgent(
    budget=2000,
    points=["故宫", "长城", "颐和园"],
    days=3,
    food_enabled=True
)

# 注册工具
agent.register_tool("get_weather", get_weather)
agent.register_tool("get_crowd", get_crowd)
agent.register_tool("plan_route", plan_route)
agent.register_tool("calculate_time", calculate_time)
agent.register_tool("recommend_food", recommend_food)

# 运行规划
result = agent.run()

# 查看结果
print(result)
```

## 🔧 工具说明

| 工具名 | 功能 | 输入参数 | 输出 |
|:---|:---|:---|:---|
| `get_weather` | 查询天气 | city, days | 每天天气状况 |
| `get_crowd` | 查景点人数 | attraction_name, date | 拥挤程度 |
| `plan_route` | 规划路线 | points_list, days | 最优路线顺序 |
| `calculate_time` | 计算游玩时间 | route, crowd_level | 总耗时 |
| `recommend_food` | 推荐美食 | attraction_name | 附近3家餐厅 |

## 🏗️ ReAct架构

```
┌─────────────────────────────────────────────────────────┐
│                    ReAct Agent                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   🧠 思考 (Thought)                                     │
│      ↓ 分析问题，确定下一步行动                          │
│   🔧 行动 (Action)                                      │
│      ↓ 调用相应工具获取信息                              │
│   📊 观察 (Observation)                                 │
│      ↓ 整合结果，更新知识                                │
│   🔄 循环直到目标完成                                    │
│                                                         │
│   ✅ 输出最终答案                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🌆 支持城市

- **北京**：故宫、长城、颐和园、天安门、天坛、圆明园、恭王府、鸟巢、水立方
- **上海**：外滩、东方明珠、迪士尼、豫园
- **杭州**：西湖、灵隐寺、雷峰塔、宋城
- **西安**：兵马俑、大雁塔、华清池、城墙

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

Made with ❤️ by Travel Agent Team
