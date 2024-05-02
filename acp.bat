echo off
set message=%1
set username=%2
git add .
git commit -m %message% %username%
git push
