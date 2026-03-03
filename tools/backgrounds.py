"""
城市背景图片管理
使用Unsplash免费图片API
"""

# 城市背景图片URL映射（使用Unsplash）
CITY_BACKGROUNDS = {
    # 默认背景
    "default": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1920&q=80",
    
    # 直辖市
    "北京": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1920&q=80",  # 故宫
    "上海": "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=1920&q=80",  # 外滩
    "天津": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "重庆": "https://images.unsplash.com/photo-1530305408560-82a1374812af?w=1920&q=80",  # 夜景
    
    # 热门旅游城市
    "杭州": "https://images.unsplash.com/photo-1568315390530-135970a33d03?w=1920&q=80",  # 西湖
    "成都": "https://images.unsplash.com/photo-1565521990426-613d7b8767b4?w=1920&q=80",
    "西安": "https://images.unsplash.com/photo-1597735090079-302207a55456?w=1920&q=80",  # 古城墙
    "武汉": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=1920&q=80",  # 黄鹤楼
    "南京": "https://images.unsplash.com/photo-1596973979251-2557956d3842?w=1920&q=80",
    "苏州": "https://images.unsplash.com/photo-1548013146-72479768bada?w=1920&q=80",  # 园林
    "厦门": "https://images.unsplash.com/photo-1598890777032-bde83547c3c7?w=1920&q=80",  # 鼓浪屿
    "青岛": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920&q=80",  # 海景
    "三亚": "https://images.unsplash.com/photo-1540202404-a8f0b2c4b1c7?w=1920&q=80",  # 海滩
    "丽江": "https://images.unsplash.com/photo-1527684651001-731c474bbb5a?w=1920&q=80",  # 古城
    "大理": "https://images.unsplash.com/photo-1626263468007-a9e0cf83f1ac?w=1920&q=80",  # 洱海
    "桂林": "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=1920&q=80",  # 山水
    "张家界": "https://images.unsplash.com/photo-1598255287296-65466800b417?w=1920&q=80",
    "黄山": "https://images.unsplash.com/photo-1588392382834-a891154bca4d?w=1920&q=80",
    "拉萨": "https://images.unsplash.com/photo-1599708153386-62e2e2368c28?w=1920&q=80",  # 布达拉宫
    "九寨沟": "https://images.unsplash.com/photo-1565608087341-345c6d58b221?w=1920&q=80",
    "西双版纳": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?w=1920&q=80",
    
    # 其他省会
    "广州": "https://images.unsplash.com/photo-1583394293214-28ez1e0e1538?w=1920&q=80",
    "深圳": "https://images.unsplash.com/photo-1598135753163-6167c1a1ad65?w=1920&q=80",
    "长沙": "https://images.unsplash.com/photo-1590736969955-71cc94901144?w=1920&q=80",
    "郑州": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "沈阳": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "大连": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=1920&q=80",
    "哈尔滨": "https://images.unsplash.com/photo-1548765015-1e047ff434e5?w=1920&q=80",  # 冰雪
    "长春": "https://images.unsplash.com/photo-1548765015-1e047ff434e5?w=1920&q=80",
    "石家庄": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "太原": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "济南": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "合肥": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "南昌": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "福州": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "贵阳": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "昆明": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "南宁": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "海口": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "兰州": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "西宁": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "银川": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "乌鲁木齐": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "呼和浩特": "https://images.unsplash.com/photo-1590523277543-a94d2e4eb00b?w=1920&q=80",
    "拉萨": "https://images.unsplash.com/photo-1599708153386-62e2e2368c28?w=1920&q=80",
    
    # 港澳
    "香港": "https://images.unsplash.com/photo-1536599018102-9f803c140fc1?w=1920&q=80",  # 维港
    "澳门": "https://images.unsplash.com/photo-1559666126-84f389727b9a?w=1920&q=80",
    "台北": "https://images.unsplash.com/photo-1470004914212-05527e49370b?w=1920&q=80",
}

# 风景类别背景
CATEGORY_BACKGROUNDS = {
    "山水": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "古镇": "https://images.unsplash.com/photo-1527684651001-731c474bbb5a?w=1920&q=80",
    "海景": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "城市": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80",
    "雪景": "https://images.unsplash.com/photo-1548765015-1e047ff434e5?w=1920&q=80",
    "草原": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1920&q=80",
    "沙漠": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1920&q=80",
}

def get_city_background(city: str) -> str:
    """获取城市背景图片URL"""
    if city in CITY_BACKGROUNDS:
        return CITY_BACKGROUNDS[city]
    return CITY_BACKGROUNDS["default"]

def get_multi_city_background(cities: list) -> str:
    """获取多城市背景（使用第一个主要城市）"""
    if not cities:
        return CITY_BACKGROUNDS["default"]
    
    # 优先使用有专属背景的城市
    for city in cities:
        if city in CITY_BACKGROUNDS and city != "default":
            return CITY_BACKGROUNDS[city]
    
    return CITY_BACKGROUNDS["default"]

