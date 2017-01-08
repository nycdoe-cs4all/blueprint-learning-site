from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Activity, Grade, Subject, Device
from .forms import ActivityForm


# Create your views here.
def index(request):
    _devices = Activity.objects.all().raw("SELECT id, body->'devices' AS device FROM activities_activity")
    all_devices = []
    for device in _devices:
        all_devices += device.device
    all_devices = sorted(list(set(all_devices)))

    grades = Grade.objects.all()
    subjects = Subject.objects.all()

    q = request.GET.get('q', '')
    grade = request.GET.get('grade')
    subject = request.GET.get('subject')
    level = request.GET.get('level')
    devices = request.GET.getlist('devices')
    page = request.GET.get('page')

    if request.user.is_superuser:
        approved = str((request.GET.get('approved', 0)))
    else:
        approved = str(request.GET.get('approved', 1))

    filters = {'q': q, 'grade': grade, 'subject': subject, 'level': level, 'devices': devices, 'approved': approved}

    activities_list = Activity.objects.order_by('-date_added')

    if grade:
        activities_list = activities_list.filter(body__grade=grade)

    if approved:
        activities_list = activities_list.filter(approved=approved)

    if subject:
        activities_list = activities_list.filter(body__subject=subject)

    if devices:
        activities_list = activities_list.filter(body__devices__contains=devices)

    if request.GET.get('q'):
        vector = SearchVector('plain_body', 'title')
        query = SearchQuery(q)
        #activities_list = activities_list.filter(plain_body__search=q)
        activities_list = activities_list.annotate(rank=SearchRank(vector, query)).order_by('-rank')

    paginator = Paginator(activities_list, 20)

    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        activities = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        activities = paginator.page(paginator.num_pages)
    context = {'activities': activities, 'grades': grades, 'subjects': subjects, 'filters': filters, 'all_devices': all_devices}
    return render(request, 'activities/index.html', context)


def create(request):
    title = request.POST.get('title')
    subject = request.POST.get('subject')
    grade = request.POST.get('grade')
    devices = request.POST.get('devices')
    body = request.POST.get('html_body')
    plain_body = request.POST.get('plain_body')

    response = {}
    form = ActivityForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.user = request.user
        activity.google_file_id = request.POST.get('url')
        activity.body = {
            'title': title,
            'subject': activity.subject.name,
            'grade': activity.grade.name,
            'html': body,
            'plain': plain_body,
            'devices': [d.strip() for d in devices.split('\n')]
        }
        activity.save()
        response['status'] = 'ok'
    else:
        error_message = dict([(key, [error for error in value]) for key, value in form.errors.items()])
        response['status'] = 'failed'
        response['errors'] = error_message
    return JsonResponse(response)


def parse(request):
    from .get_activity import Activity
    activity = Activity(request.GET.get('url'))
    return JsonResponse(activity.to_dict())


def new(request):
    grades = Grade.objects.all()
    devices = Device.objects.all()
    subjects = Subject.objects.all()
    context = {'grades': grades, 'devices': devices, 'subjects': subjects}

    return render(request, 'activities/new.html', context)


def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'activities/detail.html', {'activity': activity})


def change_status(request):
    if request.user.is_superuser:
        post_id = request.POST.get('id')
        approved = request.POST.get('approved')

        activity = Activity.objects.get(pk=post_id)
        activity.approved = approved
        activity.save()
        return JsonResponse({'status': activity.approved})
    else:
        return JsonResponse({'status': 'permission denied'})
