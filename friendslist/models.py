from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages


class Friendship(models.Model):
    """
    Model representing a friendship between two users.

    Attributes:
        user1 (ForeignKey): The user who initiated the friendship.
        user2 (ForeignKey): The user who is the friend.
        created_at (DateTimeField): The date and time when the friendship was created.
    """
    user1 = models.ForeignKey(
        User, 
        related_name='friendship_user1', 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user2 = models.ForeignKey(
        User, 
        related_name='friendship_user2', 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the Friendship model.

        Attributes:
            unique_together (tuple): Ensures that each pair of user and friend is unique.
        """
        constraints = [
        models.UniqueConstraint(
            fields=['user1', 'user2'],
            name='unique_friendship',
            condition=Q(user1__lt=models.F('user2'))  # Ensures user1 is always lower ID
        )
    ]
    ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string representation of the Friendship instance.

        Returns:
            str: A string indicating the usernames of the user and their friend.
        """
        return f"{self.user1} ↔ {self.user2}"

    @classmethod
    def create_friendship(cls, user1, user2):
        """Create a friendship in a normalized order (user1.id < user2.id)."""
        # Ensure user1.id < user2.id to avoid duplicates like (A,B) and (B,A)
        if user1.id > user2.id:
            user1, user2 = user2, user1
        return cls.objects.get_or_create(user1=user1, user2=user2)


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(
        User, 
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, 
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the FriendRequest model.

        Attributes:
            constraints: Ensures that each friend request is unique.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name='unique_friend_request'
            )
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"

    def clean(self):
            """
        Validates the Friendship instance.

        Raises:
            ValidationError: If the user is trying to be friends with themselves.
        """
        # Prevent sending requests to oneself
            if self.sender == self.receiver:
                raise ValidationError("You cannot send a friend request to yourself.")

        # Prevent duplicate pending requests
            if FriendRequest.objects.filter(
                sender=self.sender, 
                receiver=self.receiver, 
                status='pending'
                ).exclude(pk=self.pk).exists():
                    raise ValidationError("A pending request already exists.")

    def accept(self):
        """Accept the friend request and create a Friendship."""
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()
            # Create a bidirectional Friendship
            Friendship.create_friendship(self.sender, self.receiver)
            messages.success(request, "Friend request accepted!")  # Pass the request object
        else:
            raise ValidationError("This request is no longer valid.")

    def decline(self):
        """Decline the friend request."""
        if self.status == 'pending':
            self.status = 'declined'
            self.save()
            messages.info(request, "Friend request declined.")  # Pass the request object
        else:
            raise ValidationError("This request is no longer valid.")