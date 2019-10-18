from django.urls import path
import index.consumers

websocketUrlpatterns = [
    path('', index.consumers.index),
]
