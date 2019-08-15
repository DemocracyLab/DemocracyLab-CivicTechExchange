"""democracylab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProjectSitemap


from . import views

urlpatterns = [

    url(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': {'projects': ProjectSitemap()}},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    url(r'^googlebb20bcf8545e7046.html$', TemplateView.as_view(template_name="googlebb20bcf8545e7046.html")),
    url(r'^groups/create/$', views.group_create, name='group_create'),
    url(r'^groups/edit/(?P<group_id>[0-9]+)/$', views.group_edit, name='group_edit'),
    url(r'^groups/delete/(?P<group_id>[0-9]+)/$', views.group_delete, name='group_delete'),
    url(r'^projects/edit/(?P<project_id>[0-9]+)/$', views.project_edit, name='project_edit'),
    url(r'^projects/delete/(?P<project_id>[0-9]+)/$', views.project_delete, name='project_delete'),
    url(r'^projects/signup/$', views.project_create, name='project_create'),
    url(r'^projects/approve/(?P<project_id>[0-9]+)/$', views.approve_project, name='approve_project'),
    url(
        r'^presign_s3/upload/project/thumbnail/$',
        views.presign_project_thumbnail_upload,
    ),
    url(
        r'^delete_s3/(?P<s3_key>.*)$',
        views.delete_uploaded_file,
    ),
    url(r'^api/projects', views.projects_list),
    url(r'^api/my_projects', views.my_projects),
    url(r'^api/tags', views.tags),
    url(r'^index/$', views.index),
    url(r'^api/stats$', views.get_site_stats, name='get_site_stats'),
    url(r'^api/project/(?P<project_id>[0-9]+)/$', views.get_project, name='get_project'),
    url(r'^api/group/(?P<group_id>[0-9]+)/$', views.get_group, name='get_group'),
    url(r'^contact/project/(?P<project_id>[0-9]+)/$', views.contact_project_owner, name='contact_project_owner'),
    url(r'^contact/volunteers/(?P<project_id>[0-9]+)/$', views.contact_project_volunteers, name='contact_project_volunteers'),
    url(r'^contact/volunteer/(?P<application_id>[0-9]+)/$', views.contact_project_volunteer, name='contact_project_volunteer'),
    url(r'^volunteer/(?P<project_id>[0-9]+)/$', views.volunteer_with_project, name='volunteer_with_project'),
    url(r'^volunteer/leave/(?P<project_id>[0-9]+)/$', views.leave_project, name='leave_project'),
    url(r'^volunteer/approve/(?P<application_id>[0-9]+)/$', views.accept_project_volunteer, name='accept_project_volunteer'),
    url(r'^volunteer/reject/(?P<application_id>[0-9]+)/$', views.reject_project_volunteer, name='reject_project_volunteer'),
    url(r'^volunteer/dismiss/(?P<application_id>[0-9]+)/$', views.dismiss_project_volunteer, name='dismiss_project_volunteer'),
    url(r'^volunteer/promote/(?P<application_id>[0-9]+)/$', views.promote_project_volunteer, name='promote_project_volunteer'),
    url(r'^volunteer/demote/(?P<application_id>[0-9]+)/$', views.demote_project_volunteer, name='demote_project_volunteer'),
    url(r'^volunteer/renew/(?P<application_id>[0-9]+)/$', views.renew_volunteering_with_project, name='renew_volunteering_with_project'),
    url(r'^volunteer/conclude/(?P<application_id>[0-9]+)/$', views.conclude_volunteering_with_project, name='conclude_volunteering_with_project'),
    url(r'^alert/create/$', views.add_alert, name='add_alert')

]
