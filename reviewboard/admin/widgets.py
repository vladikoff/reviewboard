from datetime import date, timedelta
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

def getUserActivityWidget():
    # User Activity Widget
    now = date.today()
    users = User.objects

    activity_list = {}
    activity_list['now'] = \
        users.filter(last_login__range=(now - timedelta(days=7), now + timedelta(days=1))).count()
    activity_list['seven_days'] = \
        users.filter(last_login__range=(now - timedelta(days=30), now-timedelta(days=7))).count()
    activity_list['thirty_days'] =  \
        users.filter(last_login__range=(now - timedelta(days=60), now-timedelta(days=30))).count()
    activity_list['sixty_days'] = \
        users.filter(last_login__range=(now - timedelta(days=90), now-timedelta(days=60))).count()
    activity_list['ninety_days'] = \
        users.filter(last_login__lte= now - timedelta(days=90)).count()
    activity_list['total'] = users.count()

    widget_actions = [['#',_("Add New")],['#',_("Manage Users"),'btn-right']]

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-user-activity.html"
    widget_data['data'] = activity_list
    widget_data['actions'] = widget_actions

    return widget_data