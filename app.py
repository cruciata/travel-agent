"""
智能旅行规划Agent - Streamlit Web界面（支持全国城市）
"""
import streamlit as st
import json
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_all_cities, get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city

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
    .city-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .food-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .rank-badge {
        background: #ff6b6b;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
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

def display_city_food(city):
    """展示城市美食推荐（美团/大众点评风格）"""
    food_data = get_food_for_city(city)
    
    st.markdown(f"### 🍜 {city}美食推荐")
    st.markdown("<small>数据参考：美团必吃榜、大众点评热门榜</small>", unsafe_allow_html=True)
    
    # 必吃榜
    if food_data.get("must_eat"):
        st.markdown("**🏆 必吃榜**")
        for i, restaurant in enumerate(food_data["must_eat"][:3], 1):
            rank_badge = f'<span class="rank-badge">{restaurant.get("rank", "")}</span>' if restaurant.get("rank") else ""
            tags = " ".join([f'<span style="background:#f0f0f0;padding:2px 8px;border-radius:10px;font-size:0.8rem;margin-right:5px;">{tag}</span>' for tag in restaurant.get("tags", [])])
            
            st.markdown(f"""
            <div class="food-card">
                {rank_badge}
                <strong>{restaurant['name']}</strong> 
                <span style="color:#ff9500;">{'⭐' * int(restaurant['rating'])}</span> {restaurant['rating']}
                <span style="color:#666;float:right;">💰 {restaurant['price']}元/人</span>
                <br>
                <small>{restaurant['type']} | {tags}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # 热门榜
    if food_data.get("hot"):
        st.markdown("**🔥 热门榜**")
        for restaurant in food_data["hot"][:2]:
            tags = " ".join([f'<span style="background:#f0f0f0;padding:2px 8px;border-radius:10px;font-size:0.8rem;margin-right:5px;">{tag}</span>' for tag in restaurant.get("tags", [])])
            
            st.markdown(f"""
            <div class="food-card">
                <strong>{restaurant['name']}</strong> 
                <span style="color:#ff9500;">{'⭐' * int(restaurant['rating'])}</span> {restaurant['rating']}
                <span style="color:#666;float:right;">💰 {restaurant['price']}元/人</span>
                <br>
                <small>{restaurant['type']} | {tags}</small>
            </div>
            """, unsafe_allow_html=True)

def display_itinerary(result, city):
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
        weather_cols = st.columns(min(len(weather['forecast']), 7))
        for i, day in enumerate(weather['forecast']):
            if i < len(weather_cols):
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
        attractions = day_plan['attractions']
        attractions_str = " → ".join(attractions)
        with st.expander(f"第 {day_plan['day']} 天 - {attractions_str}"):
            for attraction in attractions:
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
    
    # 城市美食推荐（美团/大众点评风格）
    if city:
        display_city_food(city)
    
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
    st.markdown('<div class="sub-header">基于ReAct架构 | 覆盖全国城市 | 美团/大众点评美食推荐</div>', unsafe_allow_html=True)
    
    # 初始化session state
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = None
    if 'search_keyword' not in st.session_state:
        st.session_state.search_keyword = ""
    
    # 侧边栏输入
    with st.sidebar:
        st.markdown("## ⚙️ 旅行配置")
        
        # 1. 城市选择（支持搜索）
        st.markdown("### 🏙️ 选择城市")
        
        # 搜索城市
        search_keyword = st.text_input(
            "🔍 搜索城市",
            placeholder="输入城市名，如：成都、厦门、青岛...",
            help="支持全国300+城市搜索"
        )
        
        # 热门城市快捷选择
        st.markdown("<small>热门城市：</small>", unsafe_allow_html=True)
        popular_cols = st.columns(5)
        for i, city in enumerate(POPULAR_CITIES[:10]):
            with popular_cols[i % 5]:
                if st.button(city, key=f"pop_{city}", use_container_width=True):
                    st.session_state.selected_city = city
                    st.session_state.search_keyword = ""
                    st.rerun()
        
        # 搜索结果
        selected_city = None
        if search_keyword:
            matched_cities = search_cities(search_keyword)
            if matched_cities:
                selected_city = st.selectbox(
                    f"找到 {len(matched_cities)} 个城市",
                    matched_cities,
                    key="search_result"
                )
            else:
                st.warning(f"未找到 '{search_keyword}' 相关城市")
        
        # 如果没有搜索选择，使用session state中的城市
        if not selected_city and st.session_state.selected_city:
            selected_city = st.session_state.selected_city
        
        # 显示当前选择
        if selected_city:
            st.success(f"📍 已选择：{selected_city}")
            st.session_state.selected_city = selected_city
        
        # 2. 预算输入
        budget = st.number_input(
            "💰 预算 (元)",
            min_value=100,
            max_value=50000,
            value=2000,
            step=100,
            help="您的旅行总预算"
        )
        
        # 3. 路线途经点（根据城市动态生成）
        st.markdown("### 📍 选择景点")
        
        if selected_city:
            attractions = get_attractions(selected_city)
            if attractions:
                selected_points = st.multiselect(
                    f"{selected_city}的热门景点（可多选）",
                    attractions,
                    default=attractions[:2] if len(attractions) >= 2 else attractions,
                    help=f"{selected_city}共有{len(attractions)}个推荐景点"
                )
            else:
                st.warning(f"暂无{selected_city}的景点数据")
                selected_points = []
        else:
            st.info("👆 请先选择城市")
            selected_points = []
        
        # 自定义景点输入
        custom_points = st.text_input(
            "添加自定义景点（用逗号分隔）",
            placeholder="如: 某某公园,某某街"
        )
        
        # 合并景点列表
        if custom_points:
            custom_list = [p.strip() for p in custom_points.split(",") if p.strip()]
            selected_points.extend(custom_list)
        
        # 4. 时间输入
        days = st.slider(
            "📅 游玩天数",
            min_value=1,
            max_value=7,
            value=2,
            help="计划游玩的天数"
        )
        
        # 5. 美食推荐开关
        food_enabled = st.toggle(
            "🍜 开启美食推荐",
            value=True,
            help="参考美团必吃榜、大众点评热门榜推荐餐厅"
        )
        
        # 开始规划按钮
        st.markdown("---")
        start_planning = st.button("🚀 开始智能规划", type="primary", use_container_width=True)
    
    # 主界面
    if start_planning:
        if not selected_city:
            st.error("⚠️ 请先选择城市！")
            return
        
        if not selected_points:
            st.error("⚠️ 请至少选择一个景点！")
            return
        
        # 显示输入摘要
        st.markdown("### 📝 您的旅行需求")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("城市", selected_city)
        with col2:
            st.metric("预算", f"{budget}元")
        with col3:
            st.metric("天数", f"{days}天")
        with col4:
            st.metric("景点数", len(selected_points))
        
        st.markdown(f"**📍 途经点**: {' → '.join(selected_points)}")
        st.markdown(f"**🍜 美食推荐**: {'开启（参考美团/大众点评）' if food_enabled else '关闭'}")
        
        # 创建进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 初始化Agent
        status_text.text("正在初始化智能Agent...")
        progress_bar.progress(10)
        
        agent = init_agent(budget, selected_points, days, food_enabled)
        
        # 运行Agent
        status_text.text("正在执行ReAct规划循环...")
        progress_bar.progress(30)
        
        result = agent.run()
        
        progress_bar.progress(100)
        status_text.text("规划完成！")
        
        # 显示ReAct步骤
        display_react_steps(agent.history)
        
        # 显示完整攻略
        display_itinerary(result, selected_city)
        
    else:
        # 欢迎页面
        st.markdown("""
        ### 👋 欢迎使用智能旅行规划Agent！
        
        本Agent基于 **ReAct (Reasoning + Acting)** 架构，支持**全国300+城市**：
        
        **🌟 核心功能：**
        1. 🧠 **智能思考** - 分析您的需求，制定规划策略
        2. 🔧 **工具调用** - 自动查询天气、人流、路线等信息
        3. 📊 **结果整合** - 生成完整的旅行攻略
        
        **🏙️ 城市覆盖：**
        - 北京、上海、广州、深圳、成都、杭州、西安、重庆、武汉、南京
        - 以及全国所有省份的地级市
        
        **🍜 美食推荐：**
        - 参考 **美团必吃榜**、**大众点评热门榜**
        - 覆盖必吃榜、热门榜、本地特色
        
        **📍 景点数据：**
        - 每个城市包含10-30个热门景点
        - 支持自定义添加景点
        
        ---
        
        ### 🚀 使用步骤：
        1. 在左侧侧边栏搜索或选择城市
        2. 配置预算、选择景点、设置天数
        3. 点击 **"开始智能规划"** 按钮
        4. 获取完整的个性化旅行攻略
        
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
        
        # 数据覆盖展示
        st.markdown("### 📊 数据覆盖")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("覆盖城市", len(get_all_cities()))
        with col2:
            total_attractions = sum(len(get_attractions(city)) for city in get_all_cities())
            st.metric("景点数量", total_attractions)
        with col3:
            st.metric("美食数据", "美团+大众点评")

if __name__ == "__main__":
    main()
