#!/usr/bin/env python3
"""
Predict entrypoint for Replicate: transcribes audio to SRT with auto language detection
and translation (Japanese to English).
"""
import os
import tempfile
try:
    import whisper
    from langdetect import detect, DetectorFactory
    from googletrans import Translator
    import requests
except ImportError as e:
    raise RuntimeError(
        f"Missing dependency {e.name}. Ensure requirements are installed." )

def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')

def transcribe_and_translate(input_path: str, model_size: str) -> str:
    DetectorFactory.seed = 0
    model = whisper.load_model(model_size)
    result = model.transcribe(input_path)
    segments = result.get("segments", [])
    translator = Translator()
    srt_lines = []
    for idx, seg in enumerate(segments, start=1):
        text = seg.get("text", "").strip()
        if not text:
            continue
        try:
            lang = detect(text)
        except Exception:
            lang = result.get("language", "en")
        if lang == 'ja':
            try:
                text_en = translator.translate(text, src='ja', dest='en').text
            except Exception:
                text_en = text
        else:
            text_en = text
        start_ts = format_timestamp(seg["start"])
        end_ts = format_timestamp(seg["end"])
        srt_lines.append(f"{idx}\n{start_ts} --> {end_ts}\n{text_en}\n")
    return "\n".join(srt_lines)

def predict(audio: str, model_size: str = 'base') -> str:
    # audio: URL or local path
    if audio.startswith(('http://', 'https://')):
        resp = requests.get(audio)
        resp.raise_for_status()
        suffix = os.path.splitext(audio)[1] or '.mp3'
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(resp.content)
        tmp.flush()
        input_path = tmp.name
    else:
        input_path = audio
    try:
        srt_content = transcribe_and_translate(input_path, model_size)
    finally:
        if audio.startswith(('http://', 'https://')) and os.path.exists(input_path):
            os.remove(input_path)
    return srt_content

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python predict.py <audio_file_or_url> [model_size]')
        sys.exit(1)
    audio = sys.argv[1]
    size = sys.argv[2] if len(sys.argv) > 2 else 'base'
    output = predict(audio, size)
    print(output)