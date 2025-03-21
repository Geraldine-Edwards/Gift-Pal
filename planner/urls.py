from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import PlannerViewSet

app_name = 'planner'

router = DefaultRouter()
router.register(r'events', PlannerViewSet, basename='event')

urlpatterns = [
    # Serve the planner.html template
    path('', TemplateView.as_view(template_name='planner/planner.html'), name='planner_view'),
    
    # Include DRF router URLs
    path('api/', include(router.urls)),
]
