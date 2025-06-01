from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

routers = routers.DefaultRouter()
routers.register(r'conversations', ConversationViewSet, basename='conversations')
routers.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(routers.urls)),
]
