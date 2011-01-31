from datetime import datetime
from time import strftime
import re

from django.db import models
from django.db.models import Q

from django.contrib.auth.models import User
from tagging.models import Tag, TaggedItem

from tagging.utils import parse_tag_input
from tagging.fields import TagField
from tagging.models import Tag

from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

try:
    import uuid
except ImportError:
    from django.utils import uuid


def make_uuid():
    return str(uuid.uuid4())


class EntryManager(models.Manager):

    # TODO: Make these search functions into a mixin?

    # See: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
    def _normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:
            
            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
        
        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

    # See: http://www.julienphalip.com/blog/2008/08/16/adding-search-django-site-snap/
    def _get_query(self, query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.
        
        '''
        query = None # Query to search for every search term        
        terms = self._normalize_query(query_string)
        for term in terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def search(self, query_string, sort):
        """Quick and dirty keyword search on submissions"""
        # TODO: Someday, replace this with something like Sphinx or another real search engine
        strip_qs = query_string.strip()
        if not strip_qs:
            return self.all_sorted(sort).order_by('-published')
        else:
            query = self._get_query(strip_qs, ['title', 'link', 'summary',
                'content', 'tags', 'meta', ])
            return self.all_sorted(sort).filter(query).order_by('-published')

    def all_sorted(self, sort=None):
        """Apply to .all() one of the sort orders supported for views"""
        queryset = self.all()
        if sort == 'modified':
            return queryset.order_by('-modified')
        else:
            return queryset.order_by('-published')


class Entry(models.Model):
    objects = EntryManager()

    class Meta:
        verbose_name_plural = "Entries"

    uuid = models.CharField(max_length=36,
        default=make_uuid, editable=False)

    slug = models.CharField(max_length=255, blank=True)#, unique=True)

    title = models.CharField(max_length=255, blank=True)#, unique=True)
    link = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    
    tags = TagField()

    verb_type = models.CharField(max_length=255, blank=True)
    object_type = models.CharField(max_length=255, blank=True)
    target_type = models.CharField(max_length=255, blank=True)

    meta = models.TextField(blank=True)

    actor_user = models.ForeignKey(User, blank=True)

    published = models.DateTimeField( _('date published'), 
            auto_now_add=True, blank=False)
    modified = models.DateTimeField( _('date last modified'), 
            auto_now=True, blank=False)
    
    def save(self, **kwargs):
        """Save the entry, updating slug"""
        self.slug = slugify(self.title)
        super(Entry,self).save(**kwargs)

    def get_absolute_url(self):
        #return reverse('main_entry_detail', 
        #       kwargs={'username':self.actor_user.username, 'slug':self.slug})
        return reverse('main.views.entry_detail', 
                kwargs={'username':self.actor_user.username, 'uuid':self.uuid})
    

class EntryAnnotationManager(models.Manager):
    pass

class EntryAnnotation(models.Model):
    objects = EntryAnnotationManager()

