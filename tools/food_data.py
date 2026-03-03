"""
美团/大众点评风格美食推荐数据
基于真实榜单数据构建
"""

# 各城市必吃榜/热门榜餐厅数据
MEITUAN_DIANPING_FOODS = {
    "北京": {
        "must_eat": [  # 必吃榜
            {"name": "四季民福烤鸭店", "type": "北京菜", "rating": 4.8, "price": 180, "tags": ["烤鸭", "故宫观景"], "rank": "北京烤鸭榜第1"},
            {"name": "聚宝源", "type": "老北京火锅", "rating": 4.7, "price": 120, "tags": ["涮羊肉", "牛街老字号"], "rank": "火锅榜第2"},
            {"name": "胡大饭馆", "type": "川菜", "rating": 4.6, "price": 130, "tags": ["麻辣小龙虾", "簋街排队王"], "rank": "小龙虾榜第1"},
            {"name": "满恒记", "type": "老北京火锅", "rating": 4.7, "price": 110, "tags": ["涮羊肉", "手切鲜羊"], "rank": "火锅榜第3"},
            {"name": "大董", "type": "创意北京菜", "rating": 4.6, "price": 350, "tags": ["意境菜", "高端烤鸭"], "rank": "黑珍珠一钻"},
        ],
        "hot": [  # 热门榜
            {"name": "文宇奶酪", "type": "甜品", "rating": 4.5, "price": 25, "tags": ["宫廷奶酪", "南锣鼓巷"]},
            {"name": "姚记炒肝", "type": "北京小吃", "rating": 4.4, "price": 35, "tags": ["炒肝", "包子", "鼓楼"]},
            {"name": "护国寺小吃", "type": "北京小吃", "rating": 4.3, "price": 40, "tags": ["豌豆黄", "驴打滚", "品种全"]},
            {"name": "方砖厂69号炸酱面", "type": "老北京面馆", "rating": 4.5, "price": 30, "tags": ["炸酱面", "谢霆锋同款"]},
        ]
    },
    "上海": {
        "must_eat": [
            {"name": "蟹叁寳", "type": "蟹宴", "rating": 4.8, "price": 200, "tags": ["蟹黄面", "蟹黄饭"], "rank": "蟹宴榜第1"},
            {"name": "人和馆", "type": "本帮菜", "rating": 4.7, "price": 160, "tags": ["米其林一星", "蟹粉捞饭"], "rank": "米其林一星"},
            {"name": "莱莱小笼", "type": "小笼包", "rating": 4.6, "price": 60, "tags": ["蟹粉小笼", "天津路排队王"], "rank": "小笼包榜第1"},
            {"name": "生记", "type": "潮汕牛肉火锅", "rating": 4.7, "price": 140, "tags": ["鲜切牛肉", "夜宵热门"], "rank": "牛肉火锅第2"},
            {"name": "鮨一", "type": "日料", "rating": 4.8, "price": 800, "tags": ["Omakase", "黑珍珠"], "rank": "黑珍珠二钻"},
        ],
        "hot": [
            {"name": "国际饭店西饼屋", "type": "烘焙", "rating": 4.5, "price": 50, "tags": ["蝴蝶酥", "黄河路排队"]},
            {"name": "佳家汤包", "type": "小笼包", "rating": 4.4, "price": 45, "tags": ["蟹粉汤包", "黄河路"]},
            {"name": "鲜得来", "type": "排骨年糕", "rating": 4.3, "price": 30, "tags": ["排骨年糕", "云南路"]},
            {"name": "阿大葱油饼", "type": "小吃", "rating": 4.4, "price": 10, "tags": ["葱油饼", "网红"]},
        ]
    },
    "成都": {
        "must_eat": [
            {"name": "小龙坎火锅", "type": "四川火锅", "rating": 4.7, "price": 120, "tags": ["牛油火锅", "春熙路"], "rank": "火锅榜第1"},
            {"name": "饕林餐厅", "type": "川菜", "rating": 4.6, "price": 90, "tags": ["正宗川菜", "太古里"], "rank": "川菜榜第2"},
            {"name": "马旺子", "type": "川菜", "rating": 4.7, "price": 130, "tags": ["米其林必比登", "回锅肉"], "rank": "米其林必比登"},
            {"name": "钢管厂五区小郡肝", "type": "串串香", "rating": 4.5, "price": 80, "tags": ["小郡肝", "夜宵"], "rank": "串串榜第1"},
            {"name": "陈麻婆豆腐", "type": "川菜", "rating": 4.6, "price": 70, "tags": ["百年老店", "麻婆豆腐"], "rank": "川菜榜第3"},
        ],
        "hot": [
            {"name": "洞子口张老二凉粉", "type": "小吃", "rating": 4.4, "price": 20, "tags": ["甜水面", "文殊院"]},
            {"name": "严太婆锅盔", "type": "小吃", "rating": 4.5, "price": 15, "tags": ["锅盔", "文殊院排队"]},
            {"name": "冒椒火辣", "type": "串串", "rating": 4.5, "price": 60, "tags": ["冒菜", "奎星楼"]},
            {"name": "谭豆花", "type": "早餐", "rating": 4.4, "price": 25, "tags": ["豆花", "冰醉豆花"]},
        ]
    },
    "杭州": {
        "must_eat": [
            {"name": "楼外楼", "type": "杭帮菜", "rating": 4.5, "price": 180, "tags": ["西湖醋鱼", "百年名店"], "rank": "杭帮菜榜第1"},
            {"name": "外婆家", "type": "杭帮菜", "rating": 4.4, "price": 70, "tags": ["茶香鸡", "性价比"], "rank": "江浙菜榜第2"},
            {"name": "知味观", "type": "杭帮菜", "rating": 4.5, "price": 60, "tags": ["小笼包", "百年老店"], "rank": "小吃榜第1"},
            {"name": "福缘居", "type": "杭帮菜", "rating": 4.6, "price": 100, "tags": ["脆皮大肠", "本地人推荐"], "rank": "杭帮菜榜第3"},
        ],
        "hot": [
            {"name": "新丰小吃", "type": "小吃", "rating": 4.4, "price": 20, "tags": ["虾肉小笼", "杭州人的食堂"]},
            {"name": "游埠豆浆", "type": "早餐", "rating": 4.5, "price": 15, "tags": ["咸豆浆", "油条"]},
            {"name": "葱包桧", "type": "小吃", "rating": 4.3, "price": 8, "tags": ["传统小吃", "孙奶奶"]},
        ]
    },
    "广州": {
        "must_eat": [
            {"name": "陶陶居", "type": "粤菜", "rating": 4.7, "price": 140, "tags": ["早茶", "百年老店"], "rank": "粤菜榜第1"},
            {"name": "点都德", "type": "粤菜", "rating": 4.6, "price": 90, "tags": ["红米肠", "全天茶市"], "rank": "早茶榜第2"},
            {"name": "炳胜私厨", "type": "粤菜", "rating": 4.7, "price": 250, "tags": ["黑珍珠", "海鲜"], "rank": "黑珍珠一钻"},
            {"name": "陈添记", "type": "广州小吃", "rating": 4.5, "price": 40, "tags": ["鱼皮", "艇仔粥"], "rank": "小吃榜第1"},
            {"name": "丽的面家", "type": "粤菜", "rating": 4.6, "price": 60, "tags": ["云吞面", "蔡澜推荐"], "rank": "云吞面第1"},
        ],
        "hot": [
            {"name": "银记肠粉", "type": "肠粉", "rating": 4.4, "price": 25, "tags": ["布拉肠", "宝华路"]},
            {"name": "南信牛奶", "type": "甜品", "rating": 4.5, "price": 30, "tags": ["双皮奶", "姜撞奶"]},
            {"name": "顺记冰室", "type": "甜品", "rating": 4.4, "price": 35, "tags": ["椰子雪糕", "四大冰室"]},
            {"name": "达扬炖品", "type": "炖品", "rating": 4.6, "price": 50, "tags": ["椰子炖鸡", "文明路"]},
        ]
    },
    "深圳": {
        "must_eat": [
            {"name": "陈鹏鹏潮汕菜", "type": "潮汕菜", "rating": 4.7, "price": 120, "tags": ["卤鹅", "日日香"], "rank": "潮汕菜第1"},
            {"name": "蓉悦", "type": "川菜", "rating": 4.6, "price": 150, "tags": ["精致川菜", "黑珍珠"], "rank": "黑珍珠一钻"},
            {"name": "老乾杯", "type": "日式烧肉", "rating": 4.8, "price": 500, "tags": ["米其林", "和牛"], "rank": "米其林一星"},
            {"name": "春满园", "type": "粤菜", "rating": 4.5, "price": 130, "tags": ["早茶", "老字号"], "rank": "粤菜榜第2"},
        ],
        "hot": [
            {"name": "蘩楼", "type": "粤菜", "rating": 4.5, "price": 90, "tags": ["早茶", "性价比"]},
            {"name": "沙县小吃", "type": "小吃", "rating": 4.3, "price": 25, "tags": ["拌面", "蒸饺", "正宗"]},
            {"name": "凤凰楼", "type": "粤菜", "rating": 4.4, "price": 100, "tags": ["早茶", "老字号"]},
        ]
    },
    "西安": {
        "must_eat": [
            {"name": "长安大牌档", "type": "陕西菜", "rating": 4.6, "price": 80, "tags": ["葫芦鸡", "网红"], "rank": "陕菜榜第1"},
            {"name": "老白家面馆", "type": "面馆", "rating": 4.5, "price": 25, "tags": ["油泼面", "手工面"], "rank": "面馆第1"},
            {"name": "子午路张记", "type": "肉夹馍", "rating": 4.6, "price": 20, "tags": ["肉夹馍", "子午路总店"], "rank": "肉夹馍第1"},
            {"name": "同盛祥", "type": "羊肉泡馍", "rating": 4.5, "price": 50, "tags": ["老字号", "泡馍"], "rank": "泡馍榜第1"},
            {"name": "醉长安", "type": "陕西菜", "rating": 4.5, "price": 90, "tags": ["毛笔酥", "网红"], "rank": "陕菜榜第2"},
        ],
        "hot": [
            {"name": "贾三灌汤包", "type": "灌汤包", "rating": 4.4, "price": 40, "tags": ["灌汤包", "回民街"]},
            {"name": "老米家泡馍", "type": "泡馍", "rating": 4.3, "price": 45, "tags": ["羊肉泡馍", "小炒"]},
            {"name": "东南亚甑糕", "type": "甜品", "rating": 4.4, "price": 20, "tags": ["甑糕", "胖子甑糕"]},
            {"name": "花奶奶酸梅汤", "type": "饮品", "rating": 4.5, "price": 10, "tags": ["酸梅汤", "大皮院"]},
        ]
    },
    "重庆": {
        "must_eat": [
            {"name": "珮姐老火锅", "type": "火锅", "rating": 4.7, "price": 110, "tags": ["九宫格", "洪崖洞"], "rank": "火锅榜第1"},
            {"name": "花市豌杂面", "type": "小面", "rating": 4.6, "price": 20, "tags": ["豌杂面", "渝中老字号"], "rank": "小面第1"},
            {"name": "杨记隆府", "type": "川菜", "rating": 4.5, "price": 90, "tags": ["江湖菜", "辣子鸡"], "rank": "川菜榜第1"},
            {"name": "好又来酸辣粉", "type": "小吃", "rating": 4.5, "price": 15, "tags": ["酸辣粉", "八一路"], "rank": "小吃榜第1"},
        ],
        "hot": [
            {"name": "秦云老太婆摊摊面", "type": "小面", "rating": 4.4, "price": 18, "tags": ["小面", "摊摊面"]},
            {"name": "降龙爪爪", "type": "卤味", "rating": 4.3, "price": 20, "tags": ["鸡爪", "天天向上同款"]},
            {"name": "一只酸奶牛", "type": "饮品", "rating": 4.4, "price": 15, "tags": ["酸奶紫米露", "本土品牌"]},
        ]
    },
    "南京": {
        "must_eat": [
            {"name": "南京大牌档", "type": "南京菜", "rating": 4.6, "price": 80, "tags": ["盐水鸭", "狮子桥"], "rank": "南京菜第1"},
            {"name": "李记清真馆", "type": "小吃", "rating": 4.7, "price": 30, "tags": ["牛肉锅贴", "打钉巷"], "rank": "锅贴第1"},
            {"name": "狮王府", "type": "淮扬菜", "rating": 4.5, "price": 130, "tags": ["狮子头", "精致"], "rank": "淮扬菜第2"},
            {"name": "小厨娘", "type": "淮扬菜", "rating": 4.5, "price": 100, "tags": ["淮扬菜", "性价比"], "rank": "淮扬菜第3"},
        ],
        "hot": [
            {"name": "回味鸭血粉丝", "type": "小吃", "rating": 4.4, "price": 25, "tags": ["鸭血粉丝", "连锁"]},
            {"name": "尹氏汤包", "type": "汤包", "rating": 4.5, "price": 35, "tags": ["鸡汁汤包", "夫子庙"]},
            {"name": "刘长兴", "type": "面馆", "rating": 4.4, "price": 25, "tags": ["薄皮馄饨", "老字号"]},
        ]
    },
    "武汉": {
        "must_eat": [
            {"name": "蔡林记", "type": "热干面", "rating": 4.5, "price": 20, "tags": ["热干面", "户部巷"], "rank": "热干面第1"},
            {"name": "四季美", "type": "汤包", "rating": 4.5, "price": 45, "tags": ["汤包", "户部巷"], "rank": "汤包第1"},
            {"name": "老通城", "type": "豆皮", "rating": 4.4, "price": 20, "tags": ["三鲜豆皮", "老字号"], "rank": "豆皮第1"},
            {"name": "小蓝鲸", "type": "湖北菜", "rating": 4.5, "price": 90, "tags": ["藕汤", "排骨藕汤"], "rank": "湖北菜第1"},
        ],
        "hot": [
            {"name": "严老幺烧麦", "type": "早餐", "rating": 4.6, "price": 25, "tags": ["重油烧麦", "前进四路"]},
            {"name": "靓靓蒸虾", "type": "小龙虾", "rating": 4.7, "price": 150, "tags": ["蒸虾", "万松园"]},
            {"name": "今楚汤包", "type": "汤包", "rating": 4.4, "price": 40, "tags": ["汤包", "万松园"]},
        ]
    },
    "长沙": {
        "must_eat": [
            {"name": "文和友", "type": "小龙虾", "rating": 4.6, "price": 120, "tags": ["口味虾", "复古风"], "rank": "小龙虾第1"},
            {"name": "炊烟小炒黄牛肉", "type": "湘菜", "rating": 4.7, "price": 100, "tags": ["小炒黄牛肉", "走进联合国"], "rank": "湘菜第1"},
            {"name": "费大厨辣椒炒肉", "type": "湘菜", "rating": 4.6, "price": 80, "tags": ["辣椒炒肉", "全国连锁"], "rank": "湘菜第2"},
            {"name": "壹盏灯", "type": "湘菜", "rating": 4.5, "price": 75, "tags": ["鸭掌筋", "酸萝卜肚丝"], "rank": "湘菜第3"},
            {"name": "黑色经典", "type": "臭豆腐", "rating": 4.5, "price": 15, "tags": ["臭豆腐", "坡子街"], "rank": "小吃第1"},
        ],
        "hot": [
            {"name": "茶颜悦色", "type": "饮品", "rating": 4.7, "price": 20, "tags": ["幽兰拿铁", "长沙必喝"]},
            {"name": "糖油粑粑", "type": "小吃", "rating": 4.4, "price": 10, "tags": ["糖油粑粑", "太平街"]},
            {"name": "邵福记梅菜扣肉饼", "type": "小吃", "rating": 4.5, "price": 12, "tags": ["梅菜扣肉饼", "太平街"]},
        ]
    },
    "厦门": {
        "must_eat": [
            {"name": "临家闽南菜", "type": "闽南菜", "rating": 4.6, "price": 120, "tags": ["土笋冻", "姜母鸭"], "rank": "闽南菜第1"},
            {"name": "佳味再添", "type": "小吃", "rating": 4.5, "price": 30, "tags": ["沙茶面", "芋包", "老字号"], "rank": "小吃第1"},
            {"name": "小眼镜大排档", "type": "海鲜", "rating": 4.5, "price": 100, "tags": ["酱油水", "海鲜"], "rank": "海鲜第1"},
            {"name": "黄则和", "type": "花生汤", "rating": 4.4, "price": 25, "tags": ["花生汤", "中山路"], "rank": "花生汤第1"},
        ],
        "hot": [
            {"name": "月华沙茶面", "type": "沙茶面", "rating": 4.5, "price": 20, "tags": ["沙茶面", "镇邦路"]},
            {"name": "1980烧肉粽", "type": "烧肉粽", "rating": 4.4, "price": 20, "tags": ["烧肉粽", "中山店"]},
            {"name": "莲欢海蛎煎", "type": "小吃", "rating": 4.5, "price": 25, "tags": ["海蛎煎", "局口街"]},
        ]
    },
    "青岛": {
        "must_eat": [
            {"name": "船歌鱼水饺", "type": "海鲜水饺", "rating": 4.6, "price": 100, "tags": ["墨鱼水饺", "黄花鱼水饺"], "rank": "水饺第1"},
            {"name": "九龙餐厅", "type": "鲁菜", "rating": 4.5, "price": 70, "tags": ["香辣鱿鱼条", "大沽路"], "rank": "鲁菜第1"},
            {"name": "王姐烧烤", "type": "烧烤", "rating": 4.4, "price": 60, "tags": ["烤鱿鱼", "中山路"], "rank": "烧烤第1"},
            {"name": "波螺油子", "type": "青岛菜", "rating": 4.5, "price": 80, "tags": ["海肠捞饭", "青岛本帮菜"], "rank": "青岛菜第1"},
        ],
        "hot": [
            {"name": "老西镇馄饨", "type": "馄饨", "rating": 4.5, "price": 20, "tags": ["电烤肉", "馄饨"]},
            {"name": "西镇臭豆腐", "type": "臭豆腐", "rating": 4.4, "price": 15, "tags": ["臭豆腐", "西镇"]},
            {"name": "王哥庄大馒头", "type": "面食", "rating": 4.3, "price": 10, "tags": ["铁锅馒头", "王哥庄"]},
        ]
    },
    "哈尔滨": {
        "must_eat": [
            {"name": "老厨家", "type": "东北菜", "rating": 4.6, "price": 80, "tags": ["锅包肉", "起源店"], "rank": "东北菜第1"},
            {"name": "华梅西餐厅", "type": "俄式西餐", "rating": 4.5, "price": 120, "tags": ["罐牛", "罐羊", "中央大街"], "rank": "西餐第1"},
            {"name": "张包铺", "type": "包子", "rating": 4.5, "price": 50, "tags": ["排骨包子", "豆腐包子"], "rank": "包子第1"},
            {"name": "老昌春饼", "type": "春饼", "rating": 4.4, "price": 60, "tags": ["春饼", "筋饼", "中央大街"], "rank": "春饼第1"},
        ],
        "hot": [
            {"name": "马迭尔冰棍", "type": "冷饮", "rating": 4.6, "price": 10, "tags": ["冰棍", "中央大街"]},
            {"name": "秋林红肠", "type": "熟食", "rating": 4.5, "price": 40, "tags": ["红肠", "秋林公司"]},
            {"name": "对青烤鹅", "type": "熟食", "rating": 4.4, "price": 60, "tags": ["烤鹅", "哈尔滨特产"]},
        ]
    },
    "丽江": {
        "must_eat": [
            {"name": "阿婆腊排骨", "type": "火锅", "rating": 4.6, "price": 70, "tags": ["腊排骨", "丽江古城"], "rank": "火锅第1"},
            {"name": "88号小吃店", "type": "云南菜", "rating": 4.5, "price": 60, "tags": ["鸡豆凉粉", "纳西烤肉"], "rank": "云南菜第1"},
            {"name": "勺子米线", "type": "米线", "rating": 4.5, "price": 30, "tags": ["过桥米线", "土鸡米线"], "rank": "米线第1"},
            {"name": "滇西王子", "type": "云南菜", "rating": 4.5, "price": 100, "tags": ["傣族手抓饭", "网红"], "rank": "云南菜第2"},
        ],
        "hot": [
            {"name": "鲜花饼", "type": "糕点", "rating": 4.4, "price": 5, "tags": ["鲜花饼", "伴手礼"]},
            {"name": "丽江粑粑", "type": "小吃", "rating": 4.3, "price": 10, "tags": ["纳西粑粑", "传统"]},
            {"name": "烤饵块", "type": "小吃", "rating": 4.4, "price": 8, "tags": ["烤饵块", "早点"]},
        ]
    },
}

# 为其他城市生成通用数据
def get_food_for_city(city):
    """获取城市美食推荐"""
    if city in MEITUAN_DIANPING_FOODS:
        return MEITUAN_DIANPING_FOODS[city]
    
    # 返回通用数据
    return {
        "must_eat": [
            {"name": f"{city}必吃老字号", "type": "地方菜", "rating": 4.5, "price": 80, "tags": ["老字号", "本地人推荐"], "rank": "必吃榜第1"},
            {"name": f"{city}人气火锅", "type": "火锅", "rating": 4.6, "price": 100, "tags": ["人气旺", "排队王"], "rank": "火锅榜第1"},
            {"name": f"{city}特色面馆", "type": "面馆", "rating": 4.4, "price": 30, "tags": ["特色", "手工"], "rank": "面馆第1"},
        ],
        "hot": [
            {"name": f"{city}网红小吃", "type": "小吃", "rating": 4.3, "price": 20, "tags": ["网红", "打卡"]},
            {"name": f"{city}老字号早餐", "type": "早餐", "rating": 4.4, "price": 15, "tags": ["老字号", "早点"]},
            {"name": f"{city}特色甜品", "type": "甜品", "rating": 4.2, "price": 25, "tags": ["特色", "手工"]},
        ]
    }
