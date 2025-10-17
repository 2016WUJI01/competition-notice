# WCA比赛变更通知

自动监控WCA中国区比赛信息变更，通过邮件及时通知。

## 功能

- 每5分钟检测WCA中国区比赛API
- 比赛信息变更时自动邮件通知
- 支持GitHub Actions云端运行或本地cron部署

## GitHub Actions部署（推荐）

1. **Fork本项目**

2. **配置邮箱信息**

   在仓库Settings > Secrets and variables > Actions中添加：
   - `EMAIL_USER`: 发送邮箱（如：`your-email@163.com`）
   - `EMAIL_PASS`: 邮箱授权码
   - `EMAIL_TO`: 接收邮箱（支持多个邮箱，用逗号分隔，如：`email1@example.com,email2@example.com`）

3. **启用Actions**

   进入Actions页面启用工作流，将自动每5分钟检测一次

## 本地部署

### 环境准备

```bash
git clone https://github.com/your-username/competition-notice.git
cd competition-notice
pip install -r requirements.txt
```

### 配置环境变量

创建`.env`文件：

```bash
EMAIL_USER=your-email@163.com
EMAIL_PASS=your-auth-code
EMAIL_TO=notify@example.com
# 或者配置多个接收邮箱（用逗号分隔）
# EMAIL_TO=email1@example.com,email2@example.com,email3@example.com
```

### 运行方式

**手动运行**：

```bash
python src/check_api.py
```

**定时运行（Linux/macOS）**：

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每5分钟）
echo "*/5 * * * * /home/jiashun/Desktop/coding/competition-notice/run_check.sh" | crontab -
```

**定时运行（Windows）**：
使用任务计划程序创建定时任务，设置每5分钟运行一次`python src/check_api.py`

## 常见问题

**邮件发送失败**：检查邮箱授权码和SMTP设置

**修改检测频率**：编辑`.github/workflows/check_api.yml`中的cron表达式

**更换邮箱服务商**：修改`src/check_api.py`中的SMTP配置
