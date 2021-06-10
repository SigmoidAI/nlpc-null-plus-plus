from django.urls import path
from . import views

'''
  A list of url paths this web application accepts.
  The path function is a django function used with the following arguments:
    1. route - an URL that the web application will accept. You can specify parameters (using '<' and '>'), which will be available in the request object
    2. view - the view that will be executed when a client requests on the specified route
    3. name - a name given to the current path
'''

urlpatterns = [
    path('', views.indexView, name='index'),
    path('post/', views.createPost, name='create'),
    path('post/<int:post_id>/', views.postDetailView, name='detail'),
    path('post/<int:post_id>/delete/', views.deletePostView, name='delete'),
    path('profile/<int:user_id>/', views.profileView, name='profile'),
    path('profile/<int:user_id>/delete/', views.profileDeleteView, name='profile-delete'),
    path('comment/', views.createCommentView, name='comment-create'),
    path('comment/delete/', views.deleteCommentView, name='comment-delete'),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
]
