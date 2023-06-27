from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=100)
    descripttion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
