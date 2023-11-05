import cv2
import numpy as np
import os

# Control the strength of emboss and glow effects

print(
    "YOYOYOOO DIGGITY DAWG!!!!! ready to get your video Jamesified???? \n no problem boblem just need ya to answer some Qs!!!!: "
)
video = input("Enter the path to the input video file: ")
emboss_strength = float(input("Emboss strength??? (0-none 2-high): "))
glow_strength = float(input("glow strength??? (0-none 2-high): "))
output_fps = float(input("FPS!!?!?!: "))
beans1 = input("Audio Quality????? (<1-same quality, 1-lowest ): ")
audio_bitrate = f"{beans1}k"
audio_volume_factor = float(input("DB?????!!! (0-no audio 1-same 20-high): "))
beans2 = float(
    input("Video Quality??!!??? (0-same quality, 0<x<1-reeeallly low ,1-normal low): ")
)
print("okie doki now just wait UwU")
video_bitrate = f"{beans2}k"
codec = "vp9"
if beans2 > 0 and beans2 < 1:
    codec = "h264"
    beans2 = round(beans2 * 50)
    video_bitrate = f"{beans2}k"


def emboss_frame(frame, strength):
    kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    embossed_frame = cv2.filter2D(frame, -1, kernel)
    embossed_frame = cv2.addWeighted(frame, 1 - strength, embossed_frame, strength, 0)
    return embossed_frame


def apply_glow(frame, strength):
    if strength == 0.0:
        return frame  # No glow, return the original frame

    # Create a copy of the frame to apply the glow effect
    glow_frame = frame.copy()

    # Create a Gaussian blur to simulate the glow
    glow_frame = cv2.GaussianBlur(glow_frame, (0, 0), 10 * strength)

    # Add the glow frame to the original frame with some weight
    result_frame = cv2.addWeighted(frame, 1 + strength, glow_frame, -strength, 0)

    return result_frame


def emboss_and_apply_glow(input_file, output_file):
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))

    # Updated codec and format for video writing
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        embossed_frame = emboss_frame(frame, emboss_strength)
        glow_frame = apply_glow(embossed_frame, glow_strength)
        out.write(glow_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    input_video = video
    output_video = "effects_video(will auto delete after processing).mp4"
    emboss_and_apply_glow(input_video, output_video)


from moviepy.editor import VideoFileClip
import os

# OG video file
OG_video = video

# Input video file
input_video = "effects_video(will auto delete after processing).mp4"

# Output video file
output_video = "output_video.mp4"

# Desired frame rate for the output video

# Load the video clip
video_clip = VideoFileClip(input_video)

# Resize the video to 480p resolution
video_clip = video_clip.resize(height=480)

# Set the audio of the output video to be the same as the input video

output_clip = video_clip.set_audio(VideoFileClip(OG_video).audio)

output_clip = output_clip.volumex(audio_volume_factor)
output_clip.write_videofile(
    output_video,
    codec=codec,
    audio_bitrate=audio_bitrate,
    fps=output_fps,
    bitrate=video_bitrate,
)

# Close the video clip
video_clip.reader.close()
os.remove("effects_video(will auto delete after processing).mp4")
print("Video conversion complete.")
