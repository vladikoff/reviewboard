from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from djblets.siteconfig.models import SiteConfiguration
from django.contrib.auth.models import User
from admin.cache_stats import get_has_cache_stats
from reviews.models import ReviewRequest, ReviewRequestDraft, DefaultReviewer, Group
from reviewboard.admin import widgets
import reviewboard
from scmtools.models import Repository


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


@register.inclusion_tag('admin/widgets/w-actions.html', takes_context=True)
def admin_actions(context):
    #Site Configuration
    current_site_config = SiteConfiguration.objects.get_current()
    request = context.get('request')

    site_configs = {}
    site_configs['read_only'] = current_site_config.get('auth_anonymous_access')
    site_configs['syntax_highlighting'] = current_site_config.get('diffviewer_syntax_highlighting')
    site_configs['logging_enabled'] = current_site_config.get('logging_enabled')
    site_configs['logging_directory'] = current_site_config.get('logging_directory')
    site_configs['logging_allow_profiling'] = current_site_config.get('logging_allow_profiling')
    site_configs['mail_use_tls'] = current_site_config.get('mail_use_tls')
    site_configs['mail_send_review_mail'] = current_site_config.get('mail_send_review_mail')
    site_configs['search_enable'] = current_site_config.get('search_enable')

    print "Logging: " + str(site_configs['logging_enabled'])

    return {
        'request': request,
        'count_users': User.objects.count(),
        'count_review_groups': Group.objects.count(),
        'count_default_reviewers': DefaultReviewer.objects.count(),
        'count_repository': Repository.objects.accessible(request.user).count(),
        'has_cache_stats': get_has_cache_stats(),
        'site_configs': site_configs,
        'media_url': settings.MEDIA_URL,
        'media_serial': settings.MEDIA_SERIAL,
        'version': reviewboard.get_version_string()
    }