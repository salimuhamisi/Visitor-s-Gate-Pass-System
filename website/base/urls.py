from django.urls import path
from . import views
from .views import check_username, staff_page


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('login_view/', views.login_view, name='login_view'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('check_username/', check_username, name='check_username'),
    path('eform/', views.eform, name='eform'),
    path('staff_page', views.staff_page, name='staff_page'),
    path('administrator/', views.administrator, name='administrator'),
    path('get_visitees/', views.get_visitees, name='get_visitees'),
    path('save_comment/<int:entry_id>/', views.save_comment, name='save_comment'),
    path('logout/', views.logout_view, name='logout'),
    path('signedout/<int:id>/',views.signedout, name='signedout'),
    path('release/<int:id>/',views.release, name='release'),
    path('list/', views.list, name='list'),
    path('grouplist/', views.grouplist, name='grouplist'),
    path('agroup/', views.agroup, name='agroup'),
    path('dasboard/', views.dashboard, name='dashboard'),
    path('checked/<int:id>/', views.checked, name='checked'),
    ]