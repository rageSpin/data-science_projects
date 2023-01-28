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
    minutes, seconds = divmod(fc//60, 60)
    hours, minutes = divmod(minutes, 60)
    # dpg.configure_item("slider", label=f"{hours}:{minutes:02}:{seconds:02}") 
    dpg.set_value('video_time', f"{hours}:{minutes:02}:{seconds:02}")

def reset_state():
    global vr
    dpg.set_value('video_running', False)
    format_counter(0)
    del vr
    dpg.set_value("video_texture", np.zeros(620*420*3))
    dpg.set_value("frame_progress", 0)

raw_data = np.zeros(620*420*3)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(width=620, height=420, default_value=raw_data, format=dpg.mvFormat_Float_rgb, tag="video_texture")

def change_text(sender, app_data):
    if dpg.get_value('video_running'):
        it_conf = dpg.get_item_configuration("progress_bar")
        pos = dpg.get_item_state("progress_bar")['pos']
        # print(it_conf['width'], it_conf['height'])
        # print(pos)
        # print(dpg.get_mouse_pos(local=False))
        # print(dpg.get_mouse_pos(local=True))
        # print(dpg.get_item_state("video_texture"))
        mouse_pos = dpg.get_mouse_pos(local=False)
        min_y = pos[1] + 20
        max_y = pos[1] + it_conf['height'] + 20
        min_x = pos[0]
        max_x = pos[0] + it_conf['width']
        if mouse_pos[1] >= min_y and mouse_pos[1] <= max_y:
            if mouse_pos[0] >= min_x and mouse_pos[0] <= max_x:
                print("inside progress bar")
                norm_prog = (mouse_pos[0]-min_x)/(max_x-min_x)
                #dpg.configure_item('progress_bar', default_value=norm_prog)
                dpg.set_value('frame_progress', norm_prog)
                #dpg.set_value("frame_counter", int(dpg.get_item_configuration('slider')['max_value']*norm_prog))

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=change_text)


# main window
with dpg.window(pos=(0,0), width=705, height=560, show=True):
    with dpg.group(horizontal=True):
        dpg.add_text("Video Filepath:", tag="text_videopath")
        dpg.add_text(source='video_filepath', show_label=True)
    
    dpg.add_image(texture_tag="video_texture")
    # dpg.add_slider_float(label="n_frame", tag='slider', width=620, min_value=0, max_value=1, default_value=0, format='', source='frame_progress')#, show=False)
    with dpg.group(horizontal=True):
        dpg.add_progress_bar(label='n_frame', default_value=0, width=620, height=5, tag='progress_bar', source='frame_progress')
        dpg.add_text("", tag='video_time', wrap=0)

# only for fast testing
dpg.set_value("video_filepath", "C:\\Users\\stefano.giannini_ama\\Videos\\GUI_video-demo_coherent-interaction.mp4")
dpg.set_value("video_running", True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_style_editor()
# dpg.start_dearpygui()
while dpg.is_dearpygui_running():

    if dpg.get_value("video_running"):
        try:
            frame_counter = int(dpg.get_value('frame_progress')*video_len)
            #print(frame_counter)
            _update_textures(frame_counter)
            dpg.set_value('frame_progress', dpg.get_value('frame_progress')+step)
            format_counter(frame_counter)
            # if frame_counter%60 == 0: print(dpg.get_frame_rate())
            if (frame_counter+1) == video_len: reset_state()

        except Exception as e:
            vr = decord.VideoReader(dpg.get_value('video_filepath'), width=620, height=420)
            step = 1/len(vr)
            video_len = len(vr)
            # print(video_len, step)
            print(e)
            print("FPS", vr.get_avg_fps())
            #dpg.configure_item("slider", max_value=len(vr))

    # time.sleep(1/(dpg.get_value('fps')*2))
    dpg.render_dearpygui_frame()


dpg.destroy_context()