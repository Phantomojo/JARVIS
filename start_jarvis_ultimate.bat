@echo off
echo Starting JARVIS Ultimate in WSL...
wsl -d Ubuntu -e bash -c "cd /home/%USERNAME%/JARVIS && ./start_jarvis_ultimate.sh"
pause
