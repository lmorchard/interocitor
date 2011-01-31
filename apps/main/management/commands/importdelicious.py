from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from main.models import Entry

import sys
from datetime import datetime
import xml.sax
from xml.sax.handler import ContentHandler

COUNT_CHUNK = 100

class Command(BaseCommand):
    help = 'Import bookmarks exported from the Delicious API'
    args = '<filename>'

    option_list = BaseCommand.option_list + (
        make_option('--actor', dest='actor', default='lmorchard',
            help='Name of user as actor'),
        make_option('--verb', dest='verb', default='post',
            help='Verb for action (eg. post)'),
        make_option('--object', dest='object', default='bookmark',
            help='Object for action (eg. status)'),
    )

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Export filename required')
        user = User.objects.get(username = USERNAME)
        handler = DeliciousXmlContentHandler(user, options['verb'], options['object'])
        xml.sax.parse(open(args[0], 'r'), handler)

class DeliciousXmlContentHandler(ContentHandler):
    
    posts_cnt = 0
    verb = None
    object = None

    def __init__(self, user, verb, object):
        self.user = user
        self.verb = verb
        self.object = object

    def startDocument(self):
        sys.stdout.write("Importing delicious bookmarks for %s\n" % self.user.username)

    def endDocument(self):
        sys.stdout.write("\nDONE.\n")

    def startElement(self, name, attrs):

        if 'post' == name:

            post = dict(attrs.copy())

            (entry, created) = Entry.objects.get_or_create(
                actor_user = self.user, 
                verb_type = self.verb,
                object_type = self.object,
                link = post['href'], 
                defaults = dict(
                    title = post['description'],
                    summary = post['extended'],
                    tags = post['tag'],
                )
            )
            if created:
                entry.published = datetime.strptime(post['time'], "%Y-%m-%dT%H:%M:%SZ")
                entry.save()

            sys.stdout.write('.')
            self.posts_cnt += 1
            if (self.posts_cnt % COUNT_CHUNK) == 0:
                sys.stdout.write('%s\n'%self.posts_cnt)
                sys.stdout.flush()

