from django.urls import path
from .views import ActionsAPIview,NotificationsAPIview,ActionsForUserAPIview

urlpatterns = [
    path('actions/', ActionsAPIview.as_view(), name='actions-list'),
    path('user/actions/', ActionsForUserAPIview.as_view(), name='ActionsForUserAPIview'),
    path('user/actions/<int:pk>', ActionsForUserAPIview.as_view(), name='ActionsForUserAPIview'),
    path('actions/<int:pk>/', ActionsForUserAPIview.as_view(), name='ActionsForUserAPIview'),
    path('notification/', NotificationsAPIview.as_view(), name='NotificationsAPIview'),
    path('notification/<int:pk>/', NotificationsAPIview.as_view(), name='NotificationsAPIview'),
]
