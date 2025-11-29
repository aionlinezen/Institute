# Task Manager Deployment Guide

## Local Development

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Git (optional)

### Setup Steps
```bash
# 1. Clone or download project
git clone <repository-url>
cd task-manager

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py
```

### Access Application
- Open browser to `http://localhost:5000`
- Tasks saved to `tasks.json` in project directory

## Production Deployment

### Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

#### Deployment Steps
```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create your-task-manager-app

# 3. Deploy application
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# 4. Open application
heroku open
```

#### Required Files (Already Included)
- `Procfile`: `web: gunicorn app:app`
- `runtime.txt`: `python-3.11.0`
- `requirements.txt`: Flask and gunicorn dependencies

### AWS Elastic Beanstalk

#### Prerequisites
- AWS account
- EB CLI installed

#### Deployment Steps
```bash
# 1. Initialize EB application
eb init

# 2. Create environment
eb create task-manager-env

# 3. Deploy application
eb deploy

# 4. Open application
eb open
```

#### Configuration
Create `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app.py
```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Build and Run
```bash
# Build image
docker build -t task-manager .

# Run container
docker run -p 5000:5000 -v $(pwd)/tasks.json:/app/tasks.json task-manager
```

### VPS/Server Deployment

#### Using Nginx + Gunicorn

##### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash taskmanager
sudo su - taskmanager
```

##### 2. Application Setup
```bash
# Clone application
git clone <repository-url> /home/taskmanager/app
cd /home/taskmanager/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

##### 3. Gunicorn Service
Create `/etc/systemd/system/taskmanager.service`:
```ini
[Unit]
Description=Task Manager Web App
After=network.target

[Service]
User=taskmanager
Group=taskmanager
WorkingDirectory=/home/taskmanager/app
Environment="PATH=/home/taskmanager/app/venv/bin"
ExecStart=/home/taskmanager/app/venv/bin/gunicorn --workers 3 --bind unix:taskmanager.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

##### 4. Nginx Configuration
Create `/etc/nginx/sites-available/taskmanager`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/taskmanager/app/taskmanager.sock;
    }
}
```

##### 5. Enable Services
```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl start taskmanager
sudo systemctl enable taskmanager

sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Environment Configuration

### Environment Variables
```bash
# Port configuration
export PORT=8000

# Debug mode (development only)
export FLASK_DEBUG=1

# Custom task file location
export TASK_FILE=/path/to/custom/tasks.json
```

### Application Configuration
Modify `app.py` for environment-specific settings:
```python
import os

# Port configuration
port = int(os.environ.get('PORT', 5000))

# Debug mode
debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Custom task file
task_file = os.environ.get('TASK_FILE', 'tasks.json')
manager = TaskManager(task_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=debug)
```

## Security Considerations

### Production Security
```python
# Disable debug mode
app.run(debug=False)

# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SECRET_KEY'] = SECRET_KEY

# Add CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### File Permissions
```bash
# Secure task file
chmod 600 tasks.json
chown taskmanager:taskmanager tasks.json

# Secure application directory
chmod -R 755 /home/taskmanager/app
chown -R taskmanager:taskmanager /home/taskmanager/app
```

### Firewall Configuration
```bash
# Allow HTTP traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

## Monitoring & Logging

### Application Logs
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# Add to routes
@app.route('/add', methods=['POST'])
def add_task():
    app.logger.info(f"Adding task: {request.form.get('name')}")
    # ... rest of function
```

### System Monitoring
```bash
# Check service status
sudo systemctl status taskmanager

# View logs
sudo journalctl -u taskmanager -f

# Monitor resource usage
htop
```

## Backup & Recovery

### Data Backup
```bash
# Backup task data
cp tasks.json tasks_backup_$(date +%Y%m%d).json

# Automated backup script
#!/bin/bash
BACKUP_DIR="/home/taskmanager/backups"
mkdir -p $BACKUP_DIR
cp /home/taskmanager/app/tasks.json $BACKUP_DIR/tasks_$(date +%Y%m%d_%H%M%S).json

# Keep only last 30 days
find $BACKUP_DIR -name "tasks_*.json" -mtime +30 -delete
```

### Cron Job for Backups
```bash
# Add to crontab
crontab -e

# Backup daily at 2 AM
0 2 * * * /home/taskmanager/backup_script.sh
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>

# Or use different port
export PORT=8000
python app.py
```

#### Permission Denied
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod 644 tasks.json
```

#### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Service Won't Start
```bash
# Check service logs
sudo journalctl -u taskmanager -n 50

# Check configuration
sudo systemctl daemon-reload
sudo systemctl restart taskmanager
```

### Performance Optimization

#### Gunicorn Workers
```bash
# Calculate optimal workers: (2 x CPU cores) + 1
gunicorn --workers 5 --bind 0.0.0.0:5000 app:app
```

#### Nginx Caching
Add to nginx configuration:
```nginx
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Scaling Considerations

### Database Migration
For larger deployments, consider migrating from JSON to database:
```python
# SQLite example
import sqlite3

class DatabaseTaskManager:
    def __init__(self, db_path='tasks.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                priority INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
```

### Load Balancing
For high traffic, use multiple application instances:
```nginx
upstream taskmanager {
    server unix:/home/taskmanager/app1/taskmanager.sock;
    server unix:/home/taskmanager/app2/taskmanager.sock;
}

server {
    location / {
        proxy_pass http://taskmanager;
    }
}
```