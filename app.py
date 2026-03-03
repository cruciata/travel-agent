"""
范の旅行小助手 - 极简风格修复版
修复：arr前缀、图标、选中样式、删除按钮、景点布局
"""
import streamlit as st
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city
from tools.travel_costs import optimize_route_by_budget
from tools.food_search import search_cities_by_food, get_food_recommendations
from tools.backgrounds import get_multi_city_background

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

# 极简风格CSS
def get_minimal_css():
    bg_url = get_multi_city_background(st.session_state.selected_cities) if st.session_state.selected_cities else ""
    bg_style = f"""
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.92), rgba(255,255,255,0.95)), url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    """ if bg_url else ".stApp { background: #fafafa; }"
    
    return f"""
    <style>
        {bg_style}
        
        * {{ font-family: 'Inter', -apple-system, sans-serif !important; }}
        
        /* 内容区域 */
        .main .block-container {{
            background: rgba(255,255,255,0.98);
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            padding: 32px;
            max-width: 1000px;
        }}
        
        /* 侧边栏 */
        [data-testid="stSidebar"] {{
            background: #ffffff !important;
            border-right: 1px solid #e0e0e0;
        }}
        
        /* 隐藏展开按钮 */
        button[kind="header"] {{ display: none !important; }}
        
        /* 标题 */
        h1 {{ font-size: 26px !important; font-weight: 600 !important; color: #212121; letter-spacing: -0.5px; }}
        h2 {{ font-size: 18px !important; font-weight: 600 !important; color: #212121; }}
        h3 {{ font-size: 14px !important; font-weight: 600 !important; color: #757575; text-transform: uppercase; letter-spacing: 0.5px; }}
        
        /* 按钮 - 极简 */
        .stButton > button {{
            background: #212121 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background: #000000 !important;
            transform: translateY(-1px);
        }}
        
        /* 线框按钮 */
        .btn-outline > button {{
            background: transparent !important;
            color: #757575 !important;
            border: 1px solid #e0e0e0 !important;
        }}
        .btn-outline > button:hover {{
            background: #212121 !important;
            color: white !important;
            border-color: #212121 !important;
        }}
        
        /* 城市卡片网格 */
        .city-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }}
        
        /* 城市卡片 - 选中黑底白字 */
        .city-card {{
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 10px 8px;
            text-align: center;
            cursor: pointer;
            font-size: 13px;
            color: #757575;
            transition: all 0.2s ease;
            min-width: 50px;
        }}
        .city-card:hover {{
            border-color: #212121;
            color: #212121;
        }}
        .city-card.selected {{
            background: #212121;
            color: #ffffff;
            border-color: #212121;
        }}
        
        /* 景点网格 - 固定2列 */
        .attractions-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }}
        
        /* 景点卡片 - 统一带图标 */
        .attraction-card {{
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 12px;
            font-size: 13px;
            color: #212121;
            display: flex;
            align-items: center;
            gap: 8px;
            min-height: 44px;
        }}
        
        /* 折叠面板 */
        .streamlit-expanderHeader {{
            background: #fafafa !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 6px !important;
        }}
        
        /* 输入框 */
        .stTextInput > div > div > input {{
            border: 1px solid #e0e0e0 !important;
            border-radius: 6px !important;
        }}
        .stTextInput > div > div > input:focus {{
            border-color: #212121 !important;
        }}
        
        /* 滑块 */
        .stSlider > div > div > div {{
            color: #212121 !important;
        }}
        
        /* 标签页 */
        .stTabs [data-baseweb="tab-list"] {{
            background: #fafafa;
            border-radius: 6px;
            padding: 4px;
        }}
        .stTabs [aria-selected="true"] {{
            background: #ffffff !important;
            color: #212121 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        /* 已选城市项 */
        .selected-city-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 12px;
            background: #fafafa;
            border-radius: 6px;
            margin-bottom: 8px;
        }}
    </style>
    """

st.markdown(get_minimal_css(), unsafe_allow_html=True)

def init_agent(budget, points, days, food_enabled):
    agent = ReActAgent(budget, points, days, food_enabled)
    agent.register_tool("get_weather", get_weather)
    agent.register_tool("get_crowd", get_crowd)
    agent.register_tool("plan_route", plan_route)
    agent.register_tool("calculate_time", calculate_time)
    agent.register_tool("recommend_food", recommend_food)
    return agent

def display_react_steps(history):
    st.markdown("### 执行过程")
    for step in history:
        status = step["status"]
        content = step["content"]
        if "思考" in status.value:
            st.markdown(f'<div style="background:#f5f5f5;border-left:3px solid #212121;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;">💭 思考：{content}</div>', unsafe_allow_html=True)
        elif "行动" in status.value:
            st.markdown(f'<div style="background:#fafafa;border-left:3px solid #757575;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;">⚡ 行动：{content}</div>', unsafe_allow_html=True)
        elif "结果" in status.value:
            st.markdown(f'<div style="background:#f0f0f0;border-left:3px solid #212121;padding:10px 14px;margin:6px 0;border-radius:0 6px 6px 0;">✓ 结果：{content}</div>', unsafe_allow_html=True)

