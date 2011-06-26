from datetime import date, timedelta, datetime
from django.contrib.auth.models import User
from reviewboard.admin.cache_stats import get_cache_stats
from django.utils.translation import ugettext as _
from reviews.models import ReviewRequest, Group
from scmtools.models import Repository
from django.db.models import Avg, Max, Min, Count

    # Review Requests Widget
def getReviewRequests(request):
    request_objects = ReviewRequest.objects
    review_requests = request_objects.all()
    
    # Request By Creation
    oldest_request = request_objects.aggregate(lowest=Min('time_added'))
    start_date = oldest_request['lowest']
    daysS = 0
    daysSoFar = (datetime.today() - start_date).days
    datesInDays  = []
    req_array = []
    while daysS < daysSoFar:
        counterDate = start_date + timedelta(days=daysS)
        datesInDays.append(counterDate)

        req_array.append([])
        req_array[daysS].append(request_objects.filter(time_added__lte=counterDate).count())
        req_array[daysS].append(counterDate)
        daysS = daysS + 1

    requests = {}
    requests['all_requests'] = review_requests
    requests['requests_by_day'] = req_array

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-review-requests.html"
    widget_data['actions'] = [['#',_("View All"),'btn-right'],['#',_("View Drafts"),'btn-right']]
    widget_data['data'] = requests
    
    return widget_data

    # User Activity Widget
def getUserActivityWidget(request):
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

    # Request Statuses by Percentage Widget
def getRequestStatuses(request):
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

    # Repository Table View
def getRepositories(request):
    repositories = Repository.objects.accessible(request.user)

    widget_data = {}
    widget_data['size'] = "widget-large"
    widget_data['template'] = "admin/widgets/w-repositories.html"
    widget_data['actions'] = [['db/scmtools/repository/add/',_("Add New")],['db/scmtools/repository/',_("View All"),'btn-right']]
    widget_data['data'] = repositories
    
    return widget_data

    #Review Group Listing
def getGroups(request):
    review_groups = Group.objects.all()

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-groups.html"
    widget_data['actions'] = [['db/reviews/group/add/',_("Add New")],['db/reviews/group/',_("View All")]]
    widget_data['data'] = review_groups

    return widget_data

    # Cache Statistic Widget
def getServerCache(request):
    cache_stats = get_cache_stats()

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-server-cache.html"
    widget_data['actions'] = ""
    widget_data['data'] = cache_stats

    return widget_data

    # News
def getNews(request):

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-news.html"
    widget_data['actions'] = [['http://www.reviewboard.org/news/',_("More News")],['#',_("Reload"), 'reload-news']]
    widget_data['data'] = ""

    return widget_data

    #Server Log
def getServerLog(request):

    widget_data = {}
    widget_data['size'] = "widget-small"
    widget_data['template'] = "admin/widgets/w-server-log.html"
    widget_data['data'] = ""
    widget_data['actions'] = [['#',_("View Log")]]

    return widget_data