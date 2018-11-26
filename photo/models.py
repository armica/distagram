from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.

from tagging.fields import TagField
class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    text = models.TextField()
    tag = TagField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=False, null=False, default='images/no_image.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_duplicated = False
        if self.image:
            try:
                before_obj = Photo.objects.get(id=self.id)
                if before_obj.image == self.image:
                    is_duplicated = True
            except:
                pass
        if not is_duplicated:
            image_obj = Image.open(self.image).convert("L")
            new_image_io = BytesIO()
            image_obj.save(new_image_io, format='JPEG')

            temp_name = self.image.name
            self.image.delete(save=False)
            self.image.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)

            try:
                before_obj = Photo.objects.iget(id=self.id)
                if before_obj.image == self.image or is_duplicated:
                    self.image = before_obj.image
                else:
                    before_obj.image.delete(save=False)
            except:
                pass
            super(Photo,self).save(force_insert, force_update, using, update_fields)


    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=[self.id])

















