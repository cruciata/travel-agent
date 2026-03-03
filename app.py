"""
范の旅行小助手 - Google风格简约3D界面
"""
import streamlit as st
import json
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_all_cities, get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city
from tools.travel_costs import plan_multi_city_route, optimize_route_by_budget, get_flight_price, get_hotel_price
from tools.food_search import search_cities_by_food, get_food_recommendations, get_city_signature_foods
from tools.backgrounds import get_city_background, get_multi_city_background

# 页面配置
st.set_page_config(
    page_title="范の旅行小助手",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google风格3D CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

<style>
    /* 全局字体 */
    * {
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* 纯白背景 */
    .stApp {
        background: #ffffff !important;
    }
    
    /* 主内容区域 */
    .main .block-container {
        background: #ffffff;
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* 侧边栏 - Material Design风格 */
    [data-testid="stSidebar"] {
        background: #f8f9fa !important;
        border-right: 1px solid #dadce0;
    }
    
    [data-testid="stSidebar"] .block-container {
        background: #f8f9fa !important;
    }
    
    /* 标题样式 - Google品牌色 */
    h1 {
        color: #202124 !important;
        font-weight: 400 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #202124 !important;
        font-weight: 400 !important;
        font-size: 1.75rem !important;
    }
    
    h3 {
        color: #5f6368 !important;
        font-weight: 500 !important;
        font-size: 1.25rem !important;
    }
    
    /* 品牌色点缀 */
    .google-blue { color: #4285f4; }
    .google-red { color: #ea4335; }
    .google-yellow { color: #fbbc04; }
    .google-green { color: #34a853; }
    
    /* 按钮 - Material Design风格 + 3D效果 */
    .stButton > button {
        background: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 1px 2px rgba(60,64,67,0.3), 
                    0 1px 3px rgba(60,64,67,0.15),
                    0 2px 4px rgba(0,0,0,0.1) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        transform-style: preserve-3d;
    }
    
    .stButton > button:hover {
        background: #1557b0 !important;
        box-shadow: 0 4px 8px rgba(60,64,67,0.3),
                    0 2px 4px rgba(60,64,67,0.2),
                    0 8px 16px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) translateZ(10px);
    }
    
    .stButton > button:active {
        transform: translateY(0) translateZ(0);
        box-shadow: 0 1px 2px rgba(60,64,67,0.3) !important;
    }
    
    /* 次要按钮 */
    .secondary-btn > button {
        background: #ffffff !important;
        color: #1a73e8 !important;
        border: 1px solid #dadce0 !important;
    }
    
    .secondary-btn > button:hover {
        background: #f8f9fa !important;
        border-color: #1a73e8 !important;
    }
    
    /* 危险/删除按钮 - 红色 */
    .danger-btn > button {
        background: #ea4335 !important;
    }
    
    .danger-btn > button:hover {
        background: #d33b28 !important;
    }
    
    /* 成功按钮 - 绿色 */
    .success-btn > button {
        background: #34a853 !important;
    }
    
    .success-btn > button:hover {
        background: #2d8e47 !important;
    }
    
    /* 输入框 - Material风格 + 3D */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px rgba(26,115,232,0.2),
                    inset 0 1px 2px rgba(0,0,0,0.05) !important;
        outline: none;
    }
    
    /* 选择框 */
    .stSelectbox > div > div {
        background: #ffffff !important;
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* 多选框卡片 - 3D效果 */
    .stMultiSelect > div {
        background: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 滑块 - Material风格 */
    .stSlider > div > div > div {
        background: #e8eaed !important;
    }
    
    .stSlider > div > div > div > div {
        background: #1a73e8 !important;
    }
    
    /* 卡片 - 简约3D */
    .card-3d {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 1px 2px rgba(60,64,67,0.3),
                    0 2px 6px rgba(60,64,67,0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #e8eaed;
    }
    
    .card-3d:hover {
        box-shadow: 0 4px 12px rgba(60,64,67,0.3),
                    0 8px 24px rgba(60,64,67,0.2);
        transform: translateY(-4px);
    }
    
    /* 城市卡片 - 品牌色边框 */
    .city-card {
        background: #ffffff;
        border: 2px solid #e8eaed;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .city-card:hover {
        border-color: #1a73e8;
        box-shadow: 0 4px 12px rgba(26,115,232,0.2);
        transform: translateY(-2px);
    }
    
    .city-card.selected {
        border-color: #34a853;
        background: #e6f4ea;
        box-shadow: 0 2px 8px rgba(52,168,83,0.3);
    }
    
    /* 信息卡片 - 品牌色 */
    .info-card {
        background: #e8f0fe;
        border-left: 4px solid #4285f4;
        border-radius: 0 8px 8px 0;
        padding: 16px;
    }
    
    .warning-card {
        background: #fef3e8;
        border-left: 4px solid #fbbc04;
    }
    
    .error-card {
        background: #fce8e6;
        border-left: 4px solid #ea4335;
    }
    
    .success-card {
        background: #e6f4ea;
        border-left: 4px solid #34a853;
    }
    
    /* 步骤指示器 - ReAct */
    .step-thinking {
        background: #e8f0fe;
        border-left: 4px solid #4285f4;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .step-acting {
        background: #fef3e8;
        border-left: 4px solid #fbbc04;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .step-observing {
        background: #e6f4ea;
        border-left: 4px solid #34a853;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    
    /* 图标按钮 - Material Icons */
    .icon-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
        margin: 2px;
    }
    
    .tag-blue {
        background: #e8f0fe;
        color: #1967d2;
    }
    
    .tag-red {
        background: #fce8e6;
        color: #d93025;
    }
    
    .tag-green {
        background: #e6f4ea;
        color: #188038;
    }
    
    .tag-yellow {
        background: #fef3e8;
        color: #b06000;
    }
    
    /* 导航标签 */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #1a73e8 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 折叠面板 */
    .streamlit-expanderHeader {
        background: #f8f9fa !important;
        border-radius: 8px;
        font-weight: 500;
        border: 1px solid #e8eaed;
    }
    
    /* 进度条 - Google蓝 */
    .stProgress > div > div > div {
        background: #1a73e8 !important;
    }
    
    /* 度量卡片 - 简约风格 */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 400 !important;
        color: #202124 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #5f6368 !important;
        font-size: 14px !important;
    }
    
    /* 开关 - Material风格 */
    .stToggle [role="switch"][aria-checked="true"] {
        background: #1a73e8 !important;
    }
    
    /* 分隔线 */
    hr {
        border: none;
        border-top: 1px solid #dadce0;
        margin: 24px 0;
    }
    
    /* 链接 - Google蓝 */
    a {
        color: #1a73e8 !important;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    /* 滚动条 - Material风格 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f3f4;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #dadce0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #bdc1c6;
    }
    
    /* 表格 */
    .stTable {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 3D悬浮效果 - 通用 */
    .hover-3d {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .hover-3d:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(60,64,67,0.2);
    }
    
    /* 路线步骤 - 3D卡片 */
    .route-step {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .route-step:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }
    
    /* 航班卡片 - 渐变效果 */
    .flight-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e8eaed;
        transition: all 0.3s ease;
    }
    
    .flight-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* 美食卡片 - 悬浮效果 */
    .food-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e8eaed;
    }
    
    .food-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        transform: translateY(-4px);
        border-color: #1a73e8;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
    }
    
    /* 加载动画 */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* 徽章样式 */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .badge-must-eat {
        background: #fce8e6;
        color: #c5221f;
    }
    
    .badge-hot {
        background: #fef3e8;
        color: #b06000;
    }
    
    .badge-price {
        background: #e8f0fe;
        color: #1967d2;
    }
    
    /* 头部样式 */
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #202124;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #5f6368;
        font-weight: 400;
    }
    
    /* Material Icons */
    .material-icons {
        font-family: 'Material Icons' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }
    
    /* 空状态 */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #5f6368;
    }
    
    .empty-state-icon {
        font-size: 64px;
        color: #dadce0;
        margin-bottom: 16px;
    }
    
    /* 工具提示 */
    [data-tooltip] {
        position: relative;
    }
    
    [data-tooltip]:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 12px;
        background: #3c4043;
        color: white;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'selected_cities' not in st.session_state:
    st.session_state.selected_cities = []
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False

def init_agent(budget, points, days, food_enabled):
    """初始化Agent并注册工具"""
    agent = ReActAgent(budget, points, days, food_enabled)
    agent.register_tool("get_weather", get_weather)
    agent.register_tool("get_crowd", get_crowd)
    agent.register_tool("plan_route", plan_route)
    agent.register_tool("calculate_time", calculate_time)
    agent.register_tool("recommend_food", recommend_food)
    return agent

def display_react_steps(history):
    """展示ReAct执行步骤 - Google风格"""
    st.markdown("### 🔄 ReAct执行过程")
    for step in history:
        status = step["status"]
        content = step["content"]
        with st.container():
            if "思考" in status.value:
                st.markdown(f'<div class="step-thinking"><span style="color:#4285f4;font-weight:500;">💭 思考</span><br>{content}</div>', unsafe_allow_html=True)
            elif "行动" in status.value:
                st.markdown(f'<div class="step-acting"><span style="color:#fbbc04;font-weight:500;">⚡ 行动</span><br>{content}</div>', unsafe_allow_html=True)
            elif "结果" in status.value:
                st.markdown(f'<div class="step-observing"><span style="color:#34a853;font-weight:500;">✓ 结果</span><br>{content}</div>', unsafe_allow_html=True)

def display_multi_city_plan(plan_result, budget):
    """展示多城市路线规划结果 - Google风格3D卡片"""
    st.markdown("### ✈️ 多城市路线规划")
    
    # 路线展示 - 3D步骤
    route = plan_result["route"]
    route_html = '<div style="display:flex; align-items:center; gap:16px; overflow-x:auto; padding:20px 0;">'
    for i, city in enumerate(route):
        route_html += f'''
        <div class="route-step" style="min-width:120px; text-align:center;">
            <div style="font-size:24px; font-weight:300; color:#5f6368;">{i+1}</div>
            <div style="font-size:18px; font-weight:500; color:#202124; margin-top:8px;">{city}</div>
        </div>
        '''
        if i < len(route) - 1:
            route_html += '<div style="color:#dadce0; font-size:24px;">→</div>'
    route_html += '</div>'
    st.markdown(route_html, unsafe_allow_html=True)
    
    # 航班信息 - 3D卡片
    st.markdown("#### 航班信息")
    for flight in plan_result.get("flights", []):
        st.markdown(f'''
        <div class="flight-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="font-size:18px; color:#202124;">{flight['from']} → {flight['to']}</strong>
                    <div style="color:#5f6368; font-size:14px; margin-top:4px;">
                        {flight['distance']}km · {flight['duration']}小时 · {'直飞' if flight['direct'] else '需转机'}
                    </div>
                </div>
                <div style="text-align:right;">
                    <span class="tag tag-price">¥{flight['economy']}</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # 酒店信息
    st.markdown("#### 🏨 酒店预估")
    hotel_cols = st.columns(min(len(plan_result.get("hotel_costs", {})), 4))
    for i, (city, cost) in enumerate(plan_result.get("hotel_costs", {}).items()):
        with hotel_cols[i % 4]:
            st.metric(city, f"¥{cost}")
    
    # 费用汇总 - 品牌色展示
    st.markdown("#### 💰 费用汇总")
    total_cost = plan_result.get('total_cost', 0)
    diff = plan_result.get('budget_diff', 0)
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("机票总价", f"¥{plan_result.get('total_flight_cost', 0)}")
    with cols[1]:
        st.metric("酒店总价", f"¥{plan_result.get('total_hotel_cost', 0)}")
    with cols[2]:
        st.metric("总费用", f"¥{total_cost}")
    with cols[3]:
        if diff >= 0:
            st.metric("预算剩余", f"¥{diff}", delta="在预算内", delta_color="normal")
        else:
            st.metric("超预算", f"¥{abs(diff)}", delta="超出", delta_color="inverse")

def display_city_food(city):
    """展示城市美食推荐 - Google风格"""
    food_data = get_food_for_city(city)
    st.markdown(f"### 🍴 {city}美食推荐")
    
    # 必吃榜
    if food_data.get("must_eat"):
        st.markdown("**🏆 必吃榜**")
        for restaurant in food_data["must_eat"][:3]:
            tags = " ".join([f'<span class="tag tag-blue">{tag}</span>' for tag in restaurant.get("tags", [])])
            rank = restaurant.get("rank", "")
            rank_badge = f'<span class="badge badge-must-eat">{rank}</span>' if rank else ""
            
            st.markdown(f'''
            <div class="food-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        {rank_badge}
                        <strong style="font-size:16px; color:#202124;">{restaurant['name']}</strong>
                        <div style="margin-top:4px;">{tags}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:#fbbc04; font-weight:500;">{'★' * int(restaurant['rating'])} {restaurant['rating']}</div>
                        <div style="color:#5f6368; font-size:14px;">¥{restaurant['price']}/人</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

def main():
    """主函数 - Google Material Design风格"""
    # 头部
    st.markdown('''
    <div class="header-container">
        <div class="header-title">
            <span style="color:#4285f4;">范</span><span style="color:#ea4335;">の</span><span style="color:#fbbc04;">旅</span><span style="color:#34a853;">行</span><span style="color:#4285f4;">小</span><span style="color:#ea4335;">助</span><span style="color:#fbbc04;">手</span>
        </div>
        <div class="header-subtitle">多城市智能规划 · 机票酒店优化 · 美食反向搜索</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## ⚙️ 旅行配置")
        
        tab1, tab2, tab3 = st.tabs(["🌍 城市", "🍜 美食", "💰 预算"])
        
        with tab1:
            st.markdown("### 选择城市")
            
            # 城市搜索
            search_keyword = st.text_input(
                "搜索城市",
                placeholder="输入城市名...",
                key="city_search"
            )
            
            # 搜索结果
            if search_keyword:
                matched = search_cities(search_keyword)
                if matched:
                    for city in matched[:5]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(city)
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button("添加", key=f"add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                            else:
                                st.markdown("<span style='color:#34a853;'>✓ 已选</span>", unsafe_allow_html=True)
            
            # 热门城市 - 3D卡片效果
            st.markdown("**热门城市**")
            for i in range(0, min(12, len(POPULAR_CITIES)), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(POPULAR_CITIES):
                        city = POPULAR_CITIES[i + j]
                        is_selected = city in st.session_state.selected_cities
                        with cols[j]:
                            card_class = "city-card selected" if is_selected else "city-card"
                            btn_label = f"✓ {city}" if is_selected else city
                            if st.button(btn_label, key=f"pop_{city}", use_container_width=True):
                                if is_selected:
                                    st.session_state.selected_cities.remove(city)
                                else:
                                    st.session_state.selected_cities.append(city)
                                st.rerun()
            
            # 显示已选城市
            if st.session_state.selected_cities:
                st.markdown("**已选城市**")
                for city in st.session_state.selected_cities:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"<span style='color:#34a853;'>✓ {city}</span>", unsafe_allow_html=True)
                    with col2:
                        if st.button("✕", key=f"remove_{city}"):
                            st.session_state.selected_cities.remove(city)
                            st.rerun()
        
        with tab2:
            st.markdown("### 根据美食找城市")
            
            food_search = st.text_input(
                "输入美食名称",
                placeholder="如：火锅、烤鸭、小笼包...",
                key="food_search"
            )
            
            if food_search:
                results = search_cities_by_food(food_search)
                if results:
                    st.success(f"找到 {len(results)} 个相关城市")
                    for result in results[:5]:
                        city = result["city"]
                        food = result["food"]
                        confidence = result["confidence"]
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{city}**")
                            st.caption(f"{food} · 匹配度: {'★' * int(confidence * 5)}")
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button("添加", key=f"food_add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                else:
                    st.warning("未找到相关城市，试试其他美食名称")
            
            st.markdown("---")
            st.markdown("**热门美食**")
            recommendations = get_food_recommendations()
            for rec in recommendations[:5]:
                with st.expander(f"🍽️ {rec['food']}"):
                    st.write(f"推荐城市: {', '.join(rec['cities'][:3])}")
        
        with tab3:
            budget = st.number_input(
                "总预算 (元)",
                min_value=1000,
                max_value=100000,
                value=5000,
                step=1000
            )
            
            days = st.slider(
                "总天数",
                min_value=1,
                max_value=15,
                value=5
            )
            
            food_enabled = st.toggle(
                "开启美食推荐",
                value=True
            )
        
        st.markdown("---")
        start_planning = st.button("开始规划", type="primary", use_container_width=True)
    
    # 主内容区
    if start_planning:
        if not st.session_state.selected_cities:
            st.error("请至少选择一个城市！")
            return
        
        st.session_state.plan_generated = True
        
        # 输入摘要 - 3D卡片
        st.markdown('<div class="card-3d">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("城市数", len(st.session_state.selected_cities))
        with col2:
            st.metric("预算", f"¥{budget}")
        with col3:
            st.metric("天数", f"{days}天")
        with col4:
            avg_days = days // len(st.session_state.selected_cities) if st.session_state.selected_cities else 0
            st.metric("每城平均", f"{avg_days}天")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 多城市路线规划
        if len(st.session_state.selected_cities) > 1:
            st.markdown("---")
            days_per_city = {city: max(1, days // len(st.session_state.selected_cities)) 
                           for city in st.session_state.selected_cities}
            plan_result = optimize_route_by_budget(st.session_state.selected_cities, budget, days_per_city)
            display_multi_city_plan(plan_result, budget)
        
        # 各城市详细规划
        st.markdown("---")
        st.markdown("### 📍 各城市详细攻略")
        
        for city in st.session_state.selected_cities:
            with st.expander(f"{city}攻略", expanded=False):
                attractions = get_attractions(city)
                
                if attractions:
                    selected_attractions = st.multiselect(
                        f"选择{city}的景点",
                        attractions,
                        default=attractions[:min(3, len(attractions))],
                        key=f"attr_{city}"
                    )
                    
                    if selected_attractions and st.button(f"生成{city}详细攻略", key=f"btn_{city}"):
                        city_days = max(1, days // len(st.session_state.selected_cities))
                        
                        progress_bar = st.progress(0)
                        agent = init_agent(budget // len(st.session_state.selected_cities), 
                                         selected_attractions, city_days, food_enabled)
                        
                        progress_bar.progress(50)
                        result = agent.run()
                        progress_bar.progress(100)
                        
                        display_react_steps(agent.history)
                        
                        st.markdown(f"**优化路线**: {' → '.join(result['route'])}")
                        
                        if result.get('weather', {}).get('forecast'):
                            weather_cols = st.columns(len(result['weather']['forecast']))
                            for i, day in enumerate(result['weather']['forecast']):
                                with weather_cols[i]:
                                    st.metric(f"第{day['day']}天", 
                                            f"{day['temp_high']}°C", 
                                            f"{day['condition']}")
                        
                        if food_enabled:
                            display_city_food(city)
    
    else:
        # 欢迎页面
        st.markdown('''
        <div class="card-3d">
            <h2 style="color:#202124; font-weight:400;">欢迎使用范の旅行小助手</h2>
            
            <h3 style="color:#5f6368; margin-top:24px;">核心功能</h3>
            <ul style="color:#5f6368; line-height:2;">
                <li><strong style="color:#4285f4;">多城市规划</strong> - 一次旅行规划多个城市，自动优化路线</li>
                <li><strong style="color:#34a853;">机票酒店优化</strong> - 根据实时价格规划最经济的方案</li>
                <li><strong style="color:#fbbc04;">美食反向搜索</strong> - 输入美食名称，找到最地道的城市</li>
                <li><strong style="color:#ea4335;">300+城市</strong> - 覆盖全国热门旅游城市</li>
            </ul>
            
            <h3 style="color:#5f6368; margin-top:24px;">使用步骤</h3>
            <ol style="color:#5f6368; line-height:2;">
                <li>在左侧选择或搜索城市（可多选）</li>
                <li>设置总预算和旅行天数</li>
                <li>点击"开始规划"获取智能路线</li>
                <li>查看各城市的详细攻略</li>
            </ol>
        </div>
        ''', unsafe_allow_html=True)
        
        # 数据展示
        st.markdown("---")
        cols = st.columns(4)
        with cols[0]:
            st.metric("覆盖城市", "300+")
        with cols[1]:
            st.metric("景点数量", "5000+")
        with cols[2]:
            st.metric("美食数据", "美团/大众点评")
        with cols[3]:
            st.metric("更新频率", "每周")

if __name__ == "__main__":
    main()
