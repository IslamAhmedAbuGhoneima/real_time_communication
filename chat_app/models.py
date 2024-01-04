from django.db import models
from account.models import User
# Create your models here.


class Message(models.Model):
    body = models.TextField()
    send_by = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='user_messages', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.send_by}'


class Room(models.Model):
    CHOICES_STATUS = [
        ('WAITING', 'Wating'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]
    uuid = models.CharField(max_length=250)
    client = models.CharField(max_length=250)
    agent = models.ForeignKey(
        User, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.URLField()
    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, db_default=CHOICES_STATUS[0][0])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.client} - {self.uuid}'
