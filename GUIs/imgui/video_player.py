import dearpygui.dearpygui as dpg
dpg.create_context()

import file_manager
import decord
import numpy as np
import time
import functools as ft

dpg.create_viewport(title='Video player', width=720, height=580, x_pos=0, y_pos=0)

with dpg.viewport_menu_bar():
    with dpg.menu(label="File"):
        dpg.add_menu_item(label="Open Video...", callback=lambda : dpg.show_item("file_dialog"))


@ft.cache
def get_frame(frame_counter):
    frame = vr[frame_counter].asnumpy()
    texture_data = frame/255
    return texture_data.ravel().astype('float32')
    

def _update_textures(frame_counter):
    return dpg.set_value('video_texture', get_frame(frame_counter))

def format_counter(fc):
    minutes, seconds = divmod(fc//30, 60)
    hours, minutes = divmod(minutes, 60)
    dpg.configure_item("slider", label=f"{hours}:{minutes:02}:{seconds:02}") 

raw_data = np.zeros(620*420*3)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(width=620, height=420, default_value=raw_data, format=dpg.mvFormat_Float_rgb, tag="video_texture")

def change_text(sender, app_data):
    print(dpg.get_item_configuration("progress_bar"))
    print(dpg.get_item_state("progress_bar"))
    print(dpg.get_item_state("text_videopath"))
    
    if dpg.is_item_hovered("progress_bar"):
        dpg.set_value("text item", f"Stop Hovering Me, Go away!!")
    else:
        dpg.set_value("text item", f"Hover Me!")

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=change_text)

# main window
with dpg.window(pos=(0,0), width=705, height=560, show=True):
    with dpg.group(horizontal=True):
        dpg.add_text("Video Filepath:", tag="text_videopath")
        dpg.add_text(source='video_filepath', show_label=True)
    
    dpg.add_image(texture_tag="video_texture")
    dpg.add_slider_int(label="n_frame", tag='slider', width=620, min_value=0, max_value=0, default_value=0, format='', source='frame_counter', show=False)
    dpg.add_progress_bar(label='n_frame', default_value=0.1, width=620, tag='progress_bar')

# only for fast testing
dpg.set_value("video_filepath", "C:\\Users\\stefano.giannini_ama\\Videos\\GUI_video-demo_coherent-interaction.mp4")
dpg.set_value("video_running", True)

dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.start_dearpygui()
while dpg.is_dearpygui_running():

    if dpg.get_value("video_running"):
        try:
            #print("ok")
            frame_counter = dpg.get_value('frame_counter')
            _update_textures(frame_counter)
            dpg.set_value('frame_counter', frame_counter+1)
            format_counter(frame_counter)
        except:
            vr = decord.VideoReader(dpg.get_value('video_filepath'), width=620, height=420)
            # print(vr.get_avg_fps())
            dpg.configure_item("slider", max_value=len(vr))

    time.sleep(1/(dpg.get_value('fps')*2))
    # if frame_counter%60 == 0: print(dpg.get_frame_rate())
    dpg.render_dearpygui_frame()


dpg.destroy_context()