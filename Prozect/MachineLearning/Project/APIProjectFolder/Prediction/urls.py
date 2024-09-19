from django.contrib import admin
from django.urls import include, path
from Prediction import views


urlpatterns = [
    path("goapp/", views.object_detection_view),
    path('task-list/<str:pk>', views.taskList),
]
