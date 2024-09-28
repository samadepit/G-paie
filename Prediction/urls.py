from django.contrib import admin
from django.urls import include, path
from Prediction import views


urlpatterns = [
    path("goapp/", views.object_detection_view),
    path('task-list/<str:pk>', views.taskList),
    path('create/', views.add_items, name='add-items'),
    path('all/', views.view_items, name='view_items'),
    path('update/<int:pk>/', views.update_items, name='update-items'),
    path('item/<int:pk>/delete/', views.delete_items, name='delete-items'),

]
