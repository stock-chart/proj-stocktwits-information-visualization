from __future__ import unicode_literals

from django.db import models
import datetime

class Message(models.Model):
    message_id = models.IntegerField()
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    user_id = models.IntegerField()
    symbol_id = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=10)

class User(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    classification = models.CharField(max_length=100, blank=True, default='')

class Symbol(models.Model):
    symbol_id = models.IntegerField()
    symbol = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    trending = models.CharField(max_length=100, blank=True, null=True)
    count = models.IntegerField(default=1)
    bull = models.IntegerField(default=0)
    bear = models.IntegerField(default=0)
