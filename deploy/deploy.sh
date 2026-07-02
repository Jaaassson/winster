#!/bin/bash
# Winster 阿里云部署脚本 (Nginx + Waitress + nohup)
# 使用方法: bash deploy/deploy.sh

set -e

PROJECT_DIR="/opt/winster"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
NGINX_CONF_SRC="$PROJECT_DIR/deploy/nginx/winster.conf"
NGINX_CONF_DEST="/etc/nginx/sites-available/winster"
NGINX_LINK="/etc/nginx/sites-enabled/winster"
WEB_DIR="/var/www/winster"
PID_FILE="$BACKEND_DIR/winster.pid"
LOG_FILE="$BACKEND_DIR/winster.log"

echo "=============================="
echo "  Winster 部署脚本"
echo "  Nginx + Waitress (nohup)"
echo "=============================="

# 1. 检查是否以 root 运行
if [ "$EUID" -ne 0 ]; then
  echo "请以 root 用户运行: sudo bash deploy/deploy.sh"
  exit 1
fi

# 2. 安装系统依赖
echo "[1/8] 安装系统依赖..."
apt update -y
apt install -y python3 python3-pip python3-venv nginx nodejs npm

# 3. 创建项目目录
echo "[2/8] 创建项目目录..."
mkdir -p "$WEB_DIR"

# 4. 配置后端
echo "[3/8] 配置后端 Python 虚拟环境..."
if [ ! -d "$BACKEND_DIR/venv" ]; then
  python3 -m venv "$BACKEND_DIR/venv"
fi
"$BACKEND_DIR/venv/bin/pip" install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
"$BACKEND_DIR/venv/bin/pip" install -r "$BACKEND_DIR/requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 创建 .env 文件（如果不存在）
echo "[4/8] 检查后端 .env 配置..."
if [ ! -f "$BACKEND_DIR/.env" ]; then
  SECRET_KEY=$("$BACKEND_DIR/venv/bin/python" -c "import secrets; print(secrets.token_hex(32))")
  JWT_SECRET_KEY=$("$BACKEND_DIR/venv/bin/python" -c "import secrets; print(secrets.token_hex(32))")
  cat > "$BACKEND_DIR/.env" << EOF
FLASK_ENV=production
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY
DATABASE_URL=sqlite:///./instance/app.db
UPLOAD_FOLDER=./app/static/uploads
MAX_CONTENT_LENGTH=16777216
CORS_ORIGINS=http://localhost
HOST=127.0.0.1
PORT=5000
WAITRESS_THREADS=4
EOF
  echo "  已生成 .env 文件"
else
  echo "  .env 已存在，跳过"
fi

# 6. 构建前端
echo "[5/8] 构建前端..."
cd "$FRONTEND_DIR"
npm install
npm run build

# 复制前端构建产物到 Nginx 目录
echo "[6/8] 部署前端文件到 $WEB_DIR..."
rm -rf "$WEB_DIR"/*
cp -r "$FRONTEND_DIR/dist/"* "$WEB_DIR/"

# 7. 配置 Nginx
echo "[7/8] 配置 Nginx..."
rm -f /etc/nginx/sites-enabled/default
cp "$NGINX_CONF_SRC" "$NGINX_CONF_DEST"
if [ ! -L "$NGINX_LINK" ]; then
  ln -s "$NGINX_CONF_DEST" "$NGINX_LINK"
fi
nginx -t
systemctl reload nginx
systemctl enable nginx

# 8. 启动后端 (nohup)
echo "[8/8] 启动后端服务 (nohup)..."
# 停止旧进程
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE")
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "  停止旧进程 PID: $OLD_PID"
    kill "$OLD_PID"
    sleep 2
  fi
  rm -f "$PID_FILE"
fi

# 用 nohup 启动
cd "$BACKEND_DIR"
nohup "$BACKEND_DIR/venv/bin/python" wsgi.py > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
sleep 2

# 验证进程是否启动
if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "  后端已启动, PID: $(cat "$PID_FILE")"
  echo "  日志文件: $LOG_FILE"
else
  echo "  错误: 后端启动失败，请查看日志: $LOG_FILE"
  exit 1
fi

echo ""
echo "=============================="
echo "  部署完成!"
echo "=============================="
echo ""
echo "后端管理:"
echo "  查看日志:   tail -f $LOG_FILE"
echo "  查看进程:   ps -p \$(cat $PID_FILE)"
echo "  停止后端:   kill \$(cat $PID_FILE)"
echo "  启动后端:   cd $BACKEND_DIR && nohup venv/bin/python wsgi.py > winster.log 2>&1 &"
echo ""
echo "Nginx:"
echo "  重载: nginx -t && systemctl reload nginx"
echo ""
echo "初始化数据库（首次部署）:"
echo "  cd $BACKEND_DIR && source venv/bin/activate && python init_data.py"
echo ""
echo "访问地址: http://$(hostname -I | awk '{print $1}')"
echo "后台管理: http://$(hostname -I | awk '{print $1}')/admin/login"
echo "默认账号: admin / admin123456"