def generate_background_css(image_url: str) -> str:
    """生成背景图片CSS样式"""
    return f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.3)), url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* 主要内容区域半透明背景 */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }}
    
    /* 侧边栏样式 */
    .css-1d391kg {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
    }}
    
    /* 标题样式 */
    h1, h2, h3 {{
        color: #1E88E5 !important;
    }}
    
    /* 卡片样式 */
    .stAlert {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
    }}
    
    /* 按钮样式 */
    .stButton>button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    /* 选择框样式 */
    .stSelectbox {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 文本输入框样式 */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px;
    }}
    
    /* 复选框样式 */
    .stMultiSelect {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 滑块样式 */
    .stSlider {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
    }}
    
    /* 数字输入框样式 */
    .stNumberInput {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 开关样式 */
    .stToggle {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 下拉菜单样式 */
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
    }}
    
    /* 标签样式 */
    .stTabs {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px;
        padding: 0.5rem;
    }}
    
    /* 代码块样式 */
    .stCode {{
        background-color: rgba(30, 30, 30, 0.95) !important;
    }}
    
    /* 数据框样式 */
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.95) !important;
    }}
    
    /* 图表样式 */
    .stPlotlyChart {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
        padding: 1rem;
    }}
    
    /* 提示信息样式 */
    .stInfo {{
        background-color: rgba(232, 244, 253, 0.95) !important;
    }}
    
    .stSuccess {{
        background-color: rgba(212, 237, 218, 0.95) !important;
    }}
    
    .stWarning {{
        background-color: rgba(255, 243, 205, 0.95) !important;
    }}
    
    .stError {{
        background-color: rgba(248, 215, 218, 0.95) !important;
    }}
    
    /* 进度条样式 */
    .stProgress > div > div {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 分隔线样式 */
    hr {{
        border-color: rgba(255, 255, 255, 0.3) !important;
    }}
    
    /* 链接样式 */
    a {{
        color: #667eea !important;
    }}
    
    a:hover {{
        color: #764ba2 !important;
    }}
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: rgba(102, 126, 234, 0.5);
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(102, 126, 234, 0.8);
    }}
    
    /* 图片加载动画 */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    .stApp {{
        animation: fadeIn 1s ease-in;
    }}
    
    /* 卡片悬停效果 */
    .element-container:hover {{
        transform: translateY(-2px);
        transition: transform 0.3s ease;
    }}
    
    /* 响应式调整 */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem;
            margin: 0.5rem;
        }}
    }}
    
    /* 加载动画 */
    .stSpinner {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 50%;
        padding: 1rem;
    }}
    
    /* 文件上传区域样式 */
    .stFileUploader {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px;
        padding: 1rem;
    }}
    
    /* 颜色选择器样式 */
    .stColorPicker {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 日期选择器样式 */
    .stDateInput {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 时间选择器样式 */
    .stTimeInput {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* JSON显示样式 */
    .stJson {{
        background-color: rgba(30, 30, 30, 0.95) !important;
        border-radius: 10px;
        padding: 1rem;
    }}
    
    /* 空白状态样式 */
    .stEmpty {{
        background-color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* 异常显示样式 */
    .stException {{
        background-color: rgba(248, 215, 218, 0.95) !important;
    }}
    
    /* 帮助文本样式 */
    .stHelp {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    /* 标注文本样式 */
    .stCaption {{
        color: rgba(255, 255, 255, 0.8) !important;
    }}
    
    /*  Latex 公式样式 */
    .stLatex {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
        padding: 1rem;
    }}
    
    /* 度量卡片样式增强 */
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: bold;
        color: #667eea !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: #666 !important;
    }}
    
    /* 表格样式增强 */
    .stTable {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
        overflow: hidden;
    }}
    
    /* 折叠面板样式增强 */
    .streamlit-expanderHeader {{
        background-color: rgba(102, 126, 234, 0.1) !important;
        border-radius: 10px;
        font-weight: bold;
    }}
    
    .streamlit-expanderContent {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 0 0 10px 10px;
    }}
    
    /* 单选按钮样式 */
    .stRadio > label {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
    }}
    
    /* 多选框样式 */
    .stCheckbox > label {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }}
    
    /* 选中的选项样式 */
    .st-bq {{
        background-color: rgba(102, 126, 234, 0.2) !important;
        border-left: 4px solid #667eea !important;
    }}
    
    /* 标记文本样式 */
    mark {{
        background-color: rgba(102, 126, 234, 0.3) !important;
        color: #333 !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }}
    
    /* 引用块样式 */
    blockquote {{
        background-color: rgba(102, 126, 234, 0.1) !important;
        border-left: 4px solid #667eea !important;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
    }}
    
    /* 脚注样式 */
    .footnote {{
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9rem;
    }}
    </style>
    """
