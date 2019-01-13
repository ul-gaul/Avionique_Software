for /F "tokens=*" %%A in (requirements.txt) do (conda install --yes %%A || pip3 install %%A)
pause