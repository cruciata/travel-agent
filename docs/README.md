# GitHub Pages 部署配置

为了让GitHub Pages能显示项目介绍页面，我创建了静态页面。

## 部署步骤

1. 进入GitHub仓库设置
   - 访问: https://github.com/cruciata/travel-agent/settings

2. 启用GitHub Pages
   - 左侧菜单选择 "Pages"
   - Source 选择 "Deploy from a branch"
   - Branch 选择 "main"，文件夹选择 "/docs"
   - 点击 "Save"

3. 等待部署完成
   - 大约1-2分钟后，访问: https://cruciata.github.io/travel-agent

## 注意

GitHub Pages只能托管静态页面，无法运行Python代码。
要体验完整功能，请使用 Streamlit Cloud 部署。
