@echo off
echo Bat dau chay test cases...
> results.txt echo KET QUA TEST ASSIGNMENT 2

set ALGOS=dfs bfs gbfs astar cus1 cus2
set TEST_DIR=cases

for %%a in (%ALGOS%) do (
    
    for %%f in ("%TEST_DIR%\*.txt") do (
        echo Dang chay %%a voi %%~nxf...
        
        echo ---- %%~nxf ^| %%a ---- >> results.txt
        
        python search.py "%%~f" %%a >> results.txt
        echo. >> results.txt
    )
)
echo Hoan thanh! Hay kiem tra file results.txt.
pause