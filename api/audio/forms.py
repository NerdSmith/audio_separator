from django import forms

from audio.models import AudioFile


class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audio',]