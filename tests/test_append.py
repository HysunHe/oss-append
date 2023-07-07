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
    original_file_path = '/var/tmp/ossappend/video9.mp4' 
    duplicate_file_path = '/tmp/video9.mp4_1688710496.mp4'

    create_duplicate_mp4_2(original_file_path, duplicate_file_path)
