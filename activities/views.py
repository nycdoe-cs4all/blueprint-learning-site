from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Activity, Grade, Subject, Device, Profile, Concept, Software, Bookmark, Resource, ResourceTag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ActivityForm, UserProfileForm, ResourceForm



# Create your views here.
def index(request):
    # _devices = Activity.objects.all().raw("SELECT id, body->'devices' AS device FROM activities_activity")
    # all_devices = []
    # for device in _devices:
    #     all_devices += device.device
    # all_devices = sorted(list(set(all_devices)))

    all_devices = [d.name for d in Device.objects.all()]
    all_software = [s.name for s in Software.objects.all()]
    all_concepts = [c.name for c in Concept.objects.all()]

    grades = Grade.objects.all()
    subjects = Subject.objects.all()

    q = request.GET.get('q', '')
    grade = request.GET.get('grade')
    subject = request.GET.get('subject')
    concepts = request.GET.getlist('concepts')
    level = request.GET.get('level')
    devices = request.GET.getlist('devices')
    software = request.GET.getlist('software')
    page = request.GET.get('page')

    if request.user.is_superuser:
        approved = str((request.GET.get('approved', 0)))
    else:
        approved = str(request.GET.get('approved', 1))

    filters = {'q': q, 'grade': grade, 'subject': subject, 'level': level, 'devices': devices, 'software': software, 'approved': approved, 'concepts': concepts}

    activities_list = Activity.objects.order_by('-date_added')

    if grade:
        activities_list = activities_list.filter(body__grade=grade)

    if approved:
        activities_list = activities_list.filter(approved=approved)

    if subject:
        activities_list = activities_list.filter(body__subject=subject)

    if software:
        activities_list = activities_list.filter(body__software__contains=software)

    if concepts:
        activities_list = activities_list.filter(body__concepts__contains=concepts)

    if devices:
        activities_list = activities_list.filter(body__devices__contains=devices)

    if request.GET.get('q'):
        vector = SearchVector('plain_body', 'title')
        query = SearchQuery(q)
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
    context = {'activities': activities, 'grades': grades, 'subjects': subjects, 'filters': filters, 'all_devices': all_devices, 'all_software': all_software, 'all_concepts': all_concepts}
    return render(request, 'activities/index.html', context)


@login_required
def create_bookmark(request):
    activity_id = request.POST.get('activity_id')
    activity = get_object_or_404(Activity, pk=activity_id)
    bookmark = Bookmark(user_id=request.user.id, activity_id=activity_id)
    bookmark.save()
    return redirect('/activities/' + activity_id)


@login_required
def delete_bookmark(request):
    activity_id = request.POST.get('activity_id')
    Bookmark.objects.filter(user=request.user, activity_id=activity_id).delete()
    return redirect('/activities/' + activity_id)


@login_required
def create(request):
    title = request.POST.get('title')
    subject = request.POST.get('subject')
    grade = request.POST.get('grade')
    body = request.POST.get('html_body')
    pacing = request.POST.get('pacing')
    plain_body = request.POST.get('plain_body')

    submitted_concepts = request.POST.get('concepts').split(':::')
    submitted_concepts = [c.lower() for c in submitted_concepts]
    possible_concepts = Concept.objects.all()
    concepts = [c.name for c in possible_concepts if c.name.lower() in submitted_concepts]

    submitted_software = request.POST.get('software').split(':::')
    submitted_software = [s.lower() for s in submitted_software]
    possible_software = Software.objects.all()
    softwares = [s.name for s in possible_software if s.name.lower() in submitted_software]

    submitted_devices = request.POST.get('devices').split(':::')
    submitted_devices = [d.lower() for d in submitted_devices]
    possible_devices = Device.objects.all()
    devices = [d.name for d in possible_devices if d.name.lower() in submitted_devices]

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
            'pacing': pacing,
            'html': body,
            'plain': plain_body,
            'devices': devices,
            'concepts': concepts,
            'software': softwares
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


