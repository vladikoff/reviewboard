from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from reviewboard.admin import widgets


register = template.Library()


@register.inclusion_tag('admin/subnav_item.html', takes_context=True)
def admin_subnav(context, url_name, name, icon=""):
    """
    Returns a <li> containing a link to the desired setting tab.
    """
    request = context.get('request')
    url = reverse(url_name)

    return {
        'url': url,
        'name': name,
        'current': url == request.path,
        'icon': icon,
        'media_url': settings.MEDIA_URL,
        'media_serial': settings.MEDIA_SERIAL,
     }

@register.inclusion_tag('admin/admin_widget.html', takes_context=True)
def admin_widget(context, widget_name, widget_title, widget_icon=""):
    """
    Returns a widget
    """
    request = context.get('request')

    widget_list = {
        'review-requests': widgets.getReviewRequests,
        'user-activity': widgets.getUserActivityWidget,
        'request-statuses': widgets.getRequestStatuses,
        'repositories': widgets.getRepositories,
        'review-groups': widgets.getGroups,
        'server-cache': widgets.getServerCache,
        'news': widgets.getNews,
        'server-log': widgets.getServerLog
    }

    widget_data = widget_list.get(widget_name)(request)

    return {
       'widget_title': widget_title,
       'widget_name': widget_name,
       'widget_icon': widget_icon,
       'widget_size': widget_data['size'],
       'widget_data': widget_data['data'],
       'widget_content': widget_data['template'],
       'widget_actions': widget_data['actions'],
        'media_url': settings.MEDIA_URL,
        'media_serial': settings.MEDIA_SERIAL,
     }