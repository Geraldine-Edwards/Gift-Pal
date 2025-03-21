from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Planner
from .serializers import PlannerSerializer
from friendslist.models import FriendRequest
from django.db.models import Q

class PlannerViewSet(viewsets.ModelViewSet):
    serializer_class = PlannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get events for the current user and their friends
        user = self.request.user
        accepted_requests = FriendRequest.objects.filter(
            (Q(sender=user) | Q(receiver=user)) & Q(status='accepted')
        )
        friend_ids = {req.sender.id if req.receiver == user else req.receiver.id for req in accepted_requests}
        return Planner.objects.filter(Q(user=user) | Q(user__in=friend_ids))

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        # Get events for the current user
        events = Planner.objects.filter(user=request.user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)