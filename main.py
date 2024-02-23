import flet as ft #https://flet.dev/docs/guides/python/getting-started
import download
import re
import time
import os # for progress bar


def main(page: ft.Page):
    container_margin = 15 # px
    page.window_width = 800+container_margin  # 幅
    page.window_height = 400  # 高さ
    page.window_resizable = True  # ウィンドウサイズ変更可否
    page.window_center()

    #　Download button 処理
    def download_button_clicked(e):
        start = time.time()

        print("CLICKED!!")
        # get url value
        if not video_url.value:
            pass
        else:
            download_btn.disabled = True #ボタンを無効化
            # get video and audio format
            if dropdown_audio.value == None: #default settings
                dropdown_video.value = "mp4"
                dropdown_audio.value = "mp3"

            # progress bar
            progress_bar_section.visible = True
            page.update() ### important! visible=Trueのように，状態を変更したら必ずpage.update()が必要

            # download run
            result_code, stdout, stderr = download.video_download(video_url.value, dropdown_video.value, dropdown_audio.value, check_box_audio.value) #stdout: 標準出力および簡単なエラー内容，stderr：エラー詳細
            end = time.time()  # 現在時刻（処理完了後）を取得
            total_time = round((end - start))
            total_time_sec = total_time % 60
            total_time_min = total_time // 60
            total_time_hour = total_time_min // 60

            if result_code == 0:
                # make message (using wild card: re module)
                download_location = re.findall('C:.*\s', stdout)[-1] #ダウンロード先を取得 https://note.nkmk.me/python-str-extract/#_7
                download_location = re.findall(r'\\.*\\', download_location)
                download_location = (''.join(download_location)) 

                message = f'Download location:  \n\n　　　{download_location}\n\n\nTime:  \n　　　{total_time_hour}h {total_time_min}min {total_time_sec}sec'
                open_dlg_modal(e, "SUCCESS!!(｀・ω・´)", message, "Blue500")
                page.add(dlg_modal)
            else:
                open_dlg_modal(e, "Error(´・ω・｀)", stdout, "RED500")
                page.add(dlg_modal)
                print(stderr) #debug用
            
            # setting を改める
            download_btn.disabled = False #ボタンを有効化
            video_url.value = "" #テキストエリアを空に
            progress_bar_section.visible = False # プログレスバーを非表示にする
            page.update()
    
    def info_link(e):
        pass
        # page.launch_url('https://github.com/apo-github')


    # controls
    '''
    ・url field
    ・download button
    ・check box
    ・icon
    '''
    video_url = ft.TextField(label="Video URL", width=600, border_radius=ft.border_radius.all(30), border_width=2)
    download_btn = ft.ElevatedButton(text="Download", icon=ft.icons.DOWNLOAD_ROUNDED, height=50, bgcolor=ft.colors.BLUE_400, color=ft.colors.WHITE, on_click=download_button_clicked)
    check_box_audio = ft.Checkbox(label="Audio only", value=False, fill_color=ft.colors.WHITE, check_color=ft.colors.BLUE_400) # default => false
    audio_icon = ft.Icon(name=ft.icons.AUDIOTRACK_ROUNDED, color=ft.colors.BLUE_400, size=20) # icon https://gallery.flet.dev/icons-browser/

    '''
    ・alert dialog
    '''
    def close_dlg(e): ## close dialog
            dlg_modal.open = False
            page.update()

    def open_dlg_modal(e, title, log, title_color):
        page.dialog = dlg_modal
        dlg_modal.title=ft.Text(title, weight=ft.FontWeight.W_600, color=title_color) #title
        dlg_modal.content=ft.Text(log, weight=ft.FontWeight.W_600) #message
        dlg_modal.open = True
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=False, #ダイアログの外側の領域をクリックしてダイアログを閉じれるようにする(False: able to close, True: unable to close)
        actions=[
            ft.TextButton("Close", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    '''
    progress bar
    #TODO Determinateなプログレスバーにしたい
    '''
    progress_bar_text = ft.Text("Downloading...", visible=True)
    progress_bar = ft.ProgressBar(width=400, color="Blue500", bgcolor="#eeeeee", visible=True)    

    '''
    ・drop down list
    '''
    dropdown_video = ft.Dropdown(width=150,
                                label="video format",
                                border_radius=ft.border_radius.all(30), border_width=0,
                                # hint_text="Choose video format",
                                options=[ #avi, flv, gif, mkv, mov, mp4, webm, aac, aiff, alac,flac, m4a, mka, mp3, ogg, opus, vorbis
                                    ft.dropdown.Option("mp4"),
                                    ft.dropdown.Option("avi"),
                                    ft.dropdown.Option("flv"),
                                    ft.dropdown.Option("gif"),
                                    ft.dropdown.Option("mov"),
                                    ft.dropdown.Option("webm"),
                                    ft.dropdown.Option("aac"),
                                    ft.dropdown.Option("aiff"),
                                    ft.dropdown.Option("alac"),
                                    ft.dropdown.Option("flac"),
                                    ft.dropdown.Option("m4a"),
                                    ft.dropdown.Option("mka"),
                                    ft.dropdown.Option("ogg"),
                                    ft.dropdown.Option("pous"),
                                    ft.dropdown.Option("vorbis"),
                                ])
    
    dropdown_audio = ft.Dropdown(width=150,
                                border_radius=ft.border_radius.all(30), border_width=0,
                                label="audio format",
                                # hint_text="Choose audio format",
                                options=[#aac, alac, flac, m4a, mp3, opus, vorbis, wav
                                    ft.dropdown.Option("mp3"),
                                    ft.dropdown.Option("wav"),
                                    ft.dropdown.Option("aac"),
                                    ft.dropdown.Option("alac"),
                                    ft.dropdown.Option("flac"),
                                    ft.dropdown.Option("m4a"),
                                    ft.dropdown.Option("opus"),
                                    ft.dropdown.Option("vorbis"),
                                ])
    '''
    footer
    '''
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.WHITE,
        content=ft.Row(
            controls=[
                ft.Text("© 2024 apo", size=10, weight=ft.FontWeight.W_600, color=ft.colors.GREY),
                ft.IconButton(icon=ft.icons.QUESTION_ANSWER, icon_color=ft.colors.BLUE_400, on_click=info_link),
            ],
            alignment=ft.MainAxisAlignment.END, # 右寄せ (Row=>MainAxisAlignment, Col=>CrossAxisAlignment)#https://flet.dev/docs/controls/column/
        ),
    )


    '''
    controls(contents) end
    '''
    

    # put some controls together
    textfiled_section = ft.Row(
        controls=[
            video_url,
            download_btn,
        ],
    )

    check_box_audio_section = ft.Row(
        controls=[
            check_box_audio,
            audio_icon,
        ]
    )

    dropdown_section = ft.Row(
        controls=[
            dropdown_video, dropdown_audio
        ],
    )

    progress_bar_section = ft.Column(
        controls=[
            progress_bar_text, progress_bar
        ],
    )
    
    # add controls to page
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    textfiled_section,
                    check_box_audio_section,
                    # dropdown_section,
                    progress_bar_section
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, #progress bar中央寄せ
            ),margin=container_margin,
        ),
    )
    progress_bar_section.visible = False #プログレスバーを非表示にする(default)
    page.update()

ft.app(target=main)