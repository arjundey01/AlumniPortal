from os import name
from django.urls import path 

from . import views

urlpatterns = [
  # /
  path('', views.home, name='home'),
  # TEMPORARY
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),
  path('signup-details', views.signup_details, name='signup-details'),
  path('update-details', views.update_details, name='update-details'),
  path('callback', views.callback, name='callback'),
  path('update-details',views.update_details),
  #path('test',views.test),
  #path('test-signup/<name>/<email>',views.test_signup),
  path('test-signin/<name>',views.test_signin),
  path('follow/',views.follow),
  path('unfollow/',views.unfollow),
  path('followers',views.followers),
  path('following',views.following),
  #path('account',views.account),
  path('account/<username>', views.profile , name='account'),
  path('details/',views.details,name="details"),
  path('update/profile/',views.updateProfile,name="update-profile"),
  path('account/add/experience/', views.experience, name='add-experience'),
  path('account/add/project/', views.project, name='add-project'),
  path('account/add/education/', views.education, name='add-education'),
  path('account/add/job/', views.pastjobs, name='add-job'),

  path('account/update/profile', views.update_account, name='update-account'),
  path('account/update/contact/', views.update_contact, name='update-contact'),
  path('account/update/experience/<pk>/', views.update_ex, name='update-experience'),
  path('account/update/project/<pk>/', views.update_p, name='update-project'),
  path('account/update/edu/<pk>/', views.update_edu, name='update-education'),
  path('account/update/job/', views.update_job, name='update-job'),

  path('account/delete/<type>/<pk>', views.delete_item, name='delete-item'),

  path('search-sugg/',views.search_sugg, name="search-sugg"),
  path('search/',views.search_res,name="search"),

  path('get-suggestions/',views.suggestions, name = 'suggestions')

]
