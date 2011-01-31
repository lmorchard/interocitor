from django.conf.urls.defaults import *

from django.views.generic.simple import direct_to_template

from django.views.generic.list_detail import object_list
from tagging.views import tagged_object_list

from .models import Entry


urlpatterns = patterns('main.views',

    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),

    url(r'^home$', 'home', name="main_user_home"),
    url(r'^search/?$', 'search', name="main_search"),
    url(r'^t:(?P<tag_name>[^/]+)/?$', 
        'by_tag', dict(username=''), name="main_tag"),
    url(r'^u:(?P<username>[^/]+)/post$', 
        'post', name="main_post"),
    url(r'^u:(?P<username>[^/]+)/?$', 
        'profile', name="main_profile"),
    url(r'^u:(?P<username>[^/]+)/t:(?P<tag_name>[^/]+)/?$', 
        'by_tag', name="main_profile_tag"),
    url(r'^u:(?P<username>[^/]+)/e:(?P<uuid>[^/]+)/?$', 
        'entry_detail', name="main_entry_detail_uuid"),
    url(r'^u:(?P<username>[^/]+)/(?P<slug>[^/]+)/?$', 
        'entry_detail', name="main_entry_detail"),

    url(r'^opensearch.xml$', direct_to_template,
        { 'template': 'main/opensearch.xml',
          'mimetype': 'application/opensearchdescription+xml' },
        name="opensearch"),

#    url(r'feeds/(?P<format>[^/]+)/all/', RecentSubmissionsFeed(), 
#        name="demos_feed_recent"),
#    url(r'feeds/(?P<format>[^/]+)/featured/', FeaturedSubmissionsFeed(), 
#        name="demos_feed_featured"),
#    url(r'feeds/(?P<format>[^/]+)/search/(?P<query_string>[^/]+)/$', SearchSubmissionsFeed(), 
#        name="demos_feed_search"),
#    url(r'feeds/(?P<format>[^/]+)/tag/(?P<tag>[^/]+)/$', TagSubmissionsFeed(), 
#        name="demos_feed_tag"),
#    url(r'feeds/(?P<format>[^/]+)/profile/(?P<username>[^/]+)/?$', ProfileSubmissionsFeed(), 
#        name="demos_feed_profile"),
    
)
