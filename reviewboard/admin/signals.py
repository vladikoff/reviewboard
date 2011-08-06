from datetime import date
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

"""
    These signals listen to database changes
    and clear the cache to keep the admin dashboard up to date.
"""

def deleteWidgetCache():
    cache.clear()

@receiver(post_save)
def my_handler(sender,**kwargs):
    deleteWidgetCache()

@receiver(post_delete)
def my_handler(sender,**kwargs):
    deleteWidgetCache()