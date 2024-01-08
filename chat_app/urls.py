from django.urls import path
from . import views


app_name = 'chat_app'
urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('chat-admin/', views.admin, name='admin'),
    path('chat-admin/users/<uuid:uuid>', views.user_detail, name='user_detail'),
    path('chat-admin/users/edit/<uuid:uuid>',
         views.edit_user, name='edit_user'),
    path('chat-admin/<str:uuid>/delete',
         views.delete_room, name='delete_room'),
    path('chat-room/<str:uuid>', views.room, name='room'),

]
