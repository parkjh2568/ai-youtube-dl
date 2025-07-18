# YouTube MP3 다운로더 (Created By Cursor) 🎵

3시간 이상의 긴 유튜브 영상을 고품질 MP3로 변환하는 고성능 다운로더입니다.

## ✨ 주요 기능

- 🎯 **3시간 이상 긴 영상 전용**: 긴 영상도 효율적으로 처리
- 🎵 **다양한 오디오 형식**: MP3 (192kbps/320kbps), FLAC (무손실 변환)
- 📊 **실시간 진행 상황**: 다운로드 진행률, 속도, 남은 시간 표시
- 🔍 **영상 정보 미리보기**: 제목, 길이, 채널, 조회수 확인
- 🎨 **컬러풀한 UI**: 직관적인 컬러 인터페이스
- ⚡ **고성능**: yt-dlp와 FFmpeg 기반 최적화

## 📋 시스템 요구사항

- Python 3.7 이상
- FFmpeg (오디오 변환용)
- 안정적인 인터넷 연결

## 🛠️ 설치 방법

### 1. 레포지토리 클론 또는 다운로드

```bash
# 현재 디렉토리에서 파일들을 사용
```

### 2. FFmpeg 설치

#### macOS (Homebrew)
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Windows
[FFmpeg 공식 사이트](https://ffmpeg.org/download.html)에서 다운로드하여 설치

### 3. Python 패키지 설치

```bash
pip install -r requirements.txt
```

## 💻 Windows exe 파일 빌드

Windows에서 실행 가능한 단일 exe 파일을 생성할 수 있습니다.

### 방법 1: 배치 파일 사용 (추천)
```cmd
build.bat
```

### 방법 2: Python 스크립트 사용
```bash
python build.py
```

### 빌드 후:
- `dist/YouTube-MP3-Downloader.exe` 파일이 생성됩니다
- FFmpeg가 설치된 Windows PC에서 실행 가능
- 단일 exe 파일로 어디서나 실행 가능 (약 50-100MB)

### Windows에서 FFmpeg 설치:
```cmd
# winget 사용 (Windows 10/11)
winget install FFmpeg

# 또는 수동 설치
# https://ffmpeg.org/download.html
```

### 방법 3: GitHub Actions 자동 빌드 (모든 플랫폼)
GitHub에서 자동으로 Windows/macOS/Linux용 실행 파일을 빌드합니다:

1. **릴리즈 생성**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **자동 빌드**: GitHub Actions가 자동으로 모든 플랫폼용 실행 파일 생성

3. **다운로드**: [Releases 페이지](https://github.com/parkjh2568/ai-youtube-dl/releases)에서 다운로드

#### 💻 크로스 플랫폼 빌드 지원:
- ✅ **Windows**: `YouTube-MP3-Downloader.exe`
- ✅ **macOS**: `YouTube-MP3-Downloader-macos` (Intel/Apple Silicon)
- ✅ **Linux**: `YouTube-MP3-Downloader-linux`

> **참고**: macOS에서 빌드한 파일은 Windows에서 실행되지 않습니다. 각 플랫폼별로 빌드가 필요합니다.

### 🍎 macOS 보안 이슈 해결법

macOS에서 "개발자를 확인할 수 없음" 오류가 나타날 경우:

#### 방법 1: 우클릭으로 실행
1. 파일을 **우클릭** → **열기** 클릭
2. "열기" 버튼 클릭하여 실행

#### 방법 2: 시스템 설정에서 허용
1. **시스템 설정** → **개인정보 보호 및 보안**
2. **보안** 섹션에서 "확인되지 않은 개발자" 메시지 옆 **"그래도 열기"** 클릭

#### 방법 3: 터미널에서 실행 (추천)
```bash
# 다운로드 후
chmod +x YouTube-MP3-Downloader-macos
./YouTube-MP3-Downloader-macos
```

#### 방법 4: Gatekeeper 임시 해제 (고급 사용자)
```bash
# 임시 해제
sudo spctl --master-disable

# 실행 후 다시 활성화
sudo spctl --master-enable
```

> 📚 **더 자세한 해결법**: [macOS 보안 이슈 완전 가이드](MACOS_SECURITY.md)를 참고하세요!

## 🚀 사용 방법

### 기본 실행

```bash
python youtube_downloader.py
```

### 사용 단계

1. 프로그램을 실행합니다
2. 오디오 형식을 선택합니다 (MP3 192kbps/320kbps 또는 FLAC)
3. 유튜브 URL을 입력합니다
4. 영상 정보를 확인합니다
5. 3시간 미만 영상의 경우 확인 메시지가 나타납니다
6. 다운로드가 시작되며 진행 상황이 실시간으로 표시됩니다
7. 완료되면 `downloads` 폴더에 MP3 파일이 저장됩니다

### 예시 사용법

```
🎵 오디오 형식을 선택하세요:
1. MP3 192kbps (표준 고품질) - 빠른 다운로드
2. MP3 320kbps (최고 품질) - 더 큰 파일 크기
3. FLAC (무손실 변환) - 가장 큰 파일 크기
   ⚠️  주의: 유튜브는 이미 손실 압축된 오디오를 제공하므로 진정한 무손실은 아닙니다
선택 (1-3): 3
✅ FLAC 선택됨 (무손실 변환)
   📝 참고: 유튜브 원본 품질을 그대로 보존하여 FLAC으로 변환합니다

유튜브 URL을 입력하세요 (종료하려면 'q' 입력):
URL: https://www.youtube.com/watch?v=example123

📋 영상 정보
제목: 긴 음악 모음집
길이: 03:45:30
채널: 음악채널
조회수: 1,234,567
형식: FLAC (무손실 변환)

✅ 3시간 이상의 긴 영상입니다. (3.8시간)

🚀 다운로드를 시작합니다...
다운로드 중: ████████████████████████████████ 65% | 속도: 2.1MB/s | 남은 시간: 02:15
```

## 📁 출력 파일

- **저장 위치**: `./downloads/` 폴더
- **파일 형식**: MP3 (192kbps/320kbps) 또는 FLAC (무손실 변환)
- **파일명**: 유튜브 영상 제목 기반

## ⚙️ 고급 설정

### 오디오 형식 옵션
- **MP3 192kbps**: 표준 고품질, 빠른 다운로드, 작은 파일 크기
- **MP3 320kbps**: 최고 품질, 더 큰 파일 크기 (약 1.7배)
- **FLAC**: 무손실 변환, 가장 큰 파일 크기 (약 5-10배)

### 🎵 FLAC에 대한 중요한 정보
- **현실**: 유튜브는 이미 손실 압축된 오디오만 제공 (주로 Opus 128-160kbps)
- **장점**: 향후 재압축 시 품질 손실 없음, 최대한 원본 품질 보존
- **단점**: 파일 크기가 매우 큼, 다운로드 시간 증가
- **추천**: 음질에 매우 민감하거나 보관용으로 사용할 때만 선택

### 코드 설정 변경
```python
# 기본 오디오 형식 변경
self.audio_quality = '320'  # 기본값을 320kbps로 설정
self.audio_format = 'flac'  # 기본값을 FLAC으로 설정
```

### 저장 위치 변경
```python
downloader = YouTubeMP3Downloader(download_path="./my_music")
```

## 🔧 문제 해결

### 일반적인 오류

1. **FFmpeg 오류**: FFmpeg가 설치되지 않았거나 PATH에 없는 경우
2. **네트워크 오류**: 인터넷 연결이 불안정한 경우
3. **권한 오류**: 저장 폴더에 쓰기 권한이 없는 경우
4. **URL 오류**: 유효하지 않은 유튜브 URL인 경우

### 해결 방법

```bash
# FFmpeg 설치 확인
ffmpeg -version

# 패키지 재설치
pip install --upgrade yt-dlp

# 권한 확인
ls -la ./downloads/
```

## 📄 라이선스

이 프로젝트는 자유롭게 사용할 수 있습니다.

## ⚠️ 주의사항

- 저작권이 있는 콘텐츠의 다운로드는 해당 저작권법을 준수해야 합니다
- 개인적인 용도로만 사용하시기 바랍니다
- 대용량 파일 다운로드 시 충분한 저장 공간을 확보하세요

---

## 🤖 Built with AI

이 프로젝트는 **Cursor AI**와 **Claude Sonnet 4**를 사용하여 제작되었습니다! 🚀

- **AI 페어 프로그래밍**: Cursor의 AI 어시스턴트와 함께 개발
- **고품질 코드**: Claude Sonnet 4의 코딩 능력으로 최적화
- **사용자 중심 설계**: AI가 사용자 경험을 고려한 직관적 인터페이스 구현
- **실시간 개발**: 자연어로 요구사항 전달 → 즉시 고품질 코드 생성

### 🎯 AI 개발의 장점
- ⚡ **빠른 개발**: 복잡한 기능을 몇 분 만에 구현
- 🔍 **버그 없는 코드**: AI가 실시간으로 오류 검토 및 수정
- 📚 **최신 기술 적용**: 최적화된 라이브러리와 베스트 프랙티스 자동 적용
- 🎨 **사용자 친화적**: 직관적인 UI/UX 설계

> *"AI와 함께라면 누구나 개발자가 될 수 있습니다!"* 🤖✨

---

**🎵 긴 유튜브 영상을 고품질 MP3로 즐기세요! 🎵** 