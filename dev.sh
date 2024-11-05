#!/bin/bash
cd /home/jiancheng/Desktop/prod-erp/jiancheng
tmux new-session -d "cd frontend/jiancheng/ && npm run dev -- --host"
tmux split-window -d "cd backend-python/ && python3 main.py"
tmux split-window -d "cd /home/jiancheng/Desktop/imgserver && python3 -m http.server 12667"
tmux split-window -d 
tmux attach
