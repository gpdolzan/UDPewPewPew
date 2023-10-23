@echo off
set "input=%~1"
set "output=%~2"

if "%output%"=="" set "output=%~n1_compressed.ts"

ffmpeg -i "%input%" -c:v libx264 -crf 28 -preset veryslow -b:v 500k -vf "scale=-1920:1080" -r 30 -c:a aac -b:a 96k -strict experimental -f mpegts "%output%"

echo Conversion finished.
