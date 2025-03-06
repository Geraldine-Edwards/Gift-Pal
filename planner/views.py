from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Planner
from friendslist.models import Friendship, FriendRequest
from .forms import EventForm
import json
import logging


@login_required
def planner_view(request):
    # Render the main calendar template
    return render(request, 'planner/planner.html')


@login_required
def add_event(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            title = data.get('title')
            start_str = data.get('start')
            end_str = data.get('end')
            color = data.get('color')
            description = data.get('description')

            # Parse datetimes
            start_datetime = parse_datetime(start_str)
            end_datetime = parse_datetime(end_str) if end_str else None

            # Validate and make timezone-aware
            if not start_datetime:
                return JsonResponse({'status': 'error', 'message': 'Invalid start date/time'}, status=400)
            
            if timezone.is_naive(start_datetime):
                start_datetime = timezone.make_aware(start_datetime)
            
            if end_datetime and timezone.is_naive(end_datetime):
                end_datetime = timezone.make_aware(end_datetime)

            # Create the event
            event = Planner.objects.create(
                user=request.user,
                title=title,
                start=start_datetime,  # Use parsed datetime
                end=end_datetime,      # Use parsed datetime
                color=color,
                description=description
            )

            # Return a success response with the new event data
            return JsonResponse({
                'status': 'success',
                'event': {
                    'id': event.id,
                    'title': event.title,
                    'start': event.start.isoformat(),
                    'end': event.end.isoformat() if event.end else None,
                    'color': event.color,
                    'description': event.description,
                }
            })
        except Exception as e:
            # Return an error response
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@login_required
def edit_event(request, event_id):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            title = data.get('title')
            start_str = data.get('start')
            end_str = data.get('end')
            color = data.get('color')
            description = data.get('description')

            # Improved datetime parsing
            try:
                start_datetime = timezone.make_aware(parse_datetime(start_str))
                end_datetime = timezone.make_aware(parse_datetime(end_str)) if end_str else None
                
            except (ValueError, TypeError) as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Invalid date format: {str(e)}. Use ISO format (YYYY-MM-DDTHH:mm)'
                }, status=400)
            
            if timezone.is_naive(start_datetime):
                start_datetime = timezone.make_aware(start_datetime)
            
            if end_datetime and timezone.is_naive(end_datetime):
                end_datetime = timezone.make_aware(end_datetime)

            # Get the event to edit
            event = Planner.objects.get(id=event_id, user=request.user)

            # Update the event
            event.title = title
            event.start = start_datetime
            event.end = end_datetime
            event.color = color
            event.description = description
            event.save()

            # Return a success response with the updated event data
            return JsonResponse({
                'status': 'success',
                'event': {
                    'id': event.id,
                    'title': event.title,
                    'start': event.start.isoformat(),  # Now event.start is a datetime object
                    'end': event.end.isoformat() if event.end else None,
                    'color': event.color,
                    'description': event.description,
                }
            })
        except Planner.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
        except Exception as e:
            # Return an error response
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@login_required
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            # Get the event to delete
            event = Planner.objects.get(id=event_id, user=request.user)
            event.delete()

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Event deleted successfully'})
        except Planner.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


logger = logging.getLogger(__name__)


@login_required
@ensure_csrf_cookie
def get_events(request):
    try:
        logger.info("Fetching events for user: %s", request.user)

        # Get events for current user
        user_events = Planner.objects.filter(
            user=request.user).select_related('user')

        # Get friend IDs
        accepted_requests = FriendRequest.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)) &
            Q(status='accepted')
        )
        friend_ids = set()
        for req in accepted_requests:
            friend = req.sender if req.receiver == request.user else req.receiver
            friend_ids.add(friend.id)

        # Get friends' events
        friends_events = Planner.objects.filter(
            user__in=friend_ids).select_related('user')

        # Combine and serialize events
        events = []
        for event in user_events.union(friends_events):
            profile_image = (event.user.myaccount.profile_image.url
                            if hasattr(event.user, 'myaccount') and event.user.myaccount.profile_image
                            else '/static/images/nobody.jpg')

            events.append({
                'id': event.id,
                'title': event.title,
                'start': event.start.isoformat(),
                'end': event.end.isoformat() if event.end else None,
                'color': event.color,
                'description': event.description,
                'is_friend': event.user != request.user,
                'profile_image': profile_image,
                'user': event.user.username
            })

        return JsonResponse({'events': events}, safe=False)
    except Exception as e:
        logger.error("Error fetching events: %s", str(e), exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
