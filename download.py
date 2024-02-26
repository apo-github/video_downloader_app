"""youtubeの再生リストを一括ダウンロードするプログラム

・動画取得にyt-dlpを使用: https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE
・FFmpegを動的リンクとして使用: https://github.com/FFmpeg/FFmpeg
"""

'''
TODO
・DONE: フォルダにあるFFmpegを呼び出せるか
・DONE: 再生リストの動画を全てダウンロードできるか
・DONE: 音声のみに対応できるか（フォーマットを変更するようにプログラムする）
・品質を変えられるか
・DONE: GUI対応する
・DONE: パッケージ化する https://flet.dev/docs/guides/python/packaging-desktop-app/
・DONE: 配布する
'''

from pathlib import Path #https://docs.python.org/ja/3/library/pathlib.html#correspondence-to-tools-in-the-os-module
import os
import subprocess #https://monologu.com/python/module/subprocess/
# import utils
from yt_dlp import YoutubeDL #https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#embedding-yt-dlp

def video_download(url, video_format, audio_format, audio_only, DIR_PATH):
    # debug用
    print(" ## url :", url)
    print(" ## video format :", video_format)
    print(" ## audio format :", audio_format)
    print(" ## is audio only :", audio_only)
    print(" ## DIR_PATH :", DIR_PATH)

    #環境変数の設定 https://zenn.dev/shiro_toy_box/articles/1a65c8a901e854
    FFMPEG_PATH = Path.cwd() / "ffmpeg" / "bin"  #ffmpegのパスを取得
    YTDLP_PATH = Path.cwd() / "yt-dlp"
    # print(f"########{FFMPEG_PATH}")
    os.environ['Path'] = str(FFMPEG_PATH) #os.environはstrしか受け付けない
    os.environ['Path'] = str(YTDLP_PATH) #os.environはstrしか受け付けない
    ## test用
    # subprocess.run('ffmpeg -version', shell=True)


    '''
    # reviewerから同一フォルダにアイテムが追加される方がよいとの指摘があったため，廃止．
    '''
    # # 逐一フォルダ作成 
    # DOWNLOAD_PATH = "Downloads"
    # dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # DIR_NAME = "output_" + dt_now
    # print(DOWNLOAD_PATH)
    # DIR_PATH = Path.home() / DOWNLOAD_PATH / DIR_NAME
    # try:
    #     Path(DIR_PATH).mkdir()
    # except FileExistsError as e: #既にファイルが存在する場合エラーを出力
    #     print(e)
    '''
    ここまで
    '''


    # youtubeダウンロード処理 https://github.com/yt-dlp/yt-dlp/tree/master?tab=readme-ov-file#video-format-options
    '''
    format options: https://github.com/yt-dlp/yt-dlp/tree/master?tab=readme-ov-file#post-processing-options
    (default) 3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm are supported
    '''
    ## test用
    # url = "https://www.youtube.com/watch?v=iMVChD17bIM&list=PLDJfzGjtVLHkgc_MbRNtFUeW_Fb1oAtqg"
    # video_format = "mp4" #--remux-video {video_format} #avi, flv, gif, mkv, mov, mp4, webm, aac, aiff, alac,flac, m4a, mka, mp3, ogg, opus, vorbis, wav are supported 
    # audio_format = "mp3" # aac, alac, flac, m4a, mp3, opus, vorbis, wav are supported

    ## settings
    output_dir = str(DIR_PATH) #-P option is used to specify the path each type of file should be saved to.
    audio_quality = "5" # 0 -10 (eg: 5=128k)
    playlist = "--yes-playlist" #--no-playlist
    playlist_index = "0:-1" # "-I 1:3,7,-5::2" used on a playlist of size 15 will download the items at index 1,2,3,7,11,13,15

    ## download cmd run
    cmd = ""
    if audio_only == False:
        if video_format == "mp4":
            # fast (default)
            video_cmd = f'yt-dlp -P {output_dir} -f {video_format} --audio-quality {audio_quality} {playlist} --playlist-items {playlist_index} -- "{url}"' 
            cmd = video_cmd
        else:
            # slow (when using ffmpeg)
            video_cmd = f'yt-dlp -P {output_dir} --ffmpeg-location {FFMPEG_PATH} --remux-video {video_format} --recode-video {video_format} --audio-quality {audio_quality} {playlist} --playlist-items {playlist_index} -- "{url}"' 
            cmd = video_cmd
    else:
        audio_cmd = f'yt-dlp -P {output_dir} --ffmpeg-location {FFMPEG_PATH} --extract-audio --audio-format {audio_format} --audio-quality {audio_quality} {playlist} --playlist-items {playlist_index}  -- "{url}"' 
        cmd = audio_cmd

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True) #Text=True: processをbyte -> stringで出力させる．#stderr=subprocess.STDOUT: 標準出力と同じ場所にエラーも表示
    
    return result.returncode, result.stdout, result.stderr # stdoutコマンド出力