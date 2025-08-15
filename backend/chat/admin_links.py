from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin import AdminSite


def add_admin_links(site: AdminSite):
    """Add custom admin links."""
    site.site_header = "NeuroOps Admin"
    site.site_title = "NeuroOps Admin"
    site.index_title = "Welcome to NeuroOps Admin"

    # Add Redis Management link to the admin site
    def redis_management_link(request):
        url = reverse('admin:chat_redis_management')
        return format_html('<a href="{}" class="button">Redis Management</a>', url)

    redis_management_link.short_description = "Redis Management"
    redis_management_link.allow_tags = True

    # Add the link to the admin site
    site.index_template = 'admin/redis_admin_index.html'
    
    # Create a simple template to extend the admin index
    from django.template.loader import render_to_string
    from django.template import engines
    
    # Create the admin directory if it doesn't exist
    import os
    admin_templates_dir = os.path.join(os.path.dirname(__file__), 'templates/admin')
    os.makedirs(admin_templates_dir, exist_ok=True)
    
    # Create the custom admin index template
    with open(os.path.join(admin_templates_dir, 'redis_admin_index.html'), 'w') as f:
        f.write('''
{% extends "admin/index.html" %}
{% load i18n %}

{% block sidebar %}
    <div id="content-related">
        <div class="module">
            <h2>Redis Management</h2>
            <ul class="actionlist">
                <li class="addlink">
                    <a href="{% url 'admin:chat_redis_management' %}">
                        Go to Redis Management Interface
                    </a>
                </li>
            </ul>
        </div>
    </div>
    {{ block.super }}
{% endblock %}
        ''')
