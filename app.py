"""
范の旅行小助手 - Streamlit Web界面
支持多城市旅行规划、动态背景、美食反向搜索
"""
import streamlit as st
import json
from main import ReActAgent
from tools import get_weather, get_crowd, plan_route, calculate_time, recommend_food
from tools.cities import get_all_cities, get_attractions, search_cities, POPULAR_CITIES
from tools.food_data import get_food_for_city
from tools.travel_costs import plan_multi_city_route, optimize_route_by_budget, get_flight_price, get_hotel_price
from tools.food_search import search_cities_by_food, get_food_recommendations, get_city_signature_foods
from tools.backgrounds import get_city_background, get_multi_city_background, generate_background_css

# 页面配置
st.set_page_config(
    page_title="范の旅行小助手",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化session state
if 'selected_cities' not in st.session_state:
    st.session_state.selected_cities = []
if 'current_background' not in st.session_state:
    st.session_state.current_background = "default"
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "城市"

def apply_background():
    """应用背景图片"""
    if st.session_state.plan_generated and st.session_state.selected_cities:
        bg_url = get_multi_city_background(st.session_state.selected_cities)
    else:
        bg_url = get_city_background("default")
    
    st.markdown(generate_background_css(bg_url), unsafe_allow_html=True)

# 应用背景
apply_background()

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
    """展示ReAct执行步骤"""
    st.markdown("### 🔄 ReAct执行过程")
    for step in history:
        status = step["status"]
        content = step["content"]
        with st.container():
            if "思考" in status.value:
                st.info(f"🧠 **思考**: {content}")
            elif "行动" in status.value:
                st.warning(f"🔧 **行动**: {content}")
            elif "结果" in status.value:
                st.success(f"📊 **结果**: {content}")

def display_multi_city_plan(plan_result, budget):
    """展示多城市路线规划结果"""
    st.markdown("### 🗺️ 多城市路线规划")
    
    # 路线展示
    route = plan_result["route"]
    route_cols = st.columns(len(route))
    for i, city in enumerate(route):
        with route_cols[i]:
            st.markdown(f"""
            <div style="text-align:center; background:linear-gradient(135deg, #667eea, #764ba2); 
                        color:white; padding:15px; border-radius:10px;">
                <h3>{i+1}</h3>
                <h4>{city}</h4>
            </div>
            """, unsafe_allow_html=True)
            if i < len(route) - 1:
                st.markdown("<div style='text-align:center; font-size:24px;'>→</div>", unsafe_allow_html=True)
    
    # 航班信息
    st.markdown("#### ✈️ 航班信息")
    for flight in plan_result.get("flights", []):
        with st.container():
            st.markdown(f"""
            <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin:10px 0;">
                <strong>{flight['from']} → {flight['to']}</strong> 
                <span style="float:right;">
                    💰 经济舱¥{flight['economy']} / 商务舱¥{flight['business']}
                </span>
                <br><small>
                    距离: {flight['distance']}km | 
                    飞行时间: {flight['duration']}小时 | 
                    {'直飞' if flight['direct'] else '需转机'}
                </small>
            </div>
            """, unsafe_allow_html=True)
    
    # 酒店信息
    st.markdown("#### 🏨 酒店预估")
    hotel_cols = st.columns(len(plan_result.get("hotel_costs", {})))
    for i, (city, cost) in enumerate(plan_result.get("hotel_costs", {}).items()):
        with hotel_cols[i % 4]:
            st.metric(city, f"¥{cost}")
    
    # 费用汇总
    st.markdown("#### 💰 费用汇总")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("机票总价", f"¥{plan_result.get('total_flight_cost', 0)}")
    with col2:
        st.metric("酒店总价", f"¥{plan_result.get('total_hotel_cost', 0)}")
    with col3:
        st.metric("总费用", f"¥{plan_result.get('total_cost', 0)}")
    with col4:
        diff = plan_result.get('budget_diff', 0)
        if diff >= 0:
            st.metric("预算剩余", f"¥{diff}", delta="✅ 在预算内")
        else:
            st.metric("超预算", f"¥{abs(diff)}", delta="⚠️ 超出", delta_color="inverse")

def display_city_food(city):
    """展示城市美食推荐"""
    food_data = get_food_for_city(city)
    st.markdown(f"### 🍜 {city}美食推荐")
    
    # 必吃榜
    if food_data.get("must_eat"):
        st.markdown("**🏆 必吃榜**")
        for restaurant in food_data["must_eat"][:3]:
            tags = " ".join([f"`{tag}`" for tag in restaurant.get("tags", [])])
            rank = restaurant.get("rank", "")
            st.markdown(f"""
            <div style="background:white; padding:12px; border-radius:8px; margin:8px 0; 
                        border-left:4px solid #ff6b6b; box-shadow:0 2px 4px rgba(0,0,0,0.1);">
                {'<span style="background:#ff6b6b; color:white; padding:2px 8px; border-radius:4px; font-size:12px;">' + rank + '</span>' if rank else ''}
                <strong>{restaurant['name']}</strong> 
                <span style="color:#ff9500;">{'⭐' * int(restaurant['rating'])}</span> {restaurant['rating']}
                <span style="color:#666; float:right;">💰 {restaurant['price']}元/人</span>
                <br><small>{restaurant['type']} | {tags}</small>
            </div>
            """, unsafe_allow_html=True)

def main():
    """主函数"""
    # 标题
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <h1 style="font-size:3rem; color:white; text-shadow:2px 2px 4px rgba(0,0,0,0.5);">
            🌸 范の旅行小助手
        </h1>
        <p style="font-size:1.2rem; color:rgba(255,255,255,0.9);">
            多城市智能规划 · 机票酒店优化 · 美食反向搜索
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏 - 使用标签页组织
    with st.sidebar:
        st.markdown("## ⚙️ 旅行配置")
        
        tab1, tab2, tab3 = st.tabs(["🌍 城市", "🍜 美食", "💰 预算"])
        
        with tab1:
            st.markdown("### 选择城市（可多选）")
            
            # 城市搜索
            search_keyword = st.text_input(
                "🔍 搜索城市",
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
                                if st.button("➕ 添加", key=f"add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                            else:
                                st.success("✓")
            
            # 热门城市快速添加
            st.markdown("**热门城市**")
            popular_cols = st.columns(3)
            for i, city in enumerate(POPULAR_CITIES[:12]):
                with popular_cols[i % 3]:
                    is_selected = city in st.session_state.selected_cities
                    btn_label = f"✓ {city}" if is_selected else city
                    btn_type = "primary" if is_selected else "secondary"
                    
                    if st.button(btn_label, key=f"pop_{city}", type=btn_type, use_container_width=True):
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
                        st.info(city)
                    with col2:
                        if st.button("❌", key=f"remove_{city}"):
                            st.session_state.selected_cities.remove(city)
                            st.rerun()
        
        with tab2:
            st.markdown("### 🍜 根据美食找城市")
            
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
                        match_type = result["match_type"]
                        confidence = result["confidence"]
                        city = result["city"]
                        food = result["food"]
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{city}** - {food}")
                            st.caption(f"匹配度: {'⭐' * int(confidence * 5)}")
                        with col2:
                            if city not in st.session_state.selected_cities:
                                if st.button("➕", key=f"food_add_{city}"):
                                    st.session_state.selected_cities.append(city)
                                    st.rerun()
                else:
                    st.warning("未找到相关城市，试试其他美食名称")
            
            st.markdown("---")
            st.markdown("**热门美食推荐**")
            recommendations = get_food_recommendations()
            for rec in recommendations[:5]:
                with st.expander(f"🍽️ {rec['food']}"):
                    st.write(f"城市: {', '.join(rec['cities'][:3])}")
        
        with tab3:
            # 预算设置
            budget = st.number_input(
                "💰 总预算 (元)",
                min_value=1000,
                max_value=100000,
                value=5000,
                step=1000
            )
            
            # 天数设置
            days = st.slider(
                "📅 总天数",
                min_value=1,
                max_value=15,
                value=5
            )
            
            # 美食推荐开关
            food_enabled = st.toggle(
                "🍜 开启美食推荐",
                value=True
            )
            
            st.markdown("---")
            st.markdown(f"**当前配置**")
            st.write(f"城市: {len(st.session_state.selected_cities)}个")
            st.write(f"预算: ¥{budget}")
            st.write(f"天数: {days}天")
        
        # 开始规划按钮
        st.markdown("---")
        start_planning = st.button("🚀 开始规划", type="primary", use_container_width=True)
    
    # 主界面内容
    if start_planning:
        if not st.session_state.selected_cities:
            st.error("⚠️ 请至少选择一个城市！")
            return
        
        # 标记已生成规划
        st.session_state.plan_generated = True
        
        # 重新应用背景
        apply_background()
        
        # 显示输入摘要
        st.markdown("### 📝 您的旅行需求")
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
        
        # 多城市路线规划
        if len(st.session_state.selected_cities) > 1:
            st.markdown("---")
            days_per_city = {city: max(1, days // len(st.session_state.selected_cities)) 
                           for city in st.session_state.selected_cities}
            plan_result = optimize_route_by_budget(st.session_state.selected_cities, budget, days_per_city)
            display_multi_city_plan(plan_result, budget)
        
        # 每个城市的详细规划
        st.markdown("---")
        st.markdown("### 📍 各城市详细攻略")
        
        for city in st.session_state.selected_cities:
            with st.expander(f"🏙️ {city}攻略", expanded=True):
                attractions = get_attractions(city)
                
                if attractions:
                    # 选择该城市景点
                    selected_attractions = st.multiselect(
                        f"{city}的景点（推荐选择{min(3, len(attractions))}个）",
                        attractions,
                        default=attractions[:min(3, len(attractions))],
                        key=f"attr_{city}"
                    )
                    
                    if selected_attractions and st.button(f"生成{city}详细攻略", key=f"btn_{city}"):
                        city_days = max(1, days // len(st.session_state.selected_cities))
                        
                        progress_bar = st.progress(0)
                        
                        # 初始化Agent
                        progress_bar.progress(20)
                        agent = init_agent(budget // len(st.session_state.selected_cities), 
                                         selected_attractions, city_days, food_enabled)
                        
                        # 运行规划
                        progress_bar.progress(50)
                        result = agent.run()
                        
                        progress_bar.progress(100)
                        
                        # 显示结果
                        display_react_steps(agent.history)
                        
                        # 路线展示
                        st.markdown(f"**优化路线**: {' → '.join(result['route'])}")
                        
                        # 天气预报
                        if result.get('weather', {}).get('forecast'):
                            weather_cols = st.columns(len(result['weather']['forecast']))
                            for i, day in enumerate(result['weather']['forecast']):
                                with weather_cols[i]:
                                    st.metric(f"第{day['day']}天", 
                                            f"{day['temp_high']}°C", 
                                            f"{day['condition']}")
                        
                        # 美食推荐
                        if food_enabled:
                            display_city_food(city)
                else:
                    st.info(f"暂无{city}的景点数据，可以手动添加")
                    custom = st.text_input(f"添加{city}的自定义景点", key=f"custom_{city}")
                    if custom:
                        st.success(f"已添加: {custom}")
    
    else:
        # 欢迎页面
        st.markdown("""
        <div style="background:rgba(255,255,255,0.95); padding:30px; border-radius:15px;">
            <h2>👋 欢迎使用范の旅行小助手</h2>
            
            <h3>🌟 核心功能</h3>
            <ul>
                <li><strong>多城市规划</strong> - 一次旅行可规划多个城市，自动优化路线</li>
                <li><strong>机票酒店</strong> - 根据实时价格规划最经济的旅行方案</li>
                <li><strong>美食反向搜索</strong> - 输入想吃的美食，找到最地道的城市</li>
                <li><strong>动态背景</strong> - 根据选择的城市自动切换风景背景</li>
                <li><strong>300+城市</strong> - 覆盖全国所有热门旅游城市</li>
            </ul>
            
            <h3>🚀 使用步骤</h3>
            <ol>
                <li>在左侧侧边栏选择或搜索城市（可多选）</li>
                <li>设置总预算和旅行天数</li>
                <li>点击"开始规划"获取智能路线</li>
                <li>查看各城市的详细攻略</li>
            </ol>
            
            <h3>🍜 美食功能</h3>
            <p>想吃火锅？输入"火锅"找到成都、重庆！<br>
            想吃烤鸭？输入"烤鸭"找到北京！<br>
            支持根据美食反向搜索城市！</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 数据覆盖展示
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("覆盖城市", "300+")
        with col2:
            st.metric("景点数量", "5000+")
        with col3:
            st.metric("美食数据", "美团/大众点评")
        with col4:
            st.metric("更新频率", "每周自动")

if __name__ == "__main__":
    main()
