from django.urls import path
from .views import ActionsAPIview

urlpatterns = [
    path('actions/', ActionsAPIview.as_view(), name='actions-list'),
    path('actions/<int:pk>/', ActionsAPIview.as_view(), name='actions-detail'),
]
