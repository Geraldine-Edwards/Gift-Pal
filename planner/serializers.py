from rest_framework import serializers
from .models import Planner

class PlannerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model=Planner
        fields = ['id', 'title', 'description', 'start', 'end', 'all_day', 'color', 'reminder', 'wishlist', 'friends', 'username', 'profile_image']
        read_only_fields = ['id', 'user']

    def get_profile_image(self, obj):
        # Get the profile image URL for the user
        if hasattr(obj.user, 'myaccount') and obj.user.myaccount.profile_image:
            return obj.user.myaccount.profile_image.url
        return 'https://res.cloudinary.com/dn7aws3wl/image/upload/v1739390582/nobody_pcaqjl.jpg'

        def validate(self, data):
            # Ensure the start time is before the end time
            if data.get('end') and data['start'] > data['end']:
                raise serializers.ValidationError("End time must be after start time.")
            return data
            