from django.urls import path
from .views import (
    ActivityLogListView,
    UserActivityLogView,
)

urlpatterns = [
    # List all activity logs (admin only)
    path('', ActivityLogListView.as_view(), name='activity-log-list'),

    # List activity logs for a specific user (admin only)
    path('user/<int:user_id>/', UserActivityLogView.as_view(), name='user-activity-log'),
]