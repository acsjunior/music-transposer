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
