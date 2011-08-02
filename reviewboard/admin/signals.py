from reviewboard.reviews.models import ReviewRequest, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Group)
def my_handler(sender, **kwargs):
    print "I'm alive!"