def display_city_attractions(city):
    attractions = get_attractions(city)
    if attractions:
        st.markdown(f"**{city}热门景点**")
        cols = st.columns(2)
        for i, attr in enumerate(attractions[:6]):
            with cols[i % 2]:
                st.markdown(f'<div class="attraction-card">📍 {attr}</div>', unsafe_allow_html=True)

def display_multi_city_plan(plan_result, budget):
    st.markdown("### 多城市路线规划")
    route = plan_result["route"]
    
    route_html = '<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:16px 0;">'
    for i, city in enumerate(route):
        route_html += f'<div style="background:#212121;color:white;padding:10px 18px;border-radius:6px;font-weight:500;font-size:14px;">{i+1}. {city}</div>'
        if i < len(route) - 1:
            route_html += '<span style="color:#757575;">→</span>'
    route_html += '</div>'
    st.markdown(route_html, unsafe_allow_html=True)
    
    if plan_result.get("flights"):
        st.markdown("#### 航班信息")
        for flight in plan_result["flights"]:
            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e0e0e0;border-radius:6px;padding:12px;margin:8px 0;">
                <strong>{flight['from']} → {flight['to']}</strong>
                <span style="float:right;color:#212121;font-weight:500;">¥{flight['economy']}</span>
                <br><small style="color:#757575;">{flight['distance']}km · {flight['duration']}小时</small>
            </div>
            """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("机票", f"¥{plan_result.get('total_flight_cost', 0)}")
    with cols[1]:
        st.metric("酒店", f"¥{plan_result.get('total_hotel_cost', 0)}")
    with cols[2]:
        st.metric("总费用", f"¥{plan_result.get('total_cost', 0)}")
    with cols[3]:
        diff = plan_result.get('budget_diff', 0)
        st.metric("剩余" if diff >= 0 else "超支", f"¥{abs(diff)}", 
                 delta="在预算内" if diff >= 0 else "超出预算",
                 delta_color="normal" if diff >= 0 else "inverse")

def main():
    st.title("范の旅行小助手")
    st.caption("多城市智能规划 · 机票酒店优化 · 美食反向搜索")
    
    with st.sidebar:
        st.markdown("## 旅行配置")
        
        tab1, tab2, tab3 = st.tabs(["城市", "美食", "预算"])
        
        with tab1:
            st.markdown("### 选择城市")
            
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
            
            st.markdown("**热门城市**")
            cols = st.columns(3)
            for i, city in enumerate(POPULAR_CITIES[:12]):
                with cols[i % 3]:
                    is_selected = city in st.session_state.selected_cities
                    btn_label = f"✓ {city}" if is_selected else city
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(btn_label, key=f"pop_{city}", type=btn_type, use_container_width=True):
                        if is_selected:
                            st.session_state.selected_cities.remove(city)
                        else:
                            st.session_state.selected_cities.append(city)
                        st.rerun()
            
            if st.session_state.selected_cities:
                st.markdown("**已选城市**")
                for city in st.session_state.selected_cities:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"✓ {city}")
                    with col2:
                        st.markdown('<span class="btn-outline">', unsafe_allow_html=True)
                        if st.button("删除", key=f"remove_{city}"):
                            st.session_state.selected_cities.remove(city)
                            st.rerun()
                        st.markdown('</span>', unsafe_allow_html=True)
                
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
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{city}**")
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button(f"添加#{city}", key=f"food_add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                else:
                    st.warning("未找到相关城市")
            
            st.markdown("**热门美食**")
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
    
    if start_planning:
        if not st.session_state.selected_cities:
            st.error("请至少选择一个城市！")
            return
        
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
        
        if len(st.session_state.selected_cities) > 1:
            st.markdown("---")
            days_per_city = {city: max(1, days // len(st.session_state.selected_cities)) 
                           for city in st.session_state.selected_cities}
            plan_result = optimize_route_by_budget(st.session_state.selected_cities, budget, days_per_city)
            display_multi_city_plan(plan_result, budget)
        
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
                            st.markdown(f"### {city}美食推荐")
                            food_data = get_food_for_city(city)
                            if food_data.get("must_eat"):
                                for r in food_data["must_eat"][:3]:
                                    st.markdown(f"**{r['name']}** ⭐{r['rating']} ¥{r['price']}/人")
    
    else:
        st.markdown("---")
        st.subheader("欢迎使用范の旅行小助手")
        st.markdown("**核心功能**")
        st.markdown("- **多城市规划** — 一次旅行规划多个城市，自动优化路线")
        st.markdown("- **机票酒店优化** — 根据实时价格规划最经济的方案")
        st.markdown("- **美食反向搜索** — 输入美食名称，找到最地道的城市")
        st.markdown("- **300+城市** — 覆盖全国热门旅游城市")
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
