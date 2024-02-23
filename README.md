# youtube_downloader_app
- URLから，動画やプレイリストを一括でダウンロードするアプリケーションです．
- 音声のみのダウンロードにも対応しています．

# requirements
- ffmpeg (https://ffmpeg.org/download.html)
- yt-dlp (python library)

# setting
C:.
├─main.py
├─download.py
│ 
├─ffmpeg
│  │  
│  └─bin
│          ffmpeg.exe
│          ffplay.exe
│          ffprobe.exe
│        
└─yt-dlp

# How to use
1. このリポジトリからソースコードをダウンロードし，
2. ffmpegをダウンロードし，settingと同様の階層構造にする．
3. pip install で yt-dlpをインストール
4. main.pyを実行
