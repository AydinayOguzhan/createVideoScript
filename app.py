import os
import random
import pyttsx3
import pysrt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import moviepy.editor as mp
from moviepy.video.fx.all import speedx

# Manually input the exciting story from Reddit
story = """Regretting opening up our marriage.

A couple of months ago, my wife (35F) and I (34M) decided to open our marriage. At the time, it seemed like a good idea. We thought it would bring some excitement and new experiences into our relationship.

However, things haven't turned out the way I hoped. My wife has been quite promiscuous, meeting several new partners and frequently going out on dates. At first, I tried to set boundaries, like asking her to be transparent about her encounters and to avoid bringing anyone to our home. But despite these boundaries, I can't stand the thought of her with someone else.

Each time she goes out, I feel a knot in my stomach. When she comes back, the look of excitement and satisfaction on her face just crushes me. I’ve tried to be supportive and remind myself that this was a mutual decision, but it’s tearing me apart. I find myself constantly thinking about her with other people, and it’s driving me crazy.

One particular incident was especially hard to handle. She went on a weekend trip with someone she met online. She was so excited about it, and I could see how much she was looking forward to it. The entire weekend, I was a wreck. I couldn’t focus on anything and just kept imagining the worst scenarios. When she came back, she was glowing, talking about how great the trip was. It was a knife to my heart.

I’ve come to realize that I can’t handle this open relationship. It’s not bringing us closer; it’s only pushing me further into a dark place. I regret agreeing to it in the first place, and now I don’t know how to talk to her about wanting to close the marriage again. I’m scared she might not feel the same way or that it might create even more tension between us."""

def get_random_background_video(folder='./background-videos'):
    videos = [f for f in os.listdir(folder) if f.endswith('.mp4')]
    if not videos:
        raise FileNotFoundError(f"No mp4 files found in the folder '{folder}'.")
    return os.path.join(folder, random.choice(videos))

def generate_voiceover(text, output_file='voiceover.mp3'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 0.9)  # Volume

    # Set male voice
    voices = engine.getProperty('voices')
    for voice in voices:
        # Microsoft Zira Desktop - woman voice
        # Microsoft David Desktop - man voice
        if 'Microsoft David Desktop' in voice.name:
            engine.setProperty('voice', voice.id)
            break

    engine.save_to_file(text, output_file)
    engine.runAndWait()

def split_text_into_chunks(text, min_words_per_chunk=2, max_words_per_chunk=4):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def seconds_to_srttime(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=millis)

def create_subtitles(chunks, voiceover_durations, output_file='subtitles.srt'):
    subs = pysrt.SubRipFile()
    start_time = 0
    for i, (chunk, duration) in enumerate(zip(chunks, voiceover_durations)):
        end_time = start_time + duration
        sub = pysrt.SubRipItem(i + 1, start=seconds_to_srttime(start_time), end=seconds_to_srttime(end_time), text=chunk)
        subs.append(sub)
        start_time = end_time
    subs.save(output_file, encoding='utf-8')

def get_voiceover_durations(chunks):
    durations = []
    for i, chunk in enumerate(chunks):
        chunk_file = f'temp_chunk_{i}.mp3'
        generate_voiceover(chunk, chunk_file)
        with mp.AudioFileClip(chunk_file) as audio:
            durations.append(audio.duration)
        os.remove(chunk_file)  # Clean up temporary files
    return durations

def create_subtitle_images(subtitles, video_size, font_path="./arial_narrow_7.ttf", font_size=40):
    subs = pysrt.open(subtitles)
    subtitle_clips = []
    for sub in subs:
        img = Image.new('RGBA', video_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, font_size)
        text = sub.text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (video_size[0] - text_width) // 2
        y = (video_size[1] - text_height) // 2  # Center vertically
        draw.text((x, y), text, font=font, fill='white')
        subtitle_image = np.array(img)
        subtitle_clip = (sub.start.ordinal / 1000, sub.end.ordinal / 1000, subtitle_image)
        subtitle_clips.append(subtitle_clip)
    return subtitle_clips

def add_subtitles_to_video(video, subtitle_images):
    clips = [video]
    for start_time, end_time, image in subtitle_images:
        img_clip = mp.ImageClip(image, duration=end_time - start_time).set_start(start_time).set_position(('center', 'center'))  # Centered vertically
        clips.append(img_clip)
    return mp.CompositeVideoClip(clips)

def create_video(background_video, voiceover, subtitles, output_file='output_video.mp4'):
    video = mp.VideoFileClip(background_video).resize(height=1280).crop(x1=0, y1=0, width=720, height=1280)
    audio = mp.AudioFileClip(voiceover)
    final_video_duration = audio.duration
    if video.duration < final_video_duration:
        video = mp.concatenate_videoclips([video] * int(final_video_duration // video.duration + 1))
    video = video.subclip(0, final_video_duration)
    final_video = video.set_audio(audio)
    # subtitle_images = create_subtitle_images(subtitles, video.size)
    # final_video = add_subtitles_to_video(final_video, subtitle_images)
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')

def main():
    print("Using manually inputted story:", story)
    chunks = split_text_into_chunks(story, min_words_per_chunk=2, max_words_per_chunk=4)
    print("Text chunks:", chunks)
    
    voiceover_durations = get_voiceover_durations(chunks)
    total_duration = sum(voiceover_durations)
    print(f"Total voiceover duration: {total_duration:.2f} seconds")

    background_video = get_random_background_video()
    print("Selected Background Video:", background_video)

    generate_voiceover(story, 'voiceover.mp3')
    print("Generated Voiceover")
    
    # create_subtitles(chunks, voiceover_durations, 'subtitles.srt')
    # print("Created Subtitles")
    
    create_video(background_video, 'voiceover.mp3', 'subtitles.srt')
    print("Created Video")

if __name__ == "__main__":
    main()