@login_required
def new(request):
    grades = Grade.objects.all()
    devices = Device.objects.all()
    subjects = Subject.objects.all()
    concepts = Concept.objects.all()
    software = Software.objects.all()
    context = {'concepts': concepts, 'software': software, 'grades': grades, 'devices': devices, 'subjects': subjects}

    return render(request, 'activities/new.html', context)


def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    try:
        profile = Profile.objects.filter(user=request.user)[:1].get()
    except:
        profile = None
    has_bookmark = False
    if request.user.is_authenticated:
        has_bookmark = Bookmark.objects.filter(user=request.user, activity=activity).count() > 0
    resources = activity.resource_set.all()
    return render(request, 'activities/detail.html', {'activity': activity, 'profile': profile, 'has_bookmark': has_bookmark, 'resources': resources})


@login_required
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


@login_required
def refresh(request):
    from .get_activity import Activity as ActivityParser
    post_id = request.POST.get('id')
    activity = Activity.objects.get(pk=post_id)
    if request.user.id == activity.user_id or request.user.is_superuser:
        parser = ActivityParser(activity.google_file_id)
        activity.plain_body = parser.plain_body
        activity.html_body = parser.body
        activity.save()
        return JsonResponse({'body': activity.html_body})
    else:
        return JsonResponse({'status': 'permission denied'})


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile#Profile.objects.filter(user=request.user)[:1].get()
        form = UserProfileForm(instance=profile)
    except Exception as e:
        print(e)
        form = UserProfileForm()
        profile = None

    if request.method == 'POST':
        if profile is not None:
            form = UserProfileForm(request.POST, instance=profile)
        else:
            form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect(reverse('user_detail', args=(request.user.id,)))

    return render(request, 'users/edit_profile.html', {'form':form})


def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    bookmarks = Activity.objects.filter(bookmark__user=user)
    # bookmarks = Bookmark.objects.filter(user=user)
    profile = user.profile
    activities = Activity.objects.filter(user=user)
    return render(request, 'users/detail.html', {'activities': activities, 'bookmarks': bookmarks, 'user': user, 'profile': profile})

@user_passes_test(lambda u: u.is_superuser)
def create_resource(request):
    form = ResourceForm(request.POST or None)
    print(form)
    if form.is_valid():
        form.save()
        return redirect('list_resources')
    return render(request, 'resources/form.html', {'form':form})


@user_passes_test(lambda u: u.is_superuser)
def edit_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    form = ResourceForm(request.POST or None, instance=resource)
    if form.is_valid():
        form.save()
        return redirect('list_resources')
    return render(request, 'resources/form.html', {'form':form})


@user_passes_test(lambda u: u.is_superuser)
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)    
    if request.method=='POST':
        resource.delete()
        return redirect('list_resources')


def show_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    activities = resource.activities.all()
    return render(request, 'resources/details.html', {'resource':resource, 'activities': activities})


def list_resources(request):
    tag_name = request.GET.get('tag')
    if tag_name:
        resources = Resource.objects.filter(tags__title=tag_name)
    else:
        resources = Resource.objects.all()
    tags = ResourceTag.objects.all()
    return render(request, 'resources/index.html', {'resources': resources, 'tags': tags})


def import_google_doc(request):
    from .get_activity import KEY
    from apiclient.discovery import build
    from bs4 import BeautifulSoup
    from django.http import HttpResponse
    import re

    file_id = request.GET.get('file_id')
    if '/' in file_id:
        file_id = file_id.split('/')[-2]

    drive_service = build('drive', 'v3', developerKey=KEY)
    files = drive_service.files()
    response = files.export(fileId=file_id, mimeType='text/html')
    html = response.execute()
    soup = BeautifulSoup(html, 'html.parser')

    body = str(soup.find('body'))
    body = re.sub(r"\s*style='(.*?)'\s*", '', body, flags=re.MULTILINE)
    body = re.sub(r'\s*(style|id)="(.*?)"\s*', '', body, flags=re.MULTILINE)

    return HttpResponse(body)
