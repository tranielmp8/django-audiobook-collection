from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AudioBook(models.Model):
  title = models.CharField(max_length=75)
  author = models.CharField(max_length=150)
  description = models.TextField()
  book_image = models.ImageField(default="books/audio-book.png", null=True, blank=True, upload_to="books/")
  is_favorite = models.BooleanField(default=False, verbose_name="Favorite")
  listen_date = models.DateField(null=True, blank=True)
  date_posted = models.DateTimeField(auto_now_add=True)
  
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  
  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ['-date_posted']