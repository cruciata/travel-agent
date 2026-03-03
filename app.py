"""
范の旅行小助手 - Google风格简约3D界面
修复版：背景图+自动显示景点+纯文字提示
"""
import streamlit as st
import json
import html
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_all_cities, get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city
from tools.travel_costs import plan_multi_city_route, optimize_route_by_budget
from tools.food_search import search_cities_by_food, get_food_recommendations
from tools.backgrounds import get_city_background, get_multi_city_background

# 页面配置
st.set_page_config(
    page_title="范の旅行小助手",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'selected_cities' not in st.session_state:
    st.session_state.selected_cities = []
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False
if 'current_bg' not in st.session_state:
    st.session_state.current_bg = "default"

def get_background_css(bg_url):
    """生成背景图片CSS"""
    if bg_url and bg_url != "default":
        return f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.92)), url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        .main .block-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-top: 20px;
            margin-bottom: 20px;
            padding: 32px;
        }}
        </style>
        """
    return """
    <style>
    .stApp {
        background: #f8f9fa !important;
    }
    .main .block-container {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 20px;
        padding: 32px;
    }
    </style>
    """

# 应用背景
if st.session_state.selected_cities:
    bg_url = get_multi_city_background(st.session_state.selected_cities)
    st.session_state.current_bg = bg_url
else:
    bg_url = "default"

st.markdown(get_background_css(bg_url), unsafe_allow_html=True)

# Google Material Design CSS
st.markdown("""
<style>
    * { font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e8eaed;
    }
    
    /* 标题 */
    h1 { color: #202124 !important; font-weight: 400 !important; font-size: 2.2rem !important; }
    h2 { color: #202124 !important; font-weight: 400 !important; font-size: 1.6rem !important; }
    h3 { color: #5f6368 !important; font-weight: 500 !important; font-size: 1.1rem !important; }
    
    /* 按钮 */
    .stButton > button {
        background: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        box-shadow: 0 1px 2px rgba(60,64,67,0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #1557b0 !important;
        box-shadow: 0 4px 8px rgba(60,64,67,0.3) !important;
        transform: translateY(-1px);
    }
    
    /* 次要按钮 */
    .secondary-btn > button {
        background: #ffffff !important;
        color: #1a73e8 !important;
        border: 1px solid #dadce0 !important;
    }
    
    /* 城市卡片 */
    .city-card {
        background: #ffffff;
        border: 1px solid #e8eaed;
        border-radius: 8px;
        padding: 8px 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
        margin: 2px;
    }
    .city-card:hover {
        border-color: #1a73e8;
        box-shadow: 0 2px 8px rgba(26,115,232,0.15);
    }
    .city-card.selected {
        background: #e8f0fe;
        border-color: #1a73e8;
        color: #1a73e8;
        font-weight: 500;
    }
    
    /* 景点卡片 */
    .attraction-card {
        background: #ffffff;
        border: 1px solid #e8eaed;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .attraction-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    
    /* 步骤指示器 */
    .step-thinking {
        background: #e8f0fe;
        border-left: 3px solid #4285f4;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .step-acting {
        background: #fef3e8;
        border-left: 3px solid #fbbc04;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .step-observing {
        background: #e6f4ea;
        border-left: 3px solid #34a853;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
    }
    
    /* 标签 */
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 500;
        margin: 2px;
    }
    .tag-blue { background: #e8f0fe; color: #1967d2; }
    .tag-green { background: #e6f4ea; color: #188038; }
    .tag-yellow { background: #fef3e8; color: #b06000; }
    .tag-red { background: #fce8e6; color: #d93025; }
    
    /* 折叠面板 */
    .streamlit-expanderHeader {
        background: #f8f9fa !important;
        border: 1px solid #e8eaed !important;
        border-radius: 8px !important;
    }
    
    /* 输入框 */
    .stTextInput > div > div > input {
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 2px rgba(26,115,232,0.2) !important;
    }
    
    /* 滚动条 */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f1f3f4; }
    ::-webkit-scrollbar-thumb { background: #dadce0; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #bdc1c6; }
    
    /* 隐藏默认展开按钮图标 */
    button[kind="header"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

def init_agent(budget, points, days, food_enabled):
    """初始化Agent"""
    agent = ReActAgent(budget, points, days, food_enabled)
    agent.register_tool("get_weather", get_weather)
    agent.register_tool("get_crowd", get_crowd)
    agent.register_tool("plan_route", plan_route)
    agent.register_tool("calculate_time", calculate_time)
    agent.register_tool("recommend_food", recommend_food)
    return agent

def display_react_steps(history):
    """展示ReAct执行步骤"""
    st.markdown("### 执行过程")
    for step in history:
        status = step["status"]
        content = step["content"]
        if "思考" in status.value:
            st.markdown(f'<div class="step-thinking">💭 思考：{content}</div>', unsafe_allow_html=True)
        elif "行动" in status.value:
            st.markdown(f'<div class="step-acting">⚡ 行动：{content}</div>', unsafe_allow_html=True)
        elif "结果" in status.value:
            st.markdown(f'<div class="step-observing">✓ 结果：{content}</div>', unsafe_allow_html=True)

def display_city_attractions(city):
    """显示城市的热门景点"""
    attractions = get_attractions(city)
    if attractions:
        st.markdown(f"**{city}热门景点**")
        # 显示前6个景点
        cols = st.columns(2)
        for i, attr in enumerate(attractions[:6]):
            with cols[i % 2]:
                st.markdown(f'<div class="attraction-card">📍 {attr}</div>', unsafe_allow_html=True)

def display_multi_city_plan(plan_result, budget):
    """展示多城市路线规划"""
    st.markdown("### 多城市路线规划")
    
    route = plan_result["route"]
    route_html = '<div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin:16px 0;">'
    for i, city in enumerate(route):
        route_html += f'<div style="background:#1a73e8; color:white; padding:12px 20px; border-radius:8px; font-weight:500;">{i+1}. {city}</div>'
        if i < len(route) - 1:
            route_html += '<div style="color:#5f6368; font-size:20px;">→</div>'
    route_html += '</div>'
    st.markdown(route_html, unsafe_allow_html=True)
    
    # 航班信息
    if plan_result.get("flights"):
        st.markdown("#### 航班信息")
        for flight in plan_result["flights"]:
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e8eaed; border-radius:8px; padding:12px; margin:8px 0;">
                <strong>{flight['from']} → {flight['to']}</strong>
                <span style="float:right; color:#1a73e8; font-weight:500;">¥{flight['economy']}</span>
                <br><small style="color:#5f6368;">{flight['distance']}km · {flight['duration']}小时</small>
            </div>
            """, unsafe_allow_html=True)
    
    # 费用汇总
    cols = st.columns(4)
    with cols[0]:
        st.metric("机票", f"¥{plan_result.get('total_flight_cost', 0)}")
    with cols[1]:
        st.metric("酒店", f"¥{plan_result.get('total_hotel_cost', 0)}")
    with cols[2]:
        st.metric("总费用", f"¥{plan_result.get('total_cost', 0)}")
    with cols[3]:
        diff = plan_result.get('budget_diff', 0)
        if diff >= 0:
            st.metric("剩余", f"¥{diff}", delta="在预算内")
        else:
            st.metric("超支", f"¥{abs(diff)}", delta="超出预算", delta_color="inverse")

def display_city_food(city):
    """展示城市美食"""
    food_data = get_food_for_city(city)
    st.markdown(f"### {city}美食推荐")
    
    if food_data.get("must_eat"):
        st.markdown("**必吃榜**")
        for r in food_data["must_eat"][:3]:
            tags = " ".join([f'<span class="tag tag-blue">{t}</span>' for t in r.get("tags", [])])
            st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e8eaed; border-radius:8px; padding:12px; margin:8px 0;">
                <strong>{r['name']}</strong>
                <span style="float:right; color:#fbbc04;">{'★' * int(r['rating'])} {r['rating']}</span>
                <br><small>{r['type']} · {tags}</small>
                <span style="float:right; color:#5f6368;">¥{r['price']}/人</span>
            </div>
            """, unsafe_allow_html=True)

def main():
    """主函数"""
    # 头部 - 使用纯文字而不是HTML
    st.title("范の旅行小助手")
    st.caption("多城市智能规划 · 机票酒店优化 · 美食反向搜索")
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## 旅行配置")
        
        tab1, tab2, tab3 = st.tabs(["城市", "美食", "预算"])
        
        with tab1:
            st.markdown("### 选择城市")
            
            # 城市搜索
            search_keyword = st.text_input("搜索城市", placeholder="输入城市名...")
            
            if search_keyword:
                matched = search_cities(search_keyword)
                if matched:
                    for city in matched[:5]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(city)
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button(f"添加##{city}", key=f"add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                            else:
                                st.markdown("✓ 已选")
            
            # 热门城市
            st.markdown("**热门城市**")
            city_cols = st.columns(3)
            for i, city in enumerate(POPULAR_CITIES[:12]):
                with city_cols[i % 3]:
                    is_selected = city in st.session_state.selected_cities
                    btn_label = f"✓ {city}" if is_selected else city
                    if st.button(btn_label, key=f"pop_{city}", use_container_width=True):
                        if is_selected:
                            st.session_state.selected_cities.remove(city)
                        else:
                            st.session_state.selected_cities.append(city)
                        st.rerun()
            
            # 已选城市
            if st.session_state.selected_cities:
                st.markdown("**已选城市**")
                for city in st.session_state.selected_cities:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"✓ {city}")
                    with col2:
                        if st.button("删除", key=f"remove_{city}"):
                            st.session_state.selected_cities.remove(city)
                            st.rerun()
                
                # 显示各城市的景点
                st.markdown("---")
                st.markdown("### 各城市热门景点")
                for city in st.session_state.selected_cities:
                    with st.expander(f"{city}的景点", expanded=True):
                        display_city_attractions(city)
        
        with tab2:
            st.markdown("### 根据美食找城市")
            
            food_search = st.text_input("输入美食名称", placeholder="如：火锅、烤鸭、小笼包...")
            
            if food_search:
                results = search_cities_by_food(food_search)
                if results:
                    st.success(f"找到 {len(results)} 个相关城市")
                    for result in results[:5]:
                        city = result["city"]
                        food = result["food"]
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{city}** - {food}")
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button(f"添加#{city}", key=f"food_add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                else:
                    st.warning("未找到相关城市")
            
            st.markdown("---")
            st.markdown("**热门美食推荐**")
            recommendations = get_food_recommendations()
            for rec in recommendations[:5]:
                with st.expander(rec['food']):
                    st.write(f"推荐城市: {', '.join(rec['cities'][:3])}")
        
        with tab3:
            budget = st.number_input("总预算 (元)", min_value=1000, max_value=100000, value=5000, step=1000)
            days = st.slider("总天数", min_value=1, max_value=15, value=5)
            food_enabled = st.toggle("开启美食推荐", value=True)
        
        st.markdown("---")
        start_planning = st.button("开始规划", type="primary", use_container_width=True)
    
    # 主内容区
    if start_planning:
        if not st.session_state.selected_cities:
            st.error("请至少选择一个城市！")
            return
        
        st.session_state.plan_generated = True
        
        # 输入摘要
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("城市数", len(st.session_state.selected_cities))
        with col2:
            st.metric("预算", f"¥{budget}")
        with col3:
            st.metric("天数", f"{days}天")
        with col4:
            avg = days // len(st.session_state.selected_cities) if st.session_state.selected_cities else 0
            st.metric("每城平均", f"{avg}天")
        
        # 多城市路线规划
        if len(st.session_state.selected_cities) > 1:
            st.markdown("---")
            days_per_city = {city: max(1, days // len(st.session_state.selected_cities)) 
                           for city in st.session_state.selected_cities}
            plan_result = optimize_route_by_budget(st.session_state.selected_cities, budget, days_per_city)
            display_multi_city_plan(plan_result, budget)
        
        # 各城市详细规划
        st.markdown("---")
        st.markdown("### 各城市详细攻略")
        
        for city in st.session_state.selected_cities:
            with st.expander(f"{city}攻略"):
                attractions = get_attractions(city)
                
                if attractions:
                    selected = st.multiselect(f"选择{city}的景点", attractions, 
                                            default=attractions[:min(3, len(attractions))],
                                            key=f"attr_{city}")
                    
                    if selected and st.button(f"生成{city}攻略", key=f"btn_{city}"):
                        city_days = max(1, days // len(st.session_state.selected_cities))
                        
                        progress = st.progress(0)
                        agent = init_agent(budget // len(st.session_state.selected_cities), 
                                         selected, city_days, food_enabled)
                        
                        progress.progress(50)
                        result = agent.run()
                        progress.progress(100)
                        
                        display_react_steps(agent.history)
                        st.markdown(f"**路线**: {' → '.join(result['route'])}")
                        
                        if result.get('weather', {}).get('forecast'):
                            wcols = st.columns(len(result['weather']['forecast']))
                            for i, day in enumerate(result['weather']['forecast']):
                                with wcols[i]:
                                    st.metric(f"第{day['day']}天", f"{day['temp_high']}°C", day['condition'])
                        
                        if food_enabled:
                            display_city_food(city)
    
    else:
        # 欢迎页面 - 使用纯文本
        st.markdown("---")
        st.subheader("欢迎使用范の旅行小助手")
        
        st.markdown("**核心功能**")
        st.markdown("- **多城市规划** - 一次旅行规划多个城市，自动优化路线")
        st.markdown("- **机票酒店优化** - 根据实时价格规划最经济的方案")
        st.markdown("- **美食反向搜索** - 输入美食名称，找到最地道的城市")
        st.markdown("- **300+城市** - 覆盖全国热门旅游城市")
        
        st.markdown("**使用步骤**")
        st.markdown("1. 在左侧选择或搜索城市（可多选）")
        st.markdown("2. 设置总预算和旅行天数")
        st.markdown('3. 点击"开始规划"获取智能路线')
        st.markdown("4. 查看各城市的详细攻略")
        
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
