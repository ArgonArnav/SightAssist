from TTS.api import TTS

class SpeechSynthesizer:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        """
        Initialize the TTS model. The default model is an English Tacotron2-DDC.
        This will download the model on first use if not already present.
        """
        self.tts = TTS(model_name)
    
    def text_to_speech(self, text, output_path="output.wav"):
        """
        Synthesize speech from text and save to output_path (WAV file).
        Returns the output file path.
        """
        if not text or text.strip() == "":
            return None
        # Use Coqui TTS to generate the speech audio
        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path

# Example usage:
# tts = SpeechSynthesizer()
# tts.text_to_speech("Hello, world!", "hello.wav")
