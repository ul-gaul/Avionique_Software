@echo off
for /F "tokens=*" %%A in (requirements.txt) do (conda install --yes %%A
echo package installed)
pause