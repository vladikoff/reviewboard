from datetime import date, timedelta, datetime

from django.contrib.auth.models import User
from django.db.models import Min
from django.db.models.aggregates import Count
from django.utils.translation import ugettext as _
from attachments.models import FileAttachment
from diffviewer.models import DiffSet

from reviewboard.admin.cache_stats import get_cache_stats
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.scmtools.models import Repository
from reviewboard.reviews.models import ReviewRequest, Group, \
    Comment, Review, Screenshot, ReviewRequestDraft


def getReviewRequests(request):
    """ Review Requests Widget
    Shows a date-based chart of review requests and change descriptions """

    # TODO still need to clean this code below
    request_objects = ReviewRequest.objects
    review_requests = request_objects.all()
    requests = {}

    if review_requests:
        # Request By Creation
        oldest_req = request_objects.aggregate(lowest=Min('time_added'))
        start_date = oldest_req['lowest']
        day_total = (datetime.today() - start_date).days
        req_data = {}
        for i in range(day_total):
            counter_date = start_date + timedelta(days=i)
            req_data[i] = {}
            req_data[i]['req_count'] =\
                    request_objects.filter(time_added__lte=counter_date).count()
            req_data[i]['req_date'] = counter_date


        # getting all widget_data together
        requests = {
            'all_requests': review_requests,
            'requests_by_day': req_data
        }

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-review-requests.html',
        'actions': [
            ('admin/db/reviews/reviewrequest/', _("View All"), 'btn-right')
        ],
        'data': requests
    }

    return widget_data

def getUserActivityWidget(request):
    """ User Activity Widget
    A pie chart of active application users based on their last login date
    """
    now = date.today()
    users = User.objects

    activity_list = {
        'now': users.filter(last_login__range=\
        (now - timedelta(days=7), now + timedelta(days=1))).count(),
        'seven_days': users.filter(last_login__range=\
        (now - timedelta(days=30), now - timedelta(days=7))).count(),
        'thirty_days': users.filter(last_login__range=\
        (now - timedelta(days=60), now - timedelta(days=30))).count(),
        'sixty_days': users.filter(last_login__range=\
        (now - timedelta(days=90), now - timedelta(days=60))).count(),
        'ninety_days': users.filter(last_login__lte=\
        now - timedelta(days=90)).count(),
        'total': users.count()
    }
    widget_actions = [
            ('admin/db/auth/user/add/',_("Add New")),
            ('admin/db/auth/user/',_("Manage Users"),'btn-right')
    ]

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-user-activity.html',
        'data': activity_list,
        'actions': widget_actions
    }

    return widget_data

def getRequestStatuses(request):
    """ Request Statuses by Percentage Widget
    A pie chart showing review request by status """

    request_objects = ReviewRequest.objects

    request_count = {
        'pending': request_objects.filter(status="P").count(),
        'draft': request_objects.filter(status="D").count(),
        'submit': request_objects.filter(status="S").count()
    }

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-request-statuses.html',
        'actions': '',
        'data': request_count
    }
    return widget_data

def getRepositories(request):
    repositories = Repository.objects.accessible(request.user).order_by('-id')[:5]

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-repositories.html',
        'actions': [
            ('db/scmtools/repository/add/',_("Add New")),
            ('db/scmtools/repository/', _("View All"),'btn-right')
        ],
        'data': repositories
    }

    return widget_data

def getGroups(request):
    """ Review Group Listing
    Shows a list of recently created groups """

    review_groups = Group.objects.all().order_by('-id')[:5]

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-groups.html',
        'actions': [
            ('db/reviews/group/add/',_("Add")),
            ('db/reviews/group/',_("View All"))
        ],
        'data': review_groups
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
            ('http://www.reviewboard.org/news/',_('More')),
            ('#',_('Reload'), 'reload-news')
    ],
        'data': ''
    }
    return widget_data

def getStats(request):
    """ Stats """

    stats_data = {
        'count_comments': Comment.objects.all().count(),
        'count_reviews': Review.objects.all().count(),
        'count_attachments': FileAttachment.objects.all().count(),
        'count_reviewdrafts': ReviewRequestDraft.objects.all().count(),
        'count_screenshots': Screenshot.objects.all().count(),
        'count_diffsets': DiffSet.objects.all().count()
    }

    widget_data = {
        'size': 'widget-small',
        'template': 'admin/widgets/w-stats.html',
        'actions': '',
        'data': stats_data
    }
    return widget_data

def getLargeStats(request):
    """ Stats Large """

    #Change Descriptions
    change_desc = ChangeDescription.objects
    change_desc_unique = \
        change_desc.extra({'timestamp' : "date(timestamp)"})\
        .values('timestamp').annotate(created_count=Count('id'))

    # need a test for this strptime for Python < 2.5 more at
    # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
    for unique_desc  in change_desc_unique:
        unique_desc['timestamp'] = datetime.\
        strptime(unique_desc['timestamp'], "%Y-%m-%d")

    #Comments
    comments = Comment.objects
    comments_per_day = \
        comments.extra({'timestamp' : "date(timestamp)"})\
        .values('timestamp').annotate(created_count=Count('id'))

    # need a test for this strptime for Python < 2.5 more at
    # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
    for comment  in comments_per_day:
        comment['timestamp'] = datetime.\
        strptime(comment['timestamp'], "%Y-%m-%d")

    #Reviews
    reviews = Review.objects.all()
    reviews_per_day = \
        reviews.extra({'timestamp' : "date(timestamp)"})\
        .values('timestamp').annotate(created_count=Count('id')).order_by('timestamp')

     # need a test for this strptime for Python < 2.5 more at
    # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
    for review  in reviews_per_day:
        review['timestamp'] = datetime.\
        strptime(review['timestamp'], "%Y-%m-%d")
    #Review Requests

    rr_req_per_day = \
        ReviewRequest.objects.all().extra({'time_added' : "date(time_added)"})\
        .values('time_added').annotate(created_count=Count('id')).order_by('time_added')

         # need a test for this strptime for Python < 2.5 more at
    # TODO http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
    for rr_req  in rr_req_per_day:
        rr_req['time_added'] = datetime.\
        strptime(rr_req['time_added'], "%Y-%m-%d")

    # getting all widget_data together
    stat_data = {
        'change_descriptions': change_desc_unique,
        'comments': comments_per_day,
        'reviews': reviews_per_day,
        'review_requests': rr_req_per_day
    }

    widget_data = {
        'size': 'widget-large',
        'template': 'admin/widgets/w-stats-large.html',
        'actions':  [
            ('#',_('Reviews'),'btn-s btn-s-checked','set-reviews'),
            ('#',_('Comments'),'btn-s btn-s-checked','set-comments'),
            ('#',_('Review Requests'),'btn-s btn-s-checked','set-requests'),
            ('#',_('Descriptions'),'btn-s btn-s-checked','set-descriptions')
        ],
        'data': stat_data
    }
    return widget_data