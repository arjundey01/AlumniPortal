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
  #path('test',views.test),
  #path('test-signup/<name>/<email>',views.test_signup),
  path('test-signin/<name>',views.test_signin),
  path('follow/',views.follow),
  path('unfollow/',views.unfollow),
  path('followers',views.followers),
  path('following',views.following),
  #path('account',views.account),
  path('account/<username>', views.profile , name='account'),
  path('update-account', views.update_account, name='update-account')
]