from datetime import date, timedelta, datetime

from django.contrib.auth.models import User
from django.db.models import Min
from django.db.models.aggregates import Count
from django.utils.translation import ugettext as _

from djblets.log.views import iter_log_lines

from reviewboard.admin.cache_stats import get_cache_stats
from reviewboard.changedescs.models import ChangeDescription

from reviews.models import ReviewRequest, Group

from scmtools.models import Repository

from djblets.log.views import iter_log_lines


def getReviewRequests(request):
    # Review Requests Widget
    # Shows a date-based chart of review requests and change descriptions

    request_objects = ReviewRequest.objects
    review_requests = request_objects.all()
    
    # Request By Creation
    oldest_request = request_objects.aggregate(lowest=Min('time_added'))
    start_date = oldest_request['lowest']
    day_counter = 0
    day_total = (datetime.today() - start_date).days
    dates_in_days  = []
    req_array = []
    while day_counter < day_total:
        counter_date = start_date + timedelta(days=day_counter)
        dates_in_days.append(counter_date)

        req_array.append([])
        req_array[day_counter].append(request_objects.filter(time_added__lte=counter_date).count())
        req_array[day_counter].append(counter_date)
        day_counter += 1

    #Change Descriptions
    change_desc = ChangeDescription.objects
    change_desc_unique = change_desc.extra({'timestamp' : "date(timestamp)"}).values('timestamp').annotate(created_count=Count('id'))

    # need a test for this strptime for Python < 2.5 more at http://stackoverflow.com/questions/1286619/django-string-to-date-date-to-unix-timestamp
    for unique_desc  in change_desc_unique:
        unique_desc['timestamp'] = datetime.strptime(unique_desc['timestamp'], "%Y-%m-%d")

    # getting all widget_data together
    requests = {}
    requests['all_requests'] = review_requests
    requests['requests_by_day'] = req_array
    requests['change_descriptions'] = change_desc_unique

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-review-requests.html"
    widget_data['actions'] = [['#',_("View All"),'btn-right'],['#',_("View Drafts"),'btn-right']]
    widget_data['data'] = requests
    
    return widget_data

def getUserActivityWidget(request):
    # User Activity Widget
    # A pie chart of active application users based on their last login date

    now = date.today()
    users = User.objects

    activity_list = {}
    activity_list['now'] = \
        users.filter(last_login__range= \
        (now - timedelta(days=7), now + timedelta(days=1))).count()
    activity_list['seven_days'] = \
        users.filter(last_login__range= \
        (now - timedelta(days=30), now-timedelta(days=7))).count()
    activity_list['thirty_days'] =  \
        users.filter(last_login__range= \
        (now - timedelta(days=60), now-timedelta(days=30))).count()
    activity_list['sixty_days'] = \
        users.filter(last_login__range= \
        (now - timedelta(days=90), now-timedelta(days=60))).count()
    activity_list['ninety_days'] = \
        users.filter(last_login__lte= \
        now - timedelta(days=90)).count()
    activity_list['total'] = users.count()

    widget_actions = [['#',_("Add New")],['#',_("Manage Users"),'btn-right']]

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-user-activity.html"
    widget_data['data'] = activity_list
    widget_data['actions'] = widget_actions

    return widget_data

def getRequestStatuses(request):
    # Request Statuses by Percentage Widget
    # A pie chart showing review request by status

    request_objects = ReviewRequest.objects

    request_count = {}
    request_count['pending'] = request_objects.filter(status="P").count()
    request_count['draft'] = request_objects.filter(status="D").count()
    request_count['submit'] = request_objects.filter(status="S").count()

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-request-statuses.html"
    widget_data['actions'] = ""
    widget_data['data'] = request_count

    return widget_data

def getRepositories(request):
    repositories = Repository.objects.accessible(request.user)

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-repositories.html"
    widget_data['actions'] = [
            ['db/scmtools/repository/add/',_("Add New")],
            ['db/scmtools/repository/',_("View All"),'btn-right']
        ]
    widget_data['data'] = repositories
    
    return widget_data

def getGroups(request):
    # Review Group Listing
    # Shows a list of recently created groups

    review_groups = Group.objects.all()

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-groups.html"
    widget_data['actions'] = [
            ['db/reviews/group/add/',_("Add")],
            ['db/reviews/group/',_("View All")]
        ]
    widget_data['data'] = review_groups

    return widget_data

def getServerCache(request):
    # Cache Statistic Widget
    # A list of memcached statistic if available to the application
    
    cache_stats = get_cache_stats()

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-server-cache.html"
    widget_data['actions'] = ""
    widget_data['data'] = cache_stats

    return widget_data

def getNews(request):
    # News
    # Latest Review Board news via RSS
    
    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-news.html"
    widget_data['actions'] = [
            ['http://www.reviewboard.org/news/',_("More")],
            ['#',_("Reload"), 'reload-news']
        ]
    widget_data['data'] = ""

    return widget_data