from os import name
from django.urls import path 

from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('signin/', views.sign_in, name='signin'),
  path('signout/', views.sign_out, name='signout'),
  path('signup-details/', views.signup_details, name='signup-details'),
  path('update-details/', views.update_profile, name='update-details'),
  path('callback', views.callback, name='callback'),
  #path('test',views.test),
  #path('test-signup/<name>/<email>',views.test_signup),
  # path('test-signin/<name>/',views.test_signin),
  path('follow/',views.follow),
  path('unfollow/',views.unfollow),
  path('followers/',views.followers),
  path('following/',views.following),
  #path('account',views.account),
  path('account/<username>/', views.profile , name='account'),
  path('details/',views.details,name="details"),
  # path('update/profile/',views.updateProfile,name="update-profile"),
  path('account/experience/<action>/', views.experience, name='experience'),
  path('account/project/<action>/', views.project, name='project'),
  path('account/education/<action>/', views.education, name='education'),
  path('account/job/<action>/', views.pastjobs, name='job'),
  path('account/change-profile-img/',views.update_photo, name="change-profile-img"),
  path('account/contact/update/',views.update_contact, name="update-contact"),

  path('search-sugg/',views.search_sugg, name="search-sugg"),
  path('search/',views.search_res,name="search"),
  # path('search/',views.filter_list,name="filter"),

  path('get-suggestions/',views.suggestions, name = 'suggestions')

]
