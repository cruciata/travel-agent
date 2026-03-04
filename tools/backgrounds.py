"""
城市背景图片管理
使用Unsplash免费图片API
为每个城市生成随机风景背景图
"""
import hashlib

# Unsplash 随机风景图基础URL
UNSPLASH_BASE = "https://images.unsplash.com/photo"

# 精选的高质量风景图ID列表（确保每个城市都有好看的背景）
LANDSCAPE_PHOTOS = [
    "1506905925346-21bda4d32df4",  # 山脉风景
    "1464822759023-fed622ff2c3b",  # 山峰
    "1470071459604-3b5ec3a7fe05",  # 雾山
    "1447752875204-b2f9798c641c",  # 森林
    "1441974231531-c6227db76b6e",  # 林间阳光
    "1501785888041-af3ef285b470",  # 湖山
    "1439066615861-d1af74d74000",  # 湖泊
    "1472214103451-9374bd1c798e",  # 日落山景
    "1500534314209-a4804b35c55a",  # 山谷
    "1458668383970-8b19e0ffb350",  # 森林小径
    "1490730141103-6c37a6c6d0e6",  # 海边日落
    "1507525428034-b723cf961d3e",  # 海滩
    "1437719417032-8595fd9e9dc6",  # 田园风光
    "1494500764479-0c8f2919a3d8",  # 田野
    "1465146344425-f00d5f5c8f07",  # 自然风光
    "1470071459604-3b5ec3a7fe05",  # 云海
    "1506905925346-21bda4d32df4",  # 高山
    "1441974231531-c6227db76b6e",  # 森林
    "1472214103451-9374bd1c798e",  # 黄昏
    "1501785888041-af3ef285b470",  # 湖光山色
]

# 特定城市可以用特定的风景类型
CITY_LANDSCAPE_MAPPING = {
    # 海边城市
    "三亚": "beach", "青岛": "beach", "厦门": "beach", "大连": "beach",
    "海口": "beach", "威海": "beach", "烟台": "beach", "珠海": "beach",
    "北海": "beach", "舟山": "beach", "连云港": "beach",
    # 山城
    "重庆": "mountain", "贵阳": "mountain", "桂林": "mountain",
    "张家界": "mountain", "黄山": "mountain", "泰山": "mountain",
    "庐山": "mountain", "峨眉山": "mountain", "武夷山": "mountain",
    # 古城
    "西安": "ancient", "南京": "ancient", "苏州": "ancient",
    "杭州": "ancient", "丽江": "ancient", "大理": "ancient",
    "平遥": "ancient", "凤凰": "ancient", "乌镇": "ancient",
    # 冰雪
    "哈尔滨": "snow", "长春": "snow", "沈阳": "snow",
    "雪乡": "snow", "阿尔山": "snow", "长白山": "snow",
    # 沙漠
    "敦煌": "desert", "吐鲁番": "desert", "中卫": "desert",
    # 草原
    "呼伦贝尔": "grassland", "锡林郭勒": "grassland", "伊犁": "grassland",
    "若尔盖": "grassland", "坝上": "grassland",
    # 高原
    "拉萨": "plateau", "林芝": "plateau", "日喀则": "plateau",
    "西宁": "plateau", "香格里拉": "plateau",
}


def get_city_background(city: str) -> str:
    """
    获取城市背景图片URL
    基于城市名生成固定的随机风景图
    """
    # 使用城市名作为种子，确保同一城市总是返回相同图片
    hash_val = int(hashlib.md5(city.encode('utf-8')).hexdigest(), 16)
    
    # 基于哈希值选择图片ID
    photo_index = hash_val % len(LANDSCAPE_PHOTOS)
    photo_id = LANDSCAPE_PHOTOS[photo_index]
    
    # 使用数字签名确保不同城市有不同的图
    random_param = hash_val % 1000
    
    # 构建Unsplash URL (使用数字ID避免中文编码问题)
    return f"{UNSPLASH_BASE}-{photo_id}?w=1920&q=80&sig={random_param}"


def get_multi_city_background(cities: list) -> str:
    """获取多城市背景（使用第一个城市）"""
    if not cities:
        return get_city_background("default")
    
    # 优先使用第一个城市
    return get_city_background(cities[0])


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

# 风景类别背景（备用）
CATEGORY_BACKGROUNDS = {
    "山水": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80",
    "古镇": "https://images.unsplash.com/photo-1527684651001-731c474bbb5a?w=1920&q=80",
    "海景": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80",
    "城市": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80",
    "雪景": "https://images.unsplash.com/photo-1548765015-1e047ff434e5?w=1920&q=80",
    "草原": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1920&q=80",
    "沙漠": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1920&q=80",
}

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
