#!/bin/bash

# Magical Athlete - Quick Deployment Script
# This script handles server deployment and management

set -e

echo "⚡ Magical Athlete Deployment Script"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"
echo ""

# Main menu
while true; do
    echo "Choose action:"
    echo "  1) Start server"
    echo "  2) Stop server"
    echo "  3) View logs"
    echo "  4) Rebuild container"
    echo "  5) Full restart"
    echo "  6) Health check"
    echo "  7) Exit"
    echo ""
    read -p "Enter choice (1-7): " choice

    case $choice in
        1)
            echo -e "${YELLOW}🚀 Starting Magical Athlete server...${NC}"
            docker-compose up -d
            echo -e "${GREEN}✓ Server started!${NC}"
            echo "Access at: http://localhost:5000"
            echo ""
            ;;
        2)
            echo -e "${YELLOW}🛑 Stopping server...${NC}"
            docker-compose down
            echo -e "${GREEN}✓ Server stopped${NC}"
            echo ""
            ;;
        3)
            echo -e "${YELLOW}📋 Server logs:${NC}"
            docker-compose logs -f --tail=50 magical-athlete
            ;;
        4)
            echo -e "${YELLOW}🔨 Rebuilding container...${NC}"
            docker-compose build --no-cache
            echo -e "${GREEN}✓ Container rebuilt${NC}"
            echo ""
            ;;
        5)
            echo -e "${YELLOW}♻️  Full restart...${NC}"
            docker-compose down
            docker-compose up -d
            echo -e "${GREEN}✓ Server restarted${NC}"
            echo "Access at: http://localhost:5000"
            echo ""
            ;;
        6)
            echo -e "${YELLOW}🏥 Health check...${NC}"
            if curl -s http://localhost:5000/api/health > /dev/null; then
                echo -e "${GREEN}✓ Server is healthy${NC}"
                curl -s http://localhost:5000/api/health | python -m json.tool
            else
                echo -e "${RED}❌ Server is not responding${NC}"
            fi
            echo ""
            ;;
        7)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            echo ""
            ;;
    esac
done
