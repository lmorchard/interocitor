from django.conf import settings

from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseForbidden

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from django.views.generic.list_detail import object_list
from tagging.views import tagged_object_list

from django.contrib.auth.models import User

from .models import Entry
from .forms import EntryNewForm, EntryEditForm

# @@TODO: Convert to class-based view?

def home(request):
    """Redirect to logged in user's profile, or to site home"""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('main.views.profile', 
            kwargs={'username':request.user.username}))
    else:
        return HttpResponseRedirect(reverse('home'))

def entry_detail(request, username, uuid=None, slug=None):
    """Detail on a single entry"""
    profile_user = get_object_or_404(User, username=username)

    if uuid:
        entry = get_object_or_404(Entry, uuid=uuid, actor_user=profile_user)
    elif slug:
        entry = get_object_or_404(Entry, slug=slug, actor_user=profile_user)
    else:
        return HttpResponseNotFound()

    return render_to_response('main/entry_detail.html', dict(
        profile_user=profile_user, entry=entry   
    ), context_instance=RequestContext(request))

def post(request, username):
    """Accept a new post"""
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    if username != request.user.username:
        return HttpResponseForbidden()

    profile_user = get_object_or_404(User, username=username)

    if request.method != "POST":
        form = EntryNewForm()
    else:
        form = EntryNewForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.actor_user = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('main.views.entry_detail',
                kwargs={'username':username,'uuid':new_entry.uuid}))

    return render_to_response('main/post.html', dict(
        profile_user=profile_user, form=form
    ), context_instance=RequestContext(request))

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    queryset = Entry.objects.filter(actor_user=profile_user).order_by('-published').all()

    return object_list(request, queryset,
        extra_context=dict(
            profile_user=profile_user,
        ),
        paginate_by=25, allow_empty=True,
        template_object_name='entry',
        template_name='main/profile.html') 

def by_tag(request, tag_name, username=None):

    profile_user = username and get_object_or_404(User, username=username) or None

    sort_order = request.GET.get('sort', 'published')

    queryset = Entry.objects.all_sorted(sort_order)
    if username:
        queryset = queryset.filter(actor_user=profile_user)

    return tagged_object_list(request,
        extra_context=dict(
            profile_user=profile_user
        ),
        queryset_or_model=queryset, tag=tag_name,
        paginate_by=24, allow_empty=True, 
        template_object_name='entry',
        template_name='main/listing_tag.html')

def search(request):
    """Search against Entry title, summary, and description"""
    query_string = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'published')
    queryset = Entry.objects.search(query_string, sort_order)
    return object_list(request, queryset,
        paginate_by=25, allow_empty=True,
        template_object_name='entry',
        template_name='main/listing_search.html') 
    
