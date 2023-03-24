from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    # path('profile', views.profile, name='profile'),
    # path('profile/<str:pk>', views.profile, name='profile'),
    path('profile', views.profile, name='profile'),
    path('face_capture', views.face_capture, name='face_capture'),
    path('voting', views.voting, name='voting'),
    # path('position/', views.position, name='position'),
    # path('candidate/<int:pos>/', views.candidate, name='candidate'),
    # path('candidate/detail/<int:id>/', views.candidateDetail, name='detail'),
    path('result', views.result, name='result'),
    path('recognize', views.recognize, name='recognize'),
]