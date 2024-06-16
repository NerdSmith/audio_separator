import librosa
import numpy as np
import tensorflow as tf

from utils.helper import wav_to_spectrogram_clips


class AudioSourceSeparator:
    def __init__(self):
        self.model = tf.keras.models.load_model("./conv_denoising_stacked_unet.h5")

    @staticmethod
    def play_separated_track(separated_audio, phase):
        separated_track = np.squeeze(separated_audio, axis=-1)
        spectrogram = np.concatenate(separated_track, axis=1)
        phase = phase[tuple(map(slice, spectrogram.shape))]
        reconstructed_track = librosa.istft(spectrogram * np.exp(1j * phase), hop_length=512, win_length=2048)
        return reconstructed_track

    def predict(self, audio):
        sound, sr = librosa.load(audio, sr=44100, mono=True)
        stft = librosa.stft(sound, n_fft=2048, hop_length=512, win_length=2048)
        phase = np.angle(stft)
        pred = self.model.predict(wav_to_spectrogram_clips(audio))
        return self.play_separated_track(pred[0], phase)
