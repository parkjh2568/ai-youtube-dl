@echo off
echo ================================
echo   YouTube MP3 다운로더 빌드
echo ================================

echo.
echo [1/4] Python 패키지 설치 중...
pip install -r requirements.txt

echo.
echo [2/4] PyInstaller로 exe 파일 생성 중...
pyinstaller --onefile --console --name "YouTube-MP3-Downloader" ^
    --add-data "README.md;." ^
    --hidden-import "yt_dlp" ^
    --hidden-import "colorama" ^
    --hidden-import "ffmpeg" ^
    --clean ^
    youtube_downloader.py

echo.
echo [3/4] 빌드 완료! 파일 확인 중...
if exist "dist\YouTube-MP3-Downloader.exe" (
    echo ✅ 성공: YouTube-MP3-Downloader.exe 생성됨
    echo 📁 위치: %cd%\dist\YouTube-MP3-Downloader.exe
    echo 📏 크기: 
    dir "dist\YouTube-MP3-Downloader.exe" | findstr YouTube-MP3-Downloader.exe
) else (
    echo ❌ 오류: exe 파일 생성 실패
    pause
    exit /b 1
)

echo.
echo [4/4] 사용법:
echo 1. FFmpeg 설치 필요: https://ffmpeg.org/download.html
echo 2. YouTube-MP3-Downloader.exe 실행
echo 3. 프로그램 안내에 따라 사용

echo.
echo ================================
echo      빌드 완료! 🎉
echo ================================
pause 