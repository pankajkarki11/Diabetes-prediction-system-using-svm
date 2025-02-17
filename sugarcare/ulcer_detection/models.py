from django.db import models

# Create your models here.
class UlcerImage(models.Model):
    image = models.ImageField(upload_to='ulcer_images/')
    result = models.CharField(max_length=100, blank=True, null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.result}"