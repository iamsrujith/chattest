from django.urls import path

from chatapp.views import home, signup, login_view, logout_view, update_status, chat_room, join_chat

urlpatterns = [
    path('', home, name="index"),
    path('signup/', signup, name="signup"),
    path('update-status/', update_status, name="status"),
    path('accounts/login/', login_view, name="login"),
    path('accounts/logout/', logout_view, name="logout"),
    path('chat/<str:id>/', chat_room, name='chat_room'),
    path('join/', join_chat, name='join_chat'),
]