#!/usr/bin/env python3
"""
YouTube MP3 다운로더 빌드 스크립트
Windows용 exe 파일 생성
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    print("=" * 50)
    print("   YouTube MP3 다운로더 빌드 스크립트")
    print("=" * 50)
    print()

def install_dependencies():
    """의존성 패키지 설치"""
    print("[1/4] Python 패키지 설치 중...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ 패키지 설치 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패: {e}")
        return False
    return True

def build_exe():
    """PyInstaller로 exe 파일 빌드"""
    print("\n[2/4] PyInstaller로 exe 파일 생성 중...")
    
    cmd = [
        "pyinstaller",
        "--onefile",           # 단일 파일로 생성
        "--console",           # 콘솔 애플리케이션
        "--name", "YouTube-MP3-Downloader",
        "--add-data", "README.md" + (";" if platform.system() == "Windows" else ":") + ".",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "colorama", 
        "--hidden-import", "ffmpeg",
        "--clean",             # 이전 빌드 파일 정리
        "youtube_downloader.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ exe 파일 생성 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False

def check_build_result():
    """빌드 결과 확인"""
    print("\n[3/4] 빌드 결과 확인 중...")
    
    exe_name = "YouTube-MP3-Downloader.exe" if platform.system() == "Windows" else "YouTube-MP3-Downloader"
    exe_path = Path("dist") / exe_name
    
    if exe_path.exists():
        file_size = exe_path.stat().st_size
        print(f"✅ 성공: {exe_name} 생성됨")
        print(f"📁 위치: {exe_path.absolute()}")
        print(f"📏 크기: {file_size / (1024*1024):.1f} MB")
        return True
    else:
        print(f"❌ 오류: {exe_name} 파일이 생성되지 않았습니다")
        return False

def print_usage():
    """사용법 안내"""
    print("\n[4/4] 사용법:")
    print("1. FFmpeg 설치 필요:")
    print("   - Windows: https://ffmpeg.org/download.html")
    print("   - 또는 winget install FFmpeg")
    print("2. YouTube-MP3-Downloader.exe 실행")
    print("3. 프로그램 안내에 따라 사용")
    print()
    print("=" * 50)
    print("       빌드 완료! 🎉")
    print("=" * 50)

def main():
    print_banner()
    
    # 운영체제 확인
    if platform.system() != "Windows":
        print("⚠️  주의: Windows가 아닌 환경에서 실행 중입니다.")
        print("Windows용 exe 파일을 생성하지만 테스트할 수 없습니다.")
        print()
    
    # 빌드 프로세스 실행
    if not install_dependencies():
        sys.exit(1)
    
    if not build_exe():
        sys.exit(1)
    
    if not check_build_result():
        sys.exit(1)
    
    print_usage()

if __name__ == "__main__":
    main() 