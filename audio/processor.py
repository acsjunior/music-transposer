import subprocess
from pedalboard import Pedalboard, PitchShift
from pedalboard.io import AudioFile


def process_audio(input_path: str, output_path: str, semitones: int) -> None:
    with AudioFile(input_path) as f:
        audio = f.read(f.frames)
        sr = f.samplerate
    board = Pedalboard([PitchShift(semitones=semitones)])
    processed = board(audio, sr)
    with AudioFile(output_path, "w", sr, processed.shape[0]) as f:
        f.write(processed)


def convert_to_mp3(wav_path: str, mp3_path: str, bitrate: str = "320k") -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-b:a", bitrate, mp3_path],
        check=True,
        capture_output=True,
    )
