from django.urls import path

from . import views

app_name = 'todoapp'

urlpatterns = [
    # get all and post the project code
    path('projcode', views.ProjCodeListView.as_view(),name="projcode"),
    # get all and post the todo task
    path('task', views.TODOListView.as_view(),name='task'),
    # edit & update the images
    path("taskdetail/", views.TODODetailView.as_view(),name='taskdetail'),
    path("taskdetail/(?p<task_id>[\w-]+)/", views.TODODetailView.as_view(),name='taskdetail'),

]