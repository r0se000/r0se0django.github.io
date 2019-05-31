from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)      #짧은글
    pub_date=models.DateTimeField('date published')     #날짜
    body=models.TextField()     #긴글

    def __str__(self):
        return self.title       #제목 표시

    def summary(self):
        return self.body[:100]