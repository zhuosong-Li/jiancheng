#!/bin/bash
cd /home/desktop/Desktop/jiancheng
tmux new-session -d "cd frontend/jiancheng/ && npm run dev"
tmux split-window -d "cd backend-python/ && python3 main.py"
tmux split-window -d "cd /home/desktop/Desktop/imageserver && python3 -m http.server 12667"
tmux split-window -d 
tmux attach
