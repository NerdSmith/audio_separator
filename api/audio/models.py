from django.db import models


class AudioFile(models.Model):
    audio = models.FileField("Аудио", upload_to='audio/')
    processed_audio = models.FileField(upload_to='processed_audio/', blank=True, null=True)

    def __str__(self):
        return self.audio.name
