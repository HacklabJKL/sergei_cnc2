import obspython as obs
import time
import subprocess
import os.path

source_name = ""
interval    = 500
prev_scene = ""

def set_scene(scene_name):
    global prev_scene
    
    if scene_name != prev_scene:
        prev_scene = scene_name
        scenes = obs.obs_frontend_get_scenes()
        for scene in scenes:
            name = obs.obs_source_get_name(scene)
            if name == scene_name:
                obs.obs_frontend_set_current_scene(scene)

def update_text():
    global interval
    global source_name

    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        settings = obs.obs_data_create()
        
        try:
            text = subprocess.check_output(["/usr/bin/python2", "%s/get_linuxcnc_status.py" % os.path.dirname(__file__)])
        except subprocess.CalledProcessError:
            text = b''
        
        obs.obs_data_set_string(settings, "text", text.decode('utf-8'))
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
        
        if b'RUNNING' in text:
            set_scene('Running')
        elif text:
            set_scene('Setup')
        else:
            set_scene('Stopped')

def script_description():
    return "LinuxCNC status"
    
def script_update(settings):
    global interval
    global source_name

    interval    = obs.obs_data_get_int(settings, "interval")
    source_name = obs.obs_data_get_string(settings, "source")

    obs.timer_remove(update_text)

    if source_name != "":
        obs.timer_add(update_text, interval)

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "interval", 1000)
    obs.obs_data_set_default_string(settings, "source", "LinuxCNC status")

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_int(props, "interval", "Update Interval (ms)", 5, 10000, 1)

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    return props

