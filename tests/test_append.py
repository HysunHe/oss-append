from moviepy.editor import VideoFileClip, concatenate

def create_duplicate_mp4_2(file1, file2):
    clip1 = VideoFileClip(file1)
    clip2 = VideoFileClip(file2)
    duplicated_clip = concatenate([clip1, clip2])
    duplicated_clip.write_videofile('/tmp/dummy.mp4')
    
def create_duplicate_mp4(original_file, duplicate_file):
    with open(original_file, 'rb') as file:
        original_bytes = file.read()

    with open(duplicate_file, 'wb') as file:
        file.write(original_bytes)

    with open(original_file, 'rb') as file:
        original_bytes = file.read()

    with open(duplicate_file, 'ab') as file:
        file.write(original_bytes)

if __name__ == '__main__':
    file1 = '/var/tmp/ossappend/video9.mp4'
    file2 = '/var/tmp/ossappend/video11.mp4'

    clip1 = VideoFileClip(file1)
    clip2 = VideoFileClip(file2)
    duplicated_clip = concatenate([clip1, clip2])
    duplicated_clip.write_videofile('/tmp/dummy.mp4')
