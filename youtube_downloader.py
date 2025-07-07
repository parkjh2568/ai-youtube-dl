#!/usr/bin/env python3
"""
YouTube MP3 다운로더
3시간 이상의 긴 영상도 효율적으로 MP3로 변환하는 고성능 다운로더
"""

import os
import sys
import re
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yt_dlp
from colorama import init, Fore, Style, Back

# 컬러 출력 초기화
init()

class YouTubeMP3Downloader:
    def __init__(self, download_path="./downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        self.audio_quality = '192'  # 기본값
        self.audio_format = 'mp3'  # 기본값
        
        # yt-dlp 기본 설정
        self.base_ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'postprocessor_args': [
                '-ac', '2',  # 스테레오
                '-ar', '44100',  # 44.1kHz 샘플링
            ],
            'embed_subs': False,
            'writesubtitles': False,
            'writeinfojson': False,
            'ignoreerrors': False,
        }
    
    def set_audio_quality(self, quality, format_type='mp3'):
        """오디오 품질 및 형식 설정"""
        self.audio_quality = quality
        self.audio_format = format_type
        
        # yt-dlp 옵션 업데이트
        self.ydl_opts = self.base_ydl_opts.copy()
        
        if format_type == 'flac':
            # FLAC 무손실 변환 설정
            self.ydl_opts.update({
                'audioformat': 'flac',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '0',  # FLAC에서는 0이 최고 품질
                }],
            })
        else:
            # MP3 설정
            self.ydl_opts.update({
                'audioformat': 'mp3',
                'audioquality': f'{quality}K',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
            })
    
    def print_banner(self):
        """배너 출력"""
        print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                     YouTube MP3 다운로더                       ║
