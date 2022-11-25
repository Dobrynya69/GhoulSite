from django.db import models
from django.contrib.auth import get_user_model

class FriendList(models.Model):
    user_one = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="first_user")
    user_two = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="second_user")
    approved_one = models.BooleanField(default=False)
    approved_two = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_one.username} - {self.user_two.username}'
    