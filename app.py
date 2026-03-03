"""
范の旅行小助手 - SVG图标版
使用简单SVG图标，确保正常显示
"""
import streamlit as st
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city
from tools.travel_costs import optimize_route_by_budget
from tools.food_search import search_cities_by_food, get_food_recommendations
from tools.backgrounds import get_multi_city_background
from tools.attraction_details import get_attraction_detail, get_city_transport

# 读取本地SVG图标
def get_svg_icon(icon_name):
    """读取本地SVG图标文件"""
    try:
        import os
        icon_path = os.path.join('static', 'icons', f'{icon_name}.svg')
        with open(icon_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
            # 提取svg标签内容，添加内联样式
            svg_content = svg_content.replace('fill="#5f6368"', 'fill="currentColor"')
            svg_content = svg_content.replace('height="24px"', 'height="18px"')
            svg_content = svg_content.replace('width="24px"', 'width="18px"')
            svg_content = svg_content.replace('<svg', '<svg style="vertical-align:middle;margin-right:4px;"')
            return svg_content
    except Exception as e:
        print(f"Error loading icon {icon_name}: {e}")
        return ''

# 图标映射
ICONS = {
    'pin': get_svg_icon('location_on'),
    'clock': get_svg_icon('schedule'),
    'ticket': get_svg_icon('confirmation_number'),
    'star': get_svg_icon('star'),
    'lightbulb': get_svg_icon('lightbulb'),
    'bus': get_svg_icon('directions_bus'),
    'walking': get_svg_icon('directions_walk'),
    'plane': get_svg_icon('flight'),
    'train': get_svg_icon('train'),
    'search': get_svg_icon('search'),
    'utensils': get_svg_icon('restaurant'),
    'wallet': get_svg_icon('account_balance_wallet'),
    'arrow': get_svg_icon('arrow_forward'),
    'check': get_svg_icon('check'),
    'trash': get_svg_icon('delete'),
    'info': get_svg_icon('info'),
}

def icon(name):
    return ICONS.get(name, '')

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
if 'selected_attractions' not in st.session_state:
    st.session_state.selected_attractions = {}

# 极简风格CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    * { font-family: 'Inter', -apple-system, sans-serif !important; }
    
    .stApp { background: #fafafa; }
    
    .main .block-container {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 32px;
        max-width: 1000px;
    }
    
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e8e8e8;
    }
    
    button[kind="header"] { display: none !important; }
    
    /* 修复 Streamlit Material Icon 显示问题 */
    [data-testid="stIconMaterial"] { 
        font-family: 'Material Icons', 'Segoe UI Symbol', sans-serif !important;
        font-size: 20px !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    
    /* 隐藏损坏的图标文本 */
    [data-testid="stIconMaterial"]:not(:has(svg)) {
        color: transparent !important;
        width: 20px !important;
    }
    
    h1 { font-size: 24px !important; font-weight: 600 !important; color: #1a1a1a; }
    h2 { font-size: 18px !important; font-weight: 600 !important; color: #1a1a1a; }
    h3 { font-size: 14px !important; font-weight: 600 !important; color: #666; }
    
    .stButton > button {
        background: #1a1a1a !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover { background: #000 !important; }
    
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #666 !important;
        border: 1px solid #ddd !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #1a1a1a !important;
        color: white !important;
        border-color: #1a1a1a !important;
    }
    
    .stTextInput > div > div > input {
        border: 1px solid #e0e0e0 !important;
        border-radius: 6px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1a1a1a !important;
    }
    
    .step-box {
        background: #f8f8f8;
        border-left: 3px solid #1a1a1a;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 6px 6px 0;
        font-size: 14px;
    }
    
    .attraction-detail-card {
        background: #fafafa;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .attraction-detail-header {
        font-weight: 600;
        font-size: 15px;
        color: #1a1a1a;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .attraction-detail-row {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin: 8px 0;
        font-size: 13px;
        color: #555;
    }
    
    .attraction-detail-icon {
        color: #999;
        width: 20px;
        text-align: center;
    }
    
    .transport-card {
        background: #f5f5f5;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
    }
    
    .transport-icon {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

def init_agent(budget, points, days, food_enabled):
    agent = ReActAgent(budget, points, days, food_enabled)
    agent.register_tool("get_weather", get_weather)
    agent.register_tool("get_crowd", get_crowd)
    agent.register_tool("plan_route", plan_route)
    agent.register_tool("calculate_time", calculate_time)
    agent.register_tool("recommend_food", recommend_food)
    return agent

def display_attraction_details(attraction_name):
    detail = get_attraction_detail(attraction_name)
    
    st.markdown(f"""
    <div class="attraction-detail-card">
        <div class="attraction-detail-header">{icon('pin')} {attraction_name}</div>
        <div class="attraction-detail-row">
            <span class="attraction-detail-icon">{icon('clock')}</span>
            <span>建议游玩时间：<strong>{detail['duration']}</strong></span>
        </div>
        <div class="attraction-detail-row">
            <span class="attraction-detail-icon">{icon('ticket')}</span>
            <span>门票价格：<strong>{detail['ticket']}</strong></span>
        </div>
        <div class="attraction-detail-row">
            <span class="attraction-detail-icon">{icon('star')}</span>
            <span>最佳时段：{detail['best_time']}</span>
        </div>
        <div class="attraction-detail-row">
            <span class="attraction-detail-icon">{icon('lightbulb')}</span>
            <span>游玩建议：{detail['tips']}</span>
        </div>
        <div class="attraction-detail-row">
            <span class="attraction-detail-icon">{icon('bus')}</span>
            <span>交通：{', '.join([f"{k}: {v}" for k, v in detail['transport'].items()])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_inter_attraction_transport(from_attr, to_attr):
    st.markdown(f"""
    <div class="transport-card">
        <span class="transport-icon">{icon('walking')}</span>
        <span><strong>{from_attr} → {to_attr}</strong> | 建议步行或打车，约10-20分钟</span>
    </div>
    """, unsafe_allow_html=True)

def display_react_steps(history):
    for step in history:
        status = step["status"]
        content = step["content"]
        if "思考" in status.value:
            st.markdown(f'<div class="step-box"><strong>{icon("lightbulb")} 思考</strong><br>{content}</div>', unsafe_allow_html=True)
        elif "行动" in status.value:
            st.markdown(f'<div class="step-box"><strong>{icon("arrow")} 行动</strong><br>{content}</div>', unsafe_allow_html=True)
        elif "结果" in status.value:
            st.markdown(f'<div class="step-box"><strong>{icon("check")} 结果</strong><br>{content}</div>', unsafe_allow_html=True)

def toggle_city(city):
    if city in st.session_state.selected_cities:
        st.session_state.selected_cities.remove(city)
        if city in st.session_state.selected_attractions:
            del st.session_state.selected_attractions[city]
    else:
        st.session_state.selected_cities.append(city)
        attractions = get_attractions(city)
        if attractions:
            st.session_state.selected_attractions[city] = attractions[:3]

def toggle_attraction(city, attraction):
    if city not in st.session_state.selected_attractions:
        st.session_state.selected_attractions[city] = []
    
    if attraction in st.session_state.selected_attractions[city]:
        st.session_state.selected_attractions[city].remove(attraction)
    else:
        st.session_state.selected_attractions[city].append(attraction)

def display_city_attractions_selector(city):
    attractions = get_attractions(city)
    if not attractions:
        return
    
    selected = st.session_state.selected_attractions.get(city, [])
    
    st.markdown(f"**{icon('pin')} {city}的景点**", unsafe_allow_html=True)
    
    attr_search = st.text_input("🔍 搜索景点", placeholder="输入景点名...", key=f"attr_search_{city}")
    
    display_attractions = attractions
    if attr_search:
        display_attractions = [a for a in attractions if attr_search.lower() in a.lower()]
    
    cols = st.columns(3)
    for i, attr in enumerate(display_attractions[:9]):
        with cols[i % 3]:
            is_selected = attr in selected
            btn_label = f"✓ {attr}" if is_selected else attr
            btn_type = "primary" if is_selected else "secondary"
            if st.button(btn_label, key=f"attr_{city}_{attr}", type=btn_type, use_container_width=True):
                toggle_attraction(city, attr)
                st.rerun()
    
    if selected:
        st.caption(f"已选择 {len(selected)} 个景点")

def main():
    st.title("范の旅行小助手")
    st.caption("多城市智能规划 · 机票酒店优化 · 美食反向搜索")
    
    with st.sidebar:
        st.markdown(f"## {icon('pin')} 旅行配置", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📍 城市", "🍜 美食", "💰 预算"])
        
        with tab1:
            st.markdown("### 选择城市")
            
            search_keyword = st.text_input("🔍 搜索城市", placeholder="输入城市名...")
            
            if search_keyword:
                matched = search_cities(search_keyword)
                if matched:
                    for city in matched[:5]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(city)
                        with col2:
                            if city in st.session_state.selected_cities:
                                st.markdown(f"{icon('check')} 已选", unsafe_allow_html=True)
                            else:
                                if st.button(f"➕ 添加", key=f"search_add_{city}"):
                                    toggle_city(city)
                                    st.rerun()
            
            st.markdown("**热门城市**")
            cols = st.columns(3)
            for i, city in enumerate(POPULAR_CITIES[:12]):
                with cols[i % 3]:
                    is_selected = city in st.session_state.selected_cities
                    btn_label = f"✓ {city}" if is_selected else city
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(btn_label, key=f"pop_{city}", type=btn_type, use_container_width=True):
                        toggle_city(city)
                        st.rerun()
            
            if st.session_state.selected_cities:
                st.markdown("---")
                st.markdown("### 已选城市及景点")
                
                for city in st.session_state.selected_cities:
                    with st.expander(f"📍 {city}", expanded=True):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{city}**")
                        with col2:
                            if st.button("🗑️ 删除", key=f"remove_{city}"):
                                toggle_city(city)
                                st.rerun()
                        
                        display_city_attractions_selector(city)
        
        with tab2:
            st.markdown("### 根据美食找城市")
            
            food_search = st.text_input("🍜 输入美食名称", placeholder="如：火锅、烤鸭、小笼包...")
            
            if food_search:
                results = search_cities_by_food(food_search)
                if results:
                    st.success(f"找到 {len(results)} 个相关城市")
                    for result in results[:5]:
                        city = result["city"]
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{city}** - {result['food']}")
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button(f"➕ 添加", key=f"food_add_{city}"):
                                    toggle_city(city)
                                    st.rerun()
                            else:
                                st.markdown(f"{icon('check')}", unsafe_allow_html=True)
                else:
                    st.warning("未找到相关城市")
            
            st.markdown("---")
            st.markdown("**热门美食推荐**")
            recommendations = get_food_recommendations()
            for rec in recommendations[:5]:
                with st.expander(f"🍜 {rec['food']}"):
                    st.write(f"推荐城市: {', '.join(rec['cities'][:3])}")
        
        with tab3:
            budget = st.number_input("💰 总预算 (元)", min_value=1000, max_value=100000, value=5000, step=1000)
            days = st.slider("⏱️ 总天数", min_value=1, max_value=15, value=5)
            food_enabled = st.toggle("🍜 开启美食推荐", value=True)
        
        st.markdown("---")
        start_planning = st.button("▶️ 开始规划", type="primary", use_container_width=True)
    
    days_per_city = {}
    if st.session_state.selected_cities:
        remaining_days = days if 'days' in locals() else 5
        for i, city in enumerate(st.session_state.selected_cities):
            if i == len(st.session_state.selected_cities) - 1:
                days_per_city[city] = max(1, remaining_days)
            else:
                city_days = max(1, remaining_days // (len(st.session_state.selected_cities) - i))
                days_per_city[city] = city_days
                remaining_days -= city_days
    
    if start_planning:
        if not st.session_state.selected_cities:
            st.error("请至少选择一个城市！")
            return
        
        for city in st.session_state.selected_cities:
            if city not in st.session_state.selected_attractions or not st.session_state.selected_attractions[city]:
                attractions = get_attractions(city)
                if attractions:
                    st.session_state.selected_attractions[city] = attractions[:3]
                    st.info(f"已自动为{city}推荐 {len(attractions[:3])} 个热门景点")
        
        st.markdown("### 旅行概览")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("城市数", len(st.session_state.selected_cities))
        with col2:
            total_attractions = sum(len(attrs) for attrs in st.session_state.selected_attractions.values())
            st.metric("景点数", total_attractions)
        with col3:
            st.metric("天数", f"{days}天")
        
        if len(st.session_state.selected_cities) > 1:
            st.markdown("---")
            st.markdown("### 多城市路线规划")
            
            plan_result = optimize_route_by_budget(st.session_state.selected_cities, budget, days_per_city)
            
            route = plan_result["route"]
            route_html = '<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:20px 0;">'
            for i, city in enumerate(route):
                route_html += f'<div style="background:#1a1a1a;color:white;padding:12px 20px;border-radius:6px;font-weight:500;">{i+1}. {city}</div>'
                if i < len(route) - 1:
                    transport = get_city_transport(city, route[i+1])
                    transport_text = list(transport.values())[0] if transport else "建议高铁"
                    route_html += f'<div style="color:#666;font-size:11px;text-align:center;"><span style="font-size:16px;">→</span><br/>{transport_text[:8]}..</div>'
            route_html += '</div>'
            st.markdown(route_html, unsafe_allow_html=True)
            
            if plan_result.get("flights"):
                st.markdown("#### 航班信息")
                for flight in plan_result["flights"]:
                    st.markdown(f"""
                    <div style="background:#ffffff;border:1px solid #e8e8e8;border-radius:6px;padding:12px;margin:8px 0;">
                        <strong>{flight['from']} → {flight['to']}</strong>
                        <span style="float:right;color:#1a1a1a;font-weight:500;">¥{flight['economy']}</span>
                        <br><small style="color:#666;">{icon('clock')} {flight['duration']}小时 | {flight['distance']}km</small>
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
                if diff >= 0:
                    st.metric("剩余", f"¥{diff}", delta="在预算内")
                else:
                    st.metric("超支", f"¥{abs(diff)}", delta="超出预算", delta_color="inverse")
        
        st.markdown("---")
        
        for city in st.session_state.selected_cities:
            selected = st.session_state.selected_attractions.get(city, [])
            if not selected:
                continue
            
            city_days = days_per_city.get(city, 1)
            
            with st.expander(f"{city} ({len(selected)}个景点)", expanded=True):
                with st.spinner(f"规划{city}路线中..."):
                    agent = init_agent(
                        budget // len(st.session_state.selected_cities),
                        selected,
                        city_days,
                        food_enabled
                    )
                    result = agent.run()
                
                optimized_route = result['route']
                
                left_col, right_col = st.columns([2, 1])
                
                with left_col:
                    st.markdown(f"**{icon('pin')} 优化路线**: {' → '.join(optimized_route)}", unsafe_allow_html=True)
                    
                    st.markdown("#### 景点详细攻略")
                    for i, attr in enumerate(optimized_route):
                        is_last = (i == len(optimized_route) - 1)
                        display_attraction_details(attr)
                        
                        if not is_last:
                            next_attr = optimized_route[i + 1]
                            display_inter_attraction_transport(attr, next_attr)
                    
                    if result.get('weather', {}).get('forecast'):
                        st.markdown(f"#### 天气预报")
                        weather_cols = st.columns(len(result['weather']['forecast']))
                        for i, day in enumerate(result['weather']['forecast']):
                            with weather_cols[i]:
                                st.metric(f"第{day['day']}天", f"{day['temp_high']}°C", f"{day['condition']}")
                    
                    if food_enabled:
                        st.markdown(f"#### 美食推荐")
                        food_data = get_food_for_city(city)
                        if food_data.get("must_eat"):
                            for r in food_data["must_eat"][:3]:
                                tags = " ".join([f"`{t}`" for t in r.get("tags", [])])
                                st.markdown(f"• **{r['name']}** ⭐{r['rating']} ¥{r['price']}/人 · {tags}")
                
                with right_col:
                    st.markdown("#### 执行过程")
                    display_react_steps(agent.history)
    
    else:
        st.markdown("---")
        st.subheader("欢迎使用范の旅行小助手")
        
        st.markdown("**核心功能**")
        st.markdown(f"- {icon('pin')} **多城市规划** — 一次旅行规划多个城市，自动优化路线", unsafe_allow_html=True)
        st.markdown(f"- {icon('plane')} **机票酒店优化** — 根据实时价格规划最经济的方案", unsafe_allow_html=True)
        st.markdown(f"- {icon('utensils')} **美食反向搜索** — 输入美食名称，找到最地道的城市", unsafe_allow_html=True)
        st.markdown(f"- {icon('star')} **景点详细攻略** — 游玩时间、门票、交通一站式信息", unsafe_allow_html=True)
        
        st.markdown("**使用步骤**")
        st.markdown(f"1. {icon('pin')} 在左侧选择城市（可多选）", unsafe_allow_html=True)
        st.markdown(f"2. {icon('star')} 为每个城市选择想去的景点（支持搜索）", unsafe_allow_html=True)
        st.markdown(f"3. {icon('wallet')} 设置总预算和旅行天数", unsafe_allow_html=True)
        st.markdown(f'4. {icon("arrow")} 点击"开始规划"一键生成完整攻略', unsafe_allow_html=True)
        
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
