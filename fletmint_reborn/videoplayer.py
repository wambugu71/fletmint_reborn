import flet as ft
import  flet_video as  fv 


class VideoPlayer(ft.Container):
    def __init__(self, playlist: list[fv.VideoMedia], player_title: str):
        super().__init__()
        self.video_playlist = playlist
        self.player_title = player_title
        self.player_w  = fv.Video(
                expand=True,
                show_controls=False,
                playlist=self.video_playlist,
                playlist_mode=ft.PlaylistMode.LOOP,
                aspect_ratio=16 / 9,
                volume=100,
                autoplay=False,
                filter_quality=ft.FilterQuality.MEDIUM,
                muted=False,
                on_loaded=lambda e: print("Video loaded successfully!"),
                on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
                on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
            )
        self.video = ft.Container(
            content = self.player_w,
            border_radius=10,
            width=400,
            on_hover=self.on_video_hover,
            on_click=self.handle_play_or_pause,
        )

        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE_ROUNDED,
            icon_color="white",
            icon_size=16,
            on_click=self.handle_play_or_pause,
        )
        self.volume_slider = ft.Slider(
            thumb_color=ft.colors.with_opacity(0, "white"),
            overlay_color=ft.colors.with_opacity(0, "white"),
            secondary_track_value=ft.colors.with_opacity(0, "white"),
            active_color="#1f5eff",
            inactive_color="#323741",
            max=100,
            on_change=self.handle_volume_change,
        )
        self.fullscreen_button = ft.IconButton(
            icon=ft.icons.FULLSCREEN_ROUNDED,
            icon_color="white",
            on_click=lambda e: self.video.content.enter_fullscreen(),
        )
        self.upper_video_controls = ft.Container(
            visible=False,
            bgcolor="white, 0.0",
            content=ft.Row(
                [self.volume_slider, self.fullscreen_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            top=0,
        )
        self.video_duration = ft.Text("00:00", color=ft.colors.GREY_400)
        self.controls_video = ft.Container(
            visible=False,
            bgcolor="white, 0.0",
            content=ft.Row(
                [
                    ft.Row(
                        [
                            self.play_button,
                            ft.Text(value = self.player_title, color="white", size=14),
                        ]
                    ),
                    self.video_duration,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bottom=10,
            left=10,
            right=15,
        )
        
   
        self.content = ft.Stack([self.video, self.controls_video])
        #self.video_duration.value = self.player_w.get_current_position()
       # self.expand  =  True
    def did_mount(self):
        try:
            self.video_duration.value = self.player_w.get_current_position()
        except Exception as e:
            self.video_duration.value = "NaN:NaN"
        self.update()

    def on_video_hover(self, e):
        self.controls_video.visible ^= True
        self.upper_video_controls.visible ^= True
        self.update()

    def handle_play_or_pause(self, e):
        if  self.player_w.is_playing():
            self.play_button.icon  = ft.icons.PAUSE_CIRCLE_ROUNDED
        else:
            self.play_button.icon  = ft.icons.PLAY_CIRCLE_ROUNDED
        
        self.player_w.play_or_pause()
        print("Play or pause button clicked!")

    def handle_volume_change(self,e):
        self.player_w.volume = e.control.value
        page.update()
        
