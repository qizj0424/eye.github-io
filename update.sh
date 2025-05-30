#!/bin/bash
# 智能旅游规划助手 - 一键自动更新脚本
# 功能：自动检测destination目录变化并更新index.html
# 适用系统：Linux/Mac

echo "================================================"
echo "智能旅游规划助手 - 自动更新系统"
echo "================================================"
echo

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3！请先安装Python 3.7+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip" 
    echo "Mac: brew install python3"
    exit 1
fi

echo "检测到Python3已安装"
echo

# 检查并安装依赖包
echo "正在检查依赖包..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "错误：依赖包安装失败！"
    exit 1
fi

echo
echo "依赖包检查完成，开始运行自动更新..."
echo

# 运行自动更新脚本
python3 auto_update_index.py

echo
echo "更新完成！按Enter键退出..."
read 