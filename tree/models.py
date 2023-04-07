from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, unique=True)

    def clean(self):
        if self.parent is not None:
            if self.parent == self:
                raise ValidationError("Вы пытаетесь ссылаться на самого себя")
            if self.menu != self.parent.menu:
                raise ValidationError(
                    "Нельзя создавать " + self.__class__.__name__ + " если меню parent не схоже с вашим")
            current = self.parent
            while current is not None:
                if current == self:
                    raise ValidationError('Вы создали рекурсию через parent')
                current = current.parent

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tree:index_slug', args=[self.slug])
