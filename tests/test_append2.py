import time
import os
from moviepy.editor import VideoFileClip, concatenate


def file_to_bytes(path_file):
    with open(path_file,'rb') as f:
        image_bytes = f.read()
        return image_bytes
    
def handle_content_video(file_name, content_bytes):
    """ docstring """
    file_fullname = f'/tmp/aaa/{file_name}'

    tmp_clip_file = f'/tmp/{file_name}_{int(time.time())}.mp4'
    with open(tmp_clip_file, 'wb') as clip_file:
        clip_file.write(content_bytes)
    this_clip = VideoFileClip(tmp_clip_file)

    if os.path.exists(file_fullname):
        try:
            exist_clips = VideoFileClip(file_fullname)
            new_clips = concatenate([exist_clips, this_clip])
        except IOError as err:
            print(str(err))
            new_clips = this_clip
    else:
        new_clips = this_clip

    # oss_utils.delete_file(file_fullname)
    os.remove(file_fullname)
    new_clips.write_videofile(file_fullname)
    

content_bytes = file_to_bytes('/home/hysunhe/projects/aijianvideo/video1.mp4')
file_name = 'test1.mp4'

handle_content_video(file_name, content_bytes)