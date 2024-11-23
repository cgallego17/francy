from django.db import models
import mimetypes

class MediaFile(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.media_type:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            if mime_type and mime_type.startswith('image'):
                self.media_type = 'image'
            elif mime_type and mime_type.startswith('video'):
                self.media_type = 'video'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type.capitalize()} - {self.file.name}"