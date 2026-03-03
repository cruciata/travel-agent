#!/bin/bash
# GitHub部署脚本
# 使用方法: ./deploy.sh YOUR_GITHUB_TOKEN

set -e

TOKEN=$1
REPO_NAME="travel-agent"

if [ -z "$TOKEN" ]; then
    echo "❌ 错误: 请提供GitHub Personal Access Token"
    echo ""
    echo "获取Token步骤:"
    echo "1. 访问 https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 生成并复制token"
    echo ""
    echo "然后运行: ./deploy.sh ghp_xxxxxxxxxxxx"
    exit 1
fi

echo "🚀 开始部署到GitHub..."

# 创建GitHub仓库
echo "📦 创建远程仓库..."
curl -s -H "Authorization: token $TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     -X POST \
     -d '{
       "name": "'"$REPO_NAME"'",
       "description": "基于ReAct架构的智能旅行规划Agent",
       "private": false,
       "auto_init": false
     }' \
     https://api.github.com/user/repos

echo ""
echo "🔗 配置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://$TOKEN@github.com/$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user | grep -o '"login":"[^"]*"' | cut -d'"' -f4)/$REPO_NAME.git"

echo "📤 推送代码..."
git push -u origin main

echo ""
echo "✅ 部署成功！"
echo ""
echo "🌐 仓库地址: https://github.com/$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user | grep -o '"login":"[^"]*"' | cut -d'"' -f4)/$REPO_NAME"
