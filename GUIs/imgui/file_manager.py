import dearpygui.dearpygui as dpg


with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag="video_running")
    dpg.add_string_value(default_value="", tag="video_filepath")
    dpg.add_int_value(default_value=0, tag='frame_counter')
    dpg.add_float_value(default_value=30, tag='fps')

def callback(sender, app_data):
    # print('OK was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    print(globals())
    dpg.set_value("video_filepath", app_data['file_path_name'])
    dpg.set_value("frame_counter", 0)
    dpg.set_value("video_running", True)

def cancel_callback(sender, app_data):
    # print('Cancel was clicked.')
    # print("Sender: ", sender)
    # print("App Data: ", app_data)
    pass


with dpg.file_dialog(height=360, directory_selector=False, show=False, callback=callback, tag="file_dialog",
    cancel_callback=cancel_callback):
    dpg.add_file_extension(".mp4", color=(255, 0, 255, 255), custom_text="[Video]")
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    #dpg.add_file_extension(".mp4", color=(255, 0, 255, 255), custom_text="[Video]")
