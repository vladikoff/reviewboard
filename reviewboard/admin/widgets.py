from array import array
import time, datetime

from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.utils.translation import ugettext as _
from djblets.util.misc import cache_memoize
from attachments.models import FileAttachment
from diffviewer.models import DiffSet

from reviewboard.admin.cache_stats import get_cache_stats
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.scmtools.models import Repository
from reviewboard.reviews.models import ReviewRequest, Group, \
    Comment, Review, Screenshot, ReviewRequestDraft


def getUserActivityWidget(request):
    """ User Activity Widget
    A pie chart of active application users based on their last login date
    """

    def activityData():
        now = datetime.date.today()
        users = User.objects

        activity_list = {
            'now': users.filter(last_login__range=\
            (now - datetime.timedelta(days=7), now + datetime.timedelta(days=1))).count(),
            'seven_days': users.filter(last_login__range=\
            (now - datetime.timedelta(days=30), now - datetime.timedelta(days=7))).count(),
            'thirty_days': users.filter(last_login__range=\
            (now - datetime.timedelta(days=60), now - datetime.timedelta(days=30))).count(),
            'sixty_days': users.filter(last_login__range=\
            (now - datetime.timedelta(days=90), now - datetime.timedelta(days=60))).count(),
            'ninety_days': users.filter(last_login__lte=\
            now - datetime.timedelta(days=90)).count(),
            'total': users.count()
        }

        return activity_list

    widget_actions = [
            ('db/auth/user/add/',_("Add New")),
            ('db/auth/user/',_("Manage Users"),'btn-right')
    ]

    key = "widget-activity-list-" + str(datetime.date.today())

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-user-activity.html',
        'data': cache_memoize(key, activityData),
        'actions': widget_actions
    }

    return widget_data


def getRequestStatuses(request):
    """ Request Statuses by Percentage Widget
    A pie chart showing review request by status """

    def statusData():
        request_objects = ReviewRequest.objects

        request_count = {
            'pending': request_objects.filter(status="P").count(),
            'draft': request_objects.filter(status="D").count(),
            'submit': request_objects.filter(status="S").count()
        }
        return request_count

    key = "widget-statuses-" + str(datetime.date.today())

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-request-statuses.html',
        'actions': '',
        'data': cache_memoize(key, statusData)
    }
    return widget_data


def getRepositories(request):

    def repoData():
        repositories = Repository.objects.accessible(request.user).order_by('-id')[:3]

        return repositories

    key = "widget-repo-list-" + str(datetime.date.today())

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-repositories.html',
        'actions': [
            ('db/scmtools/repository/add/',_("Add")),
            ('db/scmtools/repository/', _("View All"),'btn-right')
        ],
        'data': cache_memoize(key, repoData)
    }

    return widget_data


def getGroups(request):
    """ Review Group Listing
    Shows a list of recently created groups """
    def groupData():
        review_groups = Group.objects.all().order_by('-id')[:5]

        return review_groups

    key = "widget-groups-"+ str(datetime.date.today())

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-groups.html',
        'actions': [
            ('db/reviews/group/add/',_("Add")),
            ('db/reviews/group/',_("View All"))
        ],
        'data': cache_memoize(key, groupData)
    }
    return widget_data


def getServerCache(request):
    """ Cache Statistic Widget
    A list of memcached statistic if available to the application """
    cache_stats = get_cache_stats()
    uptime = {}

    for hosts, stats in cache_stats:
        if stats['uptime'] > 86400:
            uptime['value'] = stats['uptime'] / 60 / 60 / 24
            uptime['unit'] = _("days")
        elif stats['uptime'] > 3600:
            uptime['value'] = stats['uptime'] / 60 / 60
            uptime['unit'] = _("hours")
        else:
            uptime['value'] = stats['uptime'] / 60
            uptime['unit'] =  _("minutes")

    cache_data = {
        "cache_stats": cache_stats,
        "uptime": uptime
    }

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-server-cache.html',
        'actions': '',
        'data': cache_data
    }
    return widget_data


def getNews(request):
    """ News
    Latest Review Board news via RSS """

    widget_data = {
    'size': 'widget-small',
    'template': 'admin/widgets/w-news.html',
    'actions': [
            ('http://www.reviewboard.org/news/', _('More')),
            ('#', _('Reload'), 'reload-news')
    ],
        'data': ''
    }
    return widget_data


def getStats(request):
    """ Stats """
    def statsData():
        stats_data = {
            'count_comments': Comment.objects.all().count(),
            'count_reviews': Review.objects.all().count(),
            'count_attachments': FileAttachment.objects.all().count(),
            'count_reviewdrafts': ReviewRequestDraft.objects.all().count(),
            'count_screenshots': Screenshot.objects.all().count(),
            'count_diffsets': DiffSet.objects.all().count()
        }
        return stats_data

    key = "stats-day-" + str(datetime.date.today())

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-stats.html',
        'actions': '',
        'data': cache_memoize(key, statsData)
    }
    return widget_data


