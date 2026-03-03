#!/bin/bash
# 推送代码到GitHub

echo "正在推送到GitHub..."
cd /root/.openclaw/workspace/travel-agent

# 配置远程仓库
git remote remove origin 2>/dev/null
git remote add origin https://github.com/cruciata/travel-agent.git

# 推送代码
git push -u origin main

echo ""
echo "如果提示输入用户名和密码："
echo "- 用户名: cruciata"
echo "- 密码: 使用GitHub Personal Access Token（不是登录密码）"
echo ""
echo "如果没有Token，请访问: https://github.com/settings/tokens 创建"
