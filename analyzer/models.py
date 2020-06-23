from django.db import models
from django.urls import reverse, reverse_lazy
import os


class Analysis(models.Model):
    store_title = models.CharField(max_length=200, help_text="Name of this analysis.",
                             unique=True)
    image = models.ImageField(upload_to='tinydoor-client-uploads',
                             help_text="Image being analyzed.")

    def __str__(self):
        '''Return the title of Analysis for presentation purposes.'''
        return f'{self.store_title} {self.id}'

    def get_absolute_url(self):
        '''Returns a fully qualified path for a page.'''
        path_components = {'pk': self.id}
        return reverse('', kwargs=path_components)

    def save(self, *args, **kwargs):
        '''Makes a URL safe slug automatically when a new instance is saved.'''
        # call save on the superclass
        return super(Analysis, self).save(*args, **kwargs)


