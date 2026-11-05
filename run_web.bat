@echo off
title DeepDTA Web Platform
echo ======================================================================
echo           Starting DeepDTA Web Application Platform
echo ======================================================================
echo.
echo Launching server at http://127.0.0.1:8000 ...
start http://127.0.0.1:8000
echo.
"C:\Users\Rishitha\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn web.app:app --host 127.0.0.1 --port 8000
pause

