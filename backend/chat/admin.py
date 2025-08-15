from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create a custom admin site
class CustomAdminSite(admin.AdminSite):
    site_header = 'NeuroOps Admin'
    site_title = 'NeuroOps Admin'
    index_title = 'Welcome to NeuroOps Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'redis-management/',
                self.admin_view(RedisManagementView.as_view()),
                name='chat_redis_management',
            ),
        ]
        return custom_urls + urls

# Create an instance of our custom admin site
admin_site = CustomAdminSite(name='custom_admin')

# Register the default models with our custom admin site
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)

# Redis Management View
REDIS_MANAGEMENT_TITLE = 'Redis Management'

class RedisManagementView(UserPassesTestMixin, TemplateView):
    template_name = 'chat/redis_management.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admin_site.each_context(self.request))
        context['title'] = REDIS_MANAGEMENT_TITLE
        context['site_header'] = REDIS_MANAGEMENT_TITLE
        context['site_title'] = REDIS_MANAGEMENT_TITLE
        return context

# Register your models here.
