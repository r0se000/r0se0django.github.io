from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200)      #짧은글
    pub_date=models.DateTimeField('date published')     #날짜
    body=models.TextField()     #긴글

    def __str__(self):
        return self.title       #제목 표시

    def summary(self):
        return self.body[:100]

class Comment(models.Model):
    post=models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")      #comments: 게시글이 가진 모든 댓글 가져옴, cascade: 글삭제시 댓글 모두 삭제
    user=models.ForeignKey(User, on_delete=models.CASCADE)       
    body=models.CharField(max_length=500)       #댓글 내용  