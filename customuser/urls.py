from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^$', views.welcome_page, name='welcome_page'),#settignup homepage
    url(r'^register/$', views.registration_page, name='registration'),#custom Reg template
    url(r'^login/$', views.login_page, name='login'),#custom Login template
    url(r'^logout/$', auth_views.logout, {'template_name': 'customuser/logout.html'}, name='logout'),#custom template#system defined
    url(r'^user/(?P<pk>\d+)/verify/$', views.verify_user, name='verify_user'),
    url(r'^profile/$', views.user_profile, name='profile'),#custom Reg template
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]
