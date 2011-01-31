from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
import feedparser

from django.contrib.auth.models import User
from main.models import Entry

import sys
from datetime import datetime
import xml.sax
from xml.sax.handler import ContentHandler

COUNT_CHUNK = 100

class Command(BaseCommand):
    args = '<filename>'
    help = 'Import status items from an Atom or RSS feed'

    option_list = BaseCommand.option_list + (
        make_option('--actor', dest='actor', default='lmorchard',
            help='Name of user as actor'),
        make_option('--verb', dest='verb', default='post',
            help='Verb for action (eg. post)'),
        make_option('--object', dest='object', default='status',
            help='Object for action (eg. status)'),
    )

    posts_cnt = 0

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Feed filename required')

        actor_user = User.objects.get(username = options['actor'])

        d = feedparser.parse(args[0])

        print "Importing %s entries for %s" % ( len(d.entries), actor_user.username )

        for f_entry in d.entries:
            (entry, created) = Entry.objects.get_or_create(
                actor_user = actor_user, 
                verb_type = options['verb'],
                object_type = options['object'],
                link = f_entry['links'][0]['href'], 
                defaults = dict(
                    title = f_entry['title'],
                    summary = f_entry['summary'],
                )
            )
            if created:
                entry.published = datetime(*f_entry['published_parsed'][:7])
                entry.save()

            sys.stdout.write('.')
            self.posts_cnt += 1
            if (self.posts_cnt % COUNT_CHUNK) == 0:
                sys.stdout.write('%s\n'%self.posts_cnt)
                sys.stdout.flush()


