# 🌸 范の旅行小助手

基于ReAct (Reasoning + Acting) 架构的智能旅行规划系统，支持**多城市旅行规划**、**机票酒店价格优化**、**美食反向搜索**，覆盖**全国300+城市**。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Cities](https://img.shields.io/badge/城市-300+-orange.svg)
![MultiCity](https://img.shields.io/badge/多城市-支持-purple.svg)
![Food](https://img.shields.io/badge/美食反向搜索-支持-green.svg)
![AutoUpdate](https://img.shields.io/badge/自动更新-每周一-yellow.svg)

## ✨ 核心特性

- 🧠 **ReAct架构** - 智能思考+行动循环，每一步清晰可见
- 🏙️ **多城市规划** - 一次旅行规划多个城市，自动优化路线
- ✈️ **机票酒店优化** - 根据实时价格规划最经济的旅行方案
- 🍜 **美食反向搜索** - 输入美食名称，找到最地道的城市
- 🏞️ **动态背景** - 根据选择的城市自动切换风景背景
- 🌤️ **天气查询** - 实时天气预报和出行建议
- 👥 **人流预测** - 景点拥挤程度分析和错峰建议
- 📊 **美团/大众点评** - 美食推荐参考真实榜单数据
- ⏱️ **时间规划** - 精确计算游玩和交通时间
- 🔄 **自动更新** - 每周一自动更新数据库内容

## 📁 项目结构

```
travel-agent/
├── main.py                 # ReActAgent核心类
├── app.py                  # Streamlit Web界面（范の旅行小助手）
├── tools/
│   ├── __init__.py
│   ├── cities.py           # 全国城市及景点数据库（300+城市）
│   ├── food_data.py        # 美团/大众点评美食数据
│   ├── food_search.py      # 美食反向搜索功能
│   ├── travel_costs.py     # 机票酒店价格数据及路线优化
│   ├── backgrounds.py      # 城市背景图片管理
│   ├── weather.py          # 天气查询工具
│   ├── crowd.py            # 人流查询工具
│   ├── route.py            # 路线规划工具
│   ├── time_calculator.py  # 时间计算工具
│   └── food.py             # 美食推荐工具
├── requirements.txt        # 依赖列表
├── README.md               # 项目说明
└── .gitignore             # Git忽略文件
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/cruciata/travel-agent.git
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

## 🌆 支持城市（300+）

### 直辖市
北京、上海、天津、重庆

### 热门城市
杭州、成都、西安、武汉、南京、苏州、长沙、郑州、沈阳、青岛、宁波、东莞、厦门、昆明、大连、哈尔滨、济南、南宁、长春、泉州、石家庄、贵阳、南昌、金华、常州、珠海、惠州、嘉兴、南通、中山、保定、兰州、台州、徐州、太原、绍兴、烟台、海口、乌鲁木齐、呼和浩特、银川、西宁、拉萨

### 特色旅游城市
**云南**：丽江、大理、香格里拉、西双版纳、腾冲
**四川**：九寨沟、峨眉山、稻城亚丁
**海南**：三亚、海口、万宁
**西藏**：拉萨、林芝、日喀则
**新疆**：乌鲁木齐、喀什、伊犁、阿勒泰
**其他**：张家界、桂林、黄山、三亚、厦门、青岛、哈尔滨、西安

每个城市包含10-30个热门景点，支持自定义添加。

## 🍜 美食推荐（美团/大众点评数据）

美食推荐参考以下榜单数据：

- **🏆 必吃榜** - 美团必吃榜餐厅
- **🔥 热门榜** - 大众点评热门餐厅
- **⭐ 评分** - 综合评分4.0+餐厅
- **💰 人均** - 实时人均消费
- **🏷️ 标签** - 特色标签（如：老字号、网红、排队王）

支持城市：北京、上海、成都、杭州、广州、深圳、西安、重庆、南京、武汉、长沙、厦门、青岛、哈尔滨、丽江等

## 🚀 部署到GitHub

### 方式一：使用部署脚本（推荐）

```bash
# 1. 获取GitHub Personal Access Token
# 访问 https://github.com/settings/tokens → Generate new token → 勾选 repo 权限

# 2. 运行部署脚本
./deploy.sh ghp_your_token_here
```

### 方式二：手动部署

```bash
# 1. 在GitHub上创建新仓库 (https://github.com/new)
# 仓库名: travel-agent

# 2. 添加远程仓库并推送
git remote add origin https://github.com/YOUR_USERNAME/travel-agent.git
git branch -M main
git push -u origin main
```

### 方式三：使用GitHub CLI

```bash
# 登录GitHub
gh auth login

# 创建并推送仓库
gh repo create travel-agent --public --source=. --push
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

Made with ❤️ by Travel Agent Team
