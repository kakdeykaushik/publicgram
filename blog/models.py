from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings
from nudenet import NudeClassifier


NSFW_THRESHOLD = settings.NSFW_THRESHOLD

# Utility function to check is NSFW content
def check_nsfw(path):
	classifier = NudeClassifier()
	res = classifier.classify(path)
	try:
		return round(res.get(path).get("unsafe"), 3)
	except Exception as e:
		return 0

class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	is_visible = models.BooleanField(default=True)

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		path = self.file.path
		unsafe = check_nsfw(path)
		if unsafe > NSFW_THRESHOLD:
			self.is_visible = False
		super().save(*args, **kwargs)
