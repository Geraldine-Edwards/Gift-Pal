from django.urls import path
from .views import planner_view, add_event, edit_event, delete_event, get_events

app_name = 'planner'

urlpatterns = [
    path('', planner_view, name='planner_view'),
    path('get-events/', get_events, name='get_events'),
    path('add/', add_event, name='add_event'),
    path('edit/<int:event_id>/', edit_event, name='edit_event'),
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
]
