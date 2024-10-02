from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    survey_level = models.IntegerField(default=0)
    nickname = models.CharField(max_length=12, unique=True)
    ranking = models.IntegerField()

    def __str__(self):
        return self.nickname

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.SmallIntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.post.title}"

class Quest(models.Model):
    difficulty = models.SmallIntegerField()
    content = models.TextField()
    score = models.IntegerField()
    is_cleared = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Quest for {self.user.nickname}: {self.content[:20]}..."

class DailyCheck(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['date', 'user']

    def __str__(self):
        return f"Check for {self.user.nickname} on {self.date}"

class QuestList(models.Model):
    content = models.CharField(max_length=50)
    score = models.IntegerField()
    isolation_level = models.SmallIntegerField()
    difficulty = models.SmallIntegerField()

    def __str__(self):
        return f"Quest: {self.content[:20]}... (Level: {self.isolation_level}, Difficulty: {self.difficulty})"
