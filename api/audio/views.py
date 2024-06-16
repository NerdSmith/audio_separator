from io import BytesIO

import soundfile
from django.core.files import File
from django.shortcuts import render, redirect

from audio.forms import AudioFileForm
from audio.models import AudioFile

from audio.services import AudioSourceSeparator


def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            pred_audio = AudioSourceSeparator().predict(audio_file.audio.path)
            # Здесь будет логика для создания processed_audio
            # Например, вызов внешнего сервиса и сохранение результата в audio_file.processed_audio
            # audio_file.processed_audio = результат вызова сервиса
            # audio_file.save()
            name = audio_file.audio.name.split('/')[1].split('.')[0]
            b = BytesIO()
            soundfile.write(b, pred_audio, 44100, subtype='PCM_24', format="WAV")
            audio_file.processed_audio = File(b, name + "-pred.wav")
            audio_file.save(update_fields=["processed_audio"])
            return redirect('audio_list')
    else:
        form = AudioFileForm()
    return render(request, 'audio/upload_audio.html', {'form': form})

def audio_list(request):
    audios = AudioFile.objects.all()
    return render(request, 'audio/audio_list.html', {'audios': audios})