║                     3시간+ 긴 영상 전용                        ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """)
    
    def select_audio_quality(self):
        """오디오 품질 및 형식 선택"""
        print(f"\n{Fore.CYAN}🎵 오디오 형식을 선택하세요:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. MP3 192kbps (표준 고품질) - 빠른 다운로드{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. MP3 320kbps (최고 품질) - 더 큰 파일 크기{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. FLAC (무손실 변환) - 가장 큰 파일 크기{Style.RESET_ALL}")
        print(f"{Fore.RED}   ⚠️  주의: 유튜브는 이미 손실 압축된 오디오를 제공하므로 진정한 무손실은 아닙니다{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}선택 (1-3): {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.set_audio_quality('192', 'mp3')
                    print(f"{Fore.GREEN}✅ MP3 192kbps 선택됨{Style.RESET_ALL}")
                    return
                elif choice == '2':
                    self.set_audio_quality('320', 'mp3')
                    print(f"{Fore.GREEN}✅ MP3 320kbps 선택됨 (최고 품질){Style.RESET_ALL}")
                    return
                elif choice == '3':
                    self.set_audio_quality('best', 'flac')
                    print(f"{Fore.GREEN}✅ FLAC 선택됨 (무손실 변환){Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   📝 참고: 유튜브 원본 품질을 그대로 보존하여 FLAC으로 변환합니다{Style.RESET_ALL}")
                    return
                else:
                    print(f"{Fore.RED}잘못된 선택입니다. 1, 2, 또는 3을 입력하세요.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}선택이 취소되었습니다.{Style.RESET_ALL}")
                return
    
    def is_valid_youtube_url(self, url):
        """유튜브 URL 유효성 검사"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info(self, url):
        """비디오 정보 가져오기"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown')
                }
        except Exception as e:
            raise Exception(f"비디오 정보를 가져올 수 없습니다: {str(e)}")
    
    def format_duration(self, seconds):
        """초를 시:분:초 형태로 변환"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_number(self, num):
        """숫자를 천 단위로 구분하여 포맷팅"""
        return f"{num:,}"
    
    def progress_hook(self, d):
        """다운로드 진행 상황 표시"""
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                
                # 진행률 바 생성
                if '_percent_str' in d:
                    percent_num = float(d['_percent_str'].replace('%', ''))
                    bar_length = 50
                    filled_length = int(bar_length * percent_num / 100)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    
                    print(f'\r{Fore.GREEN}다운로드 중: {bar} {percent} | 속도: {speed} | 남은 시간: {eta}{Style.RESET_ALL}', end='')
                else:
                    print(f'\r{Fore.GREEN}다운로드 중... 속도: {speed} | 남은 시간: {eta}{Style.RESET_ALL}', end='')
            except:
                print(f'\r{Fore.GREEN}다운로드 중...{Style.RESET_ALL}', end='')
        
        elif d['status'] == 'finished':
            print(f'\n{Fore.YELLOW}다운로드 완료! MP3 변환 중...{Style.RESET_ALL}')
    
    def download_mp3(self, url):
        """MP3 다운로드 및 변환"""
        try:
            # URL 유효성 검사
            if not self.is_valid_youtube_url(url):
                raise Exception("유효하지 않은 유튜브 URL입니다.")
            
            print(f"{Fore.YELLOW}📹 비디오 정보를 가져오는 중...{Style.RESET_ALL}")
            
            # 비디오 정보 가져오기
            video_info = self.get_video_info(url)
            
            # 영상 정보 출력
            print(f"\n{Fore.CYAN}📋 영상 정보{Style.RESET_ALL}")
            print(f"제목: {Fore.WHITE}{video_info['title']}{Style.RESET_ALL}")
            print(f"길이: {Fore.WHITE}{self.format_duration(video_info['duration'])}{Style.RESET_ALL}")
            print(f"채널: {Fore.WHITE}{video_info['uploader']}{Style.RESET_ALL}")
            print(f"조회수: {Fore.WHITE}{self.format_number(video_info['view_count'])}{Style.RESET_ALL}")
            
            # 오디오 형식 정보 표시
            if self.audio_format == 'flac':
                print(f"형식: {Fore.WHITE}FLAC (무손실 변환){Style.RESET_ALL}")
            else:
                print(f"형식: {Fore.WHITE}MP3 {self.audio_quality}kbps{Style.RESET_ALL}")
            
            # 3시간 이상인지 확인
            duration_hours = video_info['duration'] / 3600
            if duration_hours < 3:
                print(f"\n{Fore.RED}⚠️  경고: 이 영상은 {duration_hours:.1f}시간입니다. 3시간 미만의 영상입니다.{Style.RESET_ALL}")
                response = input(f"{Fore.YELLOW}계속 다운로드하시겠습니까? (y/n): {Style.RESET_ALL}")
                if response.lower() != 'y':
                    print(f"{Fore.RED}다운로드가 취소되었습니다.{Style.RESET_ALL}")
                    return False
            else:
                print(f"\n{Fore.GREEN}✅ 3시간 이상의 긴 영상입니다. ({duration_hours:.1f}시간){Style.RESET_ALL}")
            
            # 진행 상황 표시를 위한 hook 추가
            self.ydl_opts['progress_hooks'] = [self.progress_hook]
            
            print(f"\n{Fore.CYAN}🚀 다운로드를 시작합니다...{Style.RESET_ALL}")
            start_time = time.time()
            
            # 다운로드 실행
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"\n{Fore.GREEN}🎉 다운로드 완료!{Style.RESET_ALL}")
            print(f"소요 시간: {Fore.WHITE}{self.format_duration(int(elapsed_time))}{Style.RESET_ALL}")
            print(f"저장 위치: {Fore.WHITE}{self.download_path.absolute()}{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ 오류 발생: {str(e)}{Style.RESET_ALL}")
            return False
    
    def run(self):
        """메인 실행 함수"""
        self.print_banner()
        
        # 음질 선택 (프로그램 시작 시 한 번만)
        self.select_audio_quality()
        
        while True:
            try:
                print(f"\n{Fore.CYAN}유튜브 URL을 입력하세요 (종료하려면 'q' 입력):{Style.RESET_ALL}")
                url = input(f"{Fore.YELLOW}URL: {Style.RESET_ALL}").strip()
                
                if url.lower() == 'q':
                    print(f"\n{Fore.CYAN}프로그램을 종료합니다. 안녕히 가세요!{Style.RESET_ALL}")
                    break
                
                if not url:
                    print(f"{Fore.RED}URL을 입력해주세요.{Style.RESET_ALL}")
                    continue
                
                success = self.download_mp3(url)
                
                if success:
                    print(f"\n{Fore.GREEN}다른 영상을 다운로드하시겠습니까?{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}다시 시도하시겠습니까?{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}프로그램을 종료합니다. 안녕히 가세요!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}예상치 못한 오류가 발생했습니다: {str(e)}{Style.RESET_ALL}")


def main():
    """메인 함수"""
    try:
        # FFmpeg 설치 확인
        if os.system("ffmpeg -version > /dev/null 2>&1") != 0:
            print(f"{Fore.RED}⚠️  FFmpeg가 설치되지 않았습니다.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}macOS: brew install ffmpeg{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Ubuntu: sudo apt install ffmpeg{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Windows: https://ffmpeg.org/download.html{Style.RESET_ALL}")
            return
        
        downloader = YouTubeMP3Downloader()
        downloader.run()
        
    except Exception as e:
        print(f"{Fore.RED}프로그램 실행 중 오류가 발생했습니다: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main() 