def getRecentActions(request):

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-recent-actions.html',
        'actions': '',
        'data': ''
    }

    return widget_data

def dynamicActivityData(request):
    direction = request.GET.get('direction')
    range_end = request.GET.get('range_end')
    range_start = request.GET.get('range_start')
    days_total = 30

    if range_end and range_start:
        range_end = datetime.datetime.strptime(request.GET.get('range_end'), "%Y-%m-%d")
        range_start = datetime.datetime.strptime(request.GET.get('range_start'), "%Y-%m-%d")

    if direction == "next":
        new_range_start = range_end
        new_range_end = new_range_start + datetime.timedelta(days=days_total)

    elif direction == "prev":
        new_range_start = range_start - datetime.timedelta(days=days_total)
        new_range_end = range_start
    elif direction == "same":
        new_range_start = range_start
        new_range_end = range_end
    else:
        # 30 days of activity
        new_range_end = datetime.date.today()
        new_range_start = new_range_end - datetime.timedelta(days=days_total)

    response_data = {
        "range_start": new_range_start.strftime("%Y-%m-%d"),
        "range_end": new_range_end.strftime("%Y-%m-%d")
    }

    def getObjects(modelName):
        objects = modelName.objects.all()
        print objects

    getObjects(Review)

    def largeStatsData(range_start, range_end):

        # Change Descriptions
        change_desc_unique = \
            ChangeDescription.objects.filter(timestamp__range=(range_start, range_end)).extra({'timestamp' : "date(timestamp)"})\
            .values('timestamp').annotate(created_count=Count('id')).order_by('timestamp')
        change_desc_array = []
        # need a test for this strptime for Python < 2.5 more at
        # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
        idx = 0
        for unique_desc  in change_desc_unique:
            change_desc_array.append([])
            change_desc_array[idx].append(time.mktime(time.strptime(unique_desc['timestamp'], "%Y-%m-%d")) * 1000)
            change_desc_array[idx].append(unique_desc['created_count'])
            idx += 1

        # Comments
        comments_unique = \
            Comment.objects.filter(timestamp__range=(range_start, range_end)).extra({'timestamp' : "date(timestamp)"})\
            .values('timestamp').annotate(created_count=Count('id')).order_by('timestamp')
        comment_array = []
        idx = 0
        # need a test for this strptime for Python < 2.5 more at
        # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
        for unique_comment  in comments_unique:
            comment_array.append([])
            comment_array[idx].append(time.mktime(time.strptime(unique_comment['timestamp'], "%Y-%m-%d")) * 1000)
            comment_array[idx].append(unique_comment['created_count'])
            idx += 1

        # Reviews
        reviews_unique = \
            Review.objects.filter(timestamp__range=(range_start, range_end)).extra({'timestamp' : "date(timestamp)"})\
            .values('timestamp').annotate(created_count=Count('id')).order_by('timestamp')
        review_array = []
        idx = 0
        # need a test for this strptime for Python < 2.5 more at
        # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
        for unique_review  in reviews_unique:
            review_array.append([])
            review_array[idx].append(time.mktime(time.strptime(unique_review['timestamp'], "%Y-%m-%d")) * 1000)
            review_array[idx].append(unique_review['created_count'])
            idx += 1

        # Review Requests
        rr_unique = \
            ReviewRequest.objects.filter(time_added__range=(range_start, range_end)).extra({'time_added' : "date(time_added)"})\
            .values('time_added').annotate(created_count=Count('id')).order_by('time_added')
        rr_array = []
        idx = 0
        for unique_rr  in rr_unique:
            rr_array.append([])
            rr_array[idx].append(time.mktime(time.strptime(unique_rr['time_added'], "%Y-%m-%d")) * 1000)
            rr_array[idx].append(unique_rr['created_count'])
            idx += 1


        # getting all widget_data together
        stat_data = {
            'change_descriptions': change_desc_array,
            'comments': comment_array,
            'reviews': review_array,
            'review_requests': rr_array
        }

        return stat_data

    activity_data = largeStatsData(new_range_start, new_range_end)

    activity_data = {
        "range":response_data,
        "activity_data": activity_data
    }

    return activity_data

def getLargeStats(request):
    """ Data Activity Large """

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-stats-large.html',
        'actions':  [
            ('#',_('<'),'','set-prev'),
            ('#',_('>'),'','set-next'),
            ('#',_('Reviews'),'btn-s btn-s-checked','set-reviews'),
            ('#',_('Comments'),'btn-s btn-s-checked','set-comments'),
            ('#',_('Review Requests'),'btn-s btn-s-checked','set-requests'),
            ('#',_('Descriptions'),'btn-s btn-s-checked','set-descriptions')
        ],
        'data': ["Loading..."]
    }
    return widget_data