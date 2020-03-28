@echo off 
cd %1
git add .
git commit -m "%2"
git push origin HEAD