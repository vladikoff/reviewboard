from datetime import date, timedelta
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('admin/subnav_item.html', takes_context=True)
def admin_subnav(context, url_name, name, image=""):
    """
    Returns a <li> containing a link to the desired setting tab.
    """
    request = context.get('request')
    url = reverse(url_name)

    return {
        'url': url,
        'name': name,
        'current': url == request.path,
        'image': image,
        'mediaUrl': settings.MEDIA_URL,
        'mediaSerial': settings.MEDIA_SERIAL,
     }

@register.inclusion_tag('admin/admin_widget.html', takes_context=True)
def admin_widget(context, widget_name, widget_title):
    """
    Returns a widget
    """

    widgets = {
           'user-activity': getUserActivityWidget
    }

    widget_data = widgets.get(widget_name, getUserActivityWidget)()

    return {
       'widget_title' : widget_title,
       'widget_name' : widget_name,
       'widget_size' : widget_data['size'],
       'widget_data': widget_data['data'],
       'widget_content': widget_data['template'],
       'widget_actions': widget_data['actions']
     }

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

    widget_actions = [['#','Add New'],['#','Manage Users','btn-right']]

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-user-activity.html"
    widget_data['data'] = activity_list
    widget_data['actions'] = widget_actions

    return widget_data