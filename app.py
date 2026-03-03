"""
智能旅行规划Agent - Streamlit Web界面
"""
import streamlit as st
import json
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food

# 页面配置
st.set_page_config(
    page_title="🌍 智能旅行规划Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-thinking {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .step-acting {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .step-observing {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .info-card {
        background: #f8f9fa;
        border-left: 4px solid #1E88E5;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_agent(budget, points, days, food_enabled):
    """初始化Agent并注册工具"""
    agent = ReActAgent(budget, points, days, food_enabled)
    
    # 注册工具
    agent.register_tool("get_weather", get_weather)
    agent.register_tool("get_crowd", get_crowd)
    agent.register_tool("plan_route", plan_route)
    agent.register_tool("calculate_time", calculate_time)
    agent.register_tool("recommend_food", recommend_food)
    
    return agent

def display_react_steps(history):
    """展示ReAct执行步骤"""
    st.markdown("### 🔄 ReAct执行过程")
    
    for step in history:
        status = step["status"]
        content = step["content"]
        details = step.get("details")
        
        if "思考" in status.value:
            with st.container():
                st.markdown(f"""
                    <div class="step-thinking">
                        🧠 <strong>思考</strong><br>{content}
                    </div>
                """, unsafe_allow_html=True)
        
        elif "行动" in status.value:
            with st.container():
                st.markdown(f"""
                    <div class="step-acting">
                        🔧 <strong>行动</strong><br>{content}
                    </div>
                """, unsafe_allow_html=True)
        
        elif "结果" in status.value:
            with st.container():
                st.markdown(f"""
                    <div class="step-observing">
                        📊 <strong>结果</strong><br>{content}
                    </div>
                """, unsafe_allow_html=True)
                if details:
                    with st.expander("查看详情"):
                        st.json(details)

def display_itinerary(result):
    """展示行程规划"""
    st.markdown("---")
    st.markdown("## 📅 完整旅行攻略")
    
    # 概览卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 预算", f"{result['budget']}元")
    with col2:
        st.metric("📅 天数", f"{result['days']}天")
    with col3:
        total_time = result['time'].get('total_hours', 0)
        st.metric("⏱️ 总耗时", f"{total_time}小时")
    with col4:
        cost = result['total_cost_estimate']
        st.metric("💵 预估费用", f"{cost['total']}元", 
                 delta="✅ 在预算内" if cost['within_budget'] else "⚠️ 超出预算")
    
    # 路线展示
    st.markdown("### 🗺️ 优化路线")
    route = result['route']
    route_str = " → ".join([f"**{p}**" for p in route])
    st.markdown(f"<div class='info-card'>{route_str}</div>", unsafe_allow_html=True)
    
    # 天气信息
    st.markdown("### 🌤️ 天气预报")
    weather = result['weather']
    if weather.get('forecast'):
        weather_cols = st.columns(len(weather['forecast']))
        for i, day in enumerate(weather['forecast']):
            with weather_cols[i]:
                st.markdown(f"""
                    <div style='background: #e3f2fd; padding: 1rem; border-radius: 10px; text-align: center;'>
                        <strong>第{day['day']}天</strong><br>
                        {day['condition']}<br>
                        🌡️ {day['temp_low']}°C ~ {day['temp_high']}°C<br>
                        <small>{day['suggestion']}</small>
                    </div>
                """, unsafe_allow_html=True)
    
    # 每日行程
    st.markdown("### 📍 每日行程")
    for day_plan in result['itinerary']:
        with st.expander(f"第 {day_plan['day']} 天 - {' → '.join(day_plan['attractions'])}"):
            for attraction in day_plan['attractions']:
                st.markdown(f"**📍 {attraction}**")
                
                # 人流信息
                crowd = result['crowd'].get(attraction, {})
                if crowd:
                    level = crowd.get('level', '未知')
                    emoji = {"稀疏": "🟢", "适中": "🟡", "拥挤": "🔴"}.get(level, "⚪")
                    st.markdown(f"{emoji} 人流: {level} | 等待约 {crowd.get('estimated_wait_minutes', 0)} 分钟")
                
                # 美食推荐
                if result['food'] and attraction in result['food']:
                    food_data = result['food'][attraction]
                    if food_data.get('recommendations'):
                        st.markdown("🍜 **附近美食:**")
                        for i, restaurant in enumerate(food_data['recommendations'][:2], 1):
                            st.markdown(f"   {i}. {restaurant['name']} ({restaurant['type']}) ⭐{restaurant['rating']} 💰{restaurant['price']}元")
    
    # 费用明细
    st.markdown("### 💳 费用明细")
    cost = result['total_cost_estimate']
    cost_cols = st.columns(4)
    with cost_cols[0]:
        st.info(f"门票: {cost['tickets']}元")
    with cost_cols[1]:
        st.info(f"餐饮: {cost['food']}元")
    with cost_cols[2]:
        st.info(f"交通: {cost['transport']}元")
    with cost_cols[3]:
        st.success(f"总计: {cost['total']}元")
    
    # 导出功能
    st.markdown("### 📥 导出攻略")
    if st.button("导出为JSON"):
        json_str = json.dumps(result, ensure_ascii=False, indent=2)
        st.download_button(
            label="下载JSON文件",
            data=json_str,
            file_name=f"travel_plan_{result['days']}days.json",
            mime="application/json"
        )

def main():
    """主函数"""
    # 标题
    st.markdown('<div class="main-header">🌍 智能旅行规划Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">基于ReAct架构 | 智能规划 | 实时推荐</div>', unsafe_allow_html=True)
    
    # 侧边栏输入
    with st.sidebar:
        st.markdown("## ⚙️ 旅行配置")
        
        # 1. 预算输入
        budget = st.number_input(
            "💰 预算 (元)",
            min_value=100,
            max_value=50000,
            value=2000,
            step=100,
            help="您的旅行总预算"
        )
        
        # 2. 路线途经点
        st.markdown("### 📍 选择景点")
        
        # 预设城市景点
        cities = {
            "北京": ["故宫", "长城", "颐和园", "天安门", "天坛", "圆明园", "恭王府", "鸟巢", "水立方"],
            "上海": ["外滩", "东方明珠", "迪士尼", "豫园"],
            "杭州": ["西湖", "灵隐寺", "雷峰塔", "宋城"],
            "西安": ["兵马俑", "大雁塔", "华清池", "城墙"]
        }
        
        selected_city = st.selectbox("选择城市", list(cities.keys()))
        selected_points = st.multiselect(
            "选择想去的景点",
            cities[selected_city],
            default=cities[selected_city][:2]
        )
        
        # 自定义景点输入
        custom_points = st.text_input(
            "添加自定义景点（用逗号分隔）",
            placeholder="如: 798艺术区,南锣鼓巷"
        )
        
        # 合并景点列表
        if custom_points:
            custom_list = [p.strip() for p in custom_points.split(",") if p.strip()]
            selected_points.extend(custom_list)
        
        # 3. 时间输入
        days = st.slider(
            "📅 游玩天数",
            min_value=1,
            max_value=7,
            value=2,
            help="计划游玩的天数"
        )
        
        # 4. 美食推荐开关
        food_enabled = st.toggle(
            "🍜 开启美食推荐",
            value=True,
            help="是否为每个景点推荐附近餐厅"
        )
        
        # 开始规划按钮
        st.markdown("---")
        start_planning = st.button("🚀 开始智能规划", type="primary", use_container_width=True)
    
    # 主界面
    if start_planning:
        if not selected_points:
            st.error("⚠️ 请至少选择一个景点！")
            return
        
        # 显示输入摘要
        st.markdown("### 📝 您的旅行需求")
        st.markdown(f"""
        - 💰 预算: **{budget}元**
        - 📍 途经点: **{' → '.join(selected_points)}**
        - 📅 时间: **{days}天**
        - 🍜 美食推荐: **{'开启' if food_enabled else '关闭'}**
        """)
        
        # 创建进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 初始化Agent
        status_text.text("正在初始化智能Agent...")
        progress_bar.progress(10)
        
        agent = init_agent(budget, selected_points, days, food_enabled)
        
        # 捕获输出
        import sys
        from io import StringIO
        
        # 运行Agent
        status_text.text("正在执行ReAct规划循环...")
        progress_bar.progress(30)
        
        # 执行规划
        result = agent.run()
        
        progress_bar.progress(100)
        status_text.text("规划完成！")
        
        # 显示ReAct步骤
        display_react_steps(agent.history)
        
        # 显示完整攻略
        display_itinerary(result)
        
    else:
        # 欢迎页面
        st.markdown("""
        ### 👋 欢迎使用智能旅行规划Agent！
        
        本Agent基于 **ReAct (Reasoning + Acting)** 架构，能够：
        
        1. 🧠 **智能思考** - 分析您的需求，制定规划策略
        2. 🔧 **工具调用** - 自动查询天气、人流、路线等信息
        3. 📊 **结果整合** - 生成完整的旅行攻略
        
        #### 使用步骤：
        1. 在左侧侧边栏配置您的旅行需求
        2. 点击 **"开始智能规划"** 按钮
        3. 观察Agent的ReAct思考过程
        4. 获取完整的个性化旅行攻略
        
        #### 支持的景点城市：
        - 北京: 故宫、长城、颐和园、天安门、天坛等
        - 上海: 外滩、东方明珠、迪士尼、豫园
        - 杭州: 西湖、灵隐寺、雷峰塔、宋城
        - 西安: 兵马俑、大雁塔、华清池、城墙
        
        开始规划您的旅程吧！✈️
        """)
        
        # 展示架构图
        st.markdown("### 🏗️ ReAct架构示意图")
        st.markdown("""
        ```
        ┌─────────────────────────────────────────────────────────────┐
        │                      ReAct Agent                            │
        ├─────────────────────────────────────────────────────────────┤
        │                                                             │
        │   🧠 思考 (Thought)                                         │
        │      ↓ "需要规划路线，查询天气和人流量"                       │
        │   🔧 行动 (Action)                                          │
        │      ↓ 调用工具: plan_route, get_weather, get_crowd         │
        │   📊 观察 (Observation)                                     │
        │      ↓ 收集结果，整合信息                                    │
        │   🔄 循环...                                                │
        │                                                             │
        │   ✅ 完成 → 输出完整旅行攻略                                 │
        │                                                             │
        └─────────────────────────────────────────────────────────────┘
        ```
        """)

if __name__ == "__main__":
    main()
