import asyncio
import os
import uuid
from config import TEMP_DIR
from utils import cleanup_temp_files

async def run_ffmpeg(args):
    process = await asyncio.create_subprocess_exec(
        'ffmpeg', *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return process.returncode == 0

async def convert_video_to_audio(input_path, fmt="mp3"):
    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.{fmt}")
    args = ['-i', input_path, '-vn', '-c:a', 'libmp3lame' if fmt == 'mp3' else 'aac', '-q:a', '2', output_path]
    success = await run_ffmpeg(args)
    return output_path if success else None

async def create_gif(input_path, duration=5, quality="Medium"):
    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.gif")
    scale = "scale=320:-1" if quality == "Low" else "scale=480:-1" if quality == "Medium" else "scale=720:-1"
    args = ['-t', str(duration), '-i', input_path, '-vf', f"fps=10,{scale}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", '-loop', '0', output_path]
    success = await run_ffmpeg(args)
    return output_path if success else None

async def cut_video(input_path, start_time, end_time):
    output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_cut.mp4")
    args = ['-i', input_path, '-ss', start_time, '-to', end_time, '-c', 'copy', output_path]
    success = await run_ffmpeg(args)
    return output_path if success else None
