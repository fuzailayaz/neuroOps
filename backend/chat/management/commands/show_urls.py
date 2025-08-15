from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Show all URLs in the project'

    def handle(self, *args, **options):
        resolver = get_resolver()
        self.print_urls(resolver.url_patterns, prefix='')

    def print_urls(self, urls, prefix=''):
        for url in urls:
            if hasattr(url, 'url_patterns'):
                self.print_urls(url.url_patterns, prefix + str(url.pattern))
            else:
                self.stdout.write(f"{prefix}{url.pattern} -> {url.callback.__module__}.{url.callback.__name__}")
