#!/bin/bash

# Magical Athlete - Production Deployment
# For deploying to a private VPS/server

set -e

echo "⚡ Magical Athlete - Production Deployment"
echo "=========================================="
echo ""

# Configuration
APP_DIR="/opt/magical-athlete"
GIT_REPO="https://github.com/talwalkark/Game-1.git"
PORT=5000

echo "📋 Deployment Configuration:"
echo "  Directory: $APP_DIR"
echo "  Port: $PORT"
echo "  Repository: $GIT_REPO"
echo ""

# Step 1: Install dependencies
echo "1️⃣  Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y git curl wget python3 python3-pip python3-venv
echo "✓ Dependencies installed"
echo ""

# Step 2: Clone repository
echo "2️⃣  Cloning repository..."
if [ ! -d "$APP_DIR" ]; then
    sudo git clone "$GIT_REPO" "$APP_DIR"
else
    cd "$APP_DIR"
    sudo git pull origin main
fi
echo "✓ Repository cloned/updated"
echo ""

# Step 3: Set up Python environment
echo "3️⃣  Setting up Python virtual environment..."
cd "$APP_DIR"
sudo python3 -m venv venv
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install -r requirements.txt
echo "✓ Python environment ready"
echo ""

# Step 4: Configure environment
echo "4️⃣  Configuring environment..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    sudo cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and set SECRET_KEY!"
    sudo nano .env
fi
echo "✓ Environment configured"
echo ""

# Step 5: Create systemd service
echo "5️⃣  Creating systemd service..."
sudo tee /etc/systemd/system/magical-athlete.service > /dev/null <<EOF
[Unit]
Description=Magical Athlete Game Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT src.server:app
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable magical-athlete
echo "✓ Systemd service created"
echo ""

# Step 6: Start service
echo "6️⃣  Starting service..."
sudo systemctl start magical-athlete
echo "✓ Service started"
echo ""

# Step 7: Verify deployment
echo "7️⃣  Verifying deployment..."
sleep 2
if curl -s http://localhost:$PORT/api/health > /dev/null; then
    echo "✓ Server is running!"
else
    echo "⚠️  Server may not be responding. Check logs:"
    echo "   sudo journalctl -u magical-athlete -f"
fi
echo ""

echo "🎉 Deployment Complete!"
echo ""
echo "Next steps:"
echo "  1. Configure Nginx reverse proxy (see DEPLOYMENT.md)"
echo "  2. Set up SSL/HTTPS with Let's Encrypt"
echo "  3. Configure firewall rules"
echo "  4. Monitor service: sudo journalctl -u magical-athlete -f"
echo ""
echo "Access at: http://localhost:$PORT"
echo ""
