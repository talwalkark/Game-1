# Magical Athlete - Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone and navigate to repo:**
```bash
cd Game-1
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
```

Edit `.env` and set:
```
PORT=5000
DEBUG=True
SECRET_KEY=your-secret-key-here
```

5. **Run the server:**
```bash
python -m src.server
```

Server will be available at: `http://localhost:5000`

---

## Docker Deployment (Recommended for Production)

### With Docker Compose (Simplest)

1. **Build and run:**
```bash
docker-compose up -d
```

Server will be available at: `http://localhost:5000`

2. **View logs:**
```bash
docker-compose logs -f magical-athlete
```

3. **Stop:**
```bash
docker-compose down
```

### Manual Docker Commands

1. **Build image:**
```bash
docker build -t magical-athlete:latest .
```

2. **Run container:**
```bash
docker run -d \
  --name magical-athlete \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  magical-athlete:latest
```

3. **Access logs:**
```bash
docker logs -f magical-athlete
```

---

## Private Server Deployment

### On Your Own Server (VPS/Home Server)

#### Option 1: Direct Python (Recommended for low traffic)

1. **SSH into your server**

2. **Clone repository:**
```bash
git clone https://github.com/talwalkark/Game-1.git
cd Game-1
```

3. **Setup Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure:**
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

5. **Run with Gunicorn (production):**
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 src.server:app
```

#### Option 2: Docker on Private Server (Recommended for reliability)

1. **SSH into your server**

2. **Install Docker and Docker Compose:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone and deploy:**
```bash
git clone https://github.com/talwalkark/Game-1.git
cd Game-1
docker-compose up -d
```

#### Option 3: Systemd Service (Advanced - Ubuntu/Debian)

Create `/etc/systemd/system/magical-athlete.service`:

```ini
[Unit]
Description=Magical Athlete Game Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/magical-athlete
Environment="PATH=/opt/magical-athlete/venv/bin"
ExecStart=/opt/magical-athlete/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 src.server:app
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable magical-athlete
sudo systemctl start magical-athlete
sudo systemctl status magical-athlete
```

---

## Using Reverse Proxy (Recommended for Production)

### Nginx Configuration

1. **Install Nginx:**
```bash
sudo apt-get install nginx
```

2. **Create config** `/etc/nginx/sites-available/magical-athlete`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change to your domain
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # SocketIO specific
        proxy_buffering off;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

3. **Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/magical-athlete /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/HTTPS with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env` to a random string
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS/SSL for web access
- [ ] Set firewall rules to only allow necessary ports (80, 443, 5000)
- [ ] Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- [ ] Use systemd service or Docker for automatic restarts
- [ ] Set up monitoring/logging for production

---

## Network Access

### Local Network Only

Edit `.env`:
```
SERVER_MODE=local
```

Run on specific IP:
```bash
python -m src.server --host 192.168.1.100 --port 5000
```

### Public Internet

1. Use reverse proxy with HTTPS
2. Set `CORS_ALLOWED_ORIGINS` in server.py if needed
3. Open firewall ports 80/443

### Port Forwarding (Home Server)

1. Forward ports 80→8080 and 443→8443 on your router
2. Use reverse proxy to handle traffic
3. Point domain to your public IP (use DDNS if dynamic)

---

## Troubleshooting

**Port already in use:**
```bash
lsof -i :5000  # Find process
kill -9 <PID>   # Kill process
```

**Connection refused:**
- Check firewall: `sudo ufw status`
- Check if server is running: `ps aux | grep python`
- Check logs: `docker-compose logs`

**SocketIO not connecting:**
- Ensure WebSocket support in reverse proxy
- Check CORS settings in src/server.py
- Verify no middleware blocking upgrades

**Memory issues:**
- Reduce worker count in gunicorn
- Check for memory leaks in game manager
- Use monitoring: `docker stats`

---

## Monitoring & Maintenance

```bash
# View active connections
netstat -an | grep 5000

# Check logs
journalctl -u magical-athlete -f  # Systemd
docker-compose logs -f             # Docker

# Update dependencies
pip list --outdated
pip install --upgrade -r requirements.txt

# Backup game data
tar -czf backup.tar.gz .
```

---

## Performance Tips

1. **Use Gunicorn with multiple workers** for high load:
```bash
gunicorn --worker-class eventlet -w 4 --bind 0.0.0.0:5000 src.server:app
```

2. **Add Redis** for session management (future enhancement)

3. **Use CDN** for static files

4. **Monitor server resources:**
```bash
docker stats  # If using Docker
htop          # System monitoring
```

---

For more help, check server logs or open an issue on GitHub.
