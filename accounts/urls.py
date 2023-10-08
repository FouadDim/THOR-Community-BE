from django.urls import path
from .views import *

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('create-opensource-project', createOSP, name='createOSP'),
    path('join-opensource-project', joinOSP, name='joinOSP'),
    path('get-opensource-projects', getOSPs, name='getOSPs'),
    path('get-my-opensource-project', getOSP, name='getOSP'),
    path('get-opensource-project', getOSPa, name='getOSPa'),
    path('check-verified', checkVerified, name='checkVerified'),
    path('get-all-opensource', getAllOSP, name='getAllOSP'),
    
    # path('/create-community', createCommunity, name='createCommunity'),
    # path('/join-community', joinCommunity, name='joinCommunity'),
    # path('/chat/community/:id', chatCommunity, name='chatCommunity'),
    # path('/manage-projects/get-all', getAllProjects, name='getAllProjects'),
    # path('/manage-projects/get-one', getProject, name='getProject'),
    # path('/manage-projects/get-project-chat', getProjectChat, name='getProjectChat'),
    # path('/manage-projects/delete', deleteProject, name='deleteProject'),
]
