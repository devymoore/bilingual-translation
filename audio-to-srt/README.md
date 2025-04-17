 # Audio to SRT Subtitles (Whisper + Translation)
 
 This is a Replicate-compatible model that transcribes audio files into SRT subtitle format, auto-detects Japanese segments, and translates them to English.
 
 ## Files
 
 - `predict.py`: Entry point defining the `predict(audio: str, model_size: str) -> str` function.
 - `requirements.txt`: Python dependencies.
 - `Dockerfile`: Container setup for running the model.
 
 ## Usage
 
 1. Install [Replicate CLI](https://replicate.com/docs/cli).
 2. Navigate to this directory:
    ```bash
    cd ~/Downloads/audio-to-srt
    ```
 3. Publish your model:
    ```bash
    replicate push
    ```
 4. Run predictions:
    ```bash
    replicate run USERNAME/model-name \
      -i audio="https://example.com/audio.mp3" \
      -i model_size="base"
    ```
 
 The output will be the SRT subtitle content.