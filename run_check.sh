#!/bin/bash

# 设置脚本目录
SCRIPT_DIR="/home/jiashun/Desktop/coding/competition-notice"

# 切换到脚本目录
cd "$SCRIPT_DIR"

# 激活conda环境（如果需要）
source /home/jiashun/anaconda3/etc/profile.d/conda.sh
conda activate base

# 运行Python脚本
python3 src/check_api.py >> logs/cron.log 2>&1

# 记录执行时间
echo "$(date): Script executed" >> logs/cron.log
