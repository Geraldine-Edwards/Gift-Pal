from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


class Friendship(models.Model):
    """
    Model representing a friendship between two users.

    Attributes:
        user (ForeignKey): The user who initiated the friendship.
        friend (ForeignKey): The user who is the friend.
        created_at (DateTimeField): The date and time when the friendship was created.
        updated_at (DateTimeField): The date and time when the friendship was last updated.
        confirmed (BooleanField): Indicates whether the friendship is confirmed.
    """
    user = models.ForeignKey(
        User,
        related_name='friendships',
        on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        User,
        related_name='friends',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        """
        Meta options for the Friendship model.

        Attributes:
            unique_together (tuple): Ensures that each pair of user and friend is unique.
            indexes (list): List of indexes for the model.
        """
        unique_together = ('user', 'friend')
        indexes = [
            models.Index(fields=['user', 'friend']),
        ]

    def __str__(self):
        """
        Returns a string representation of the Friendship instance.

        Returns:
            str: A string indicating the usernames of the user and their friend.
        """
        return f"{self.user.username} is friends with {self.friend.username}"

    def clean(self):
        """
        Validates the Friendship instance.

        Raises:
            ValidationError: If the user is trying to be friends with themselves.
        """
        if self.user == self.friend:
            raise ValidationError("A user cannot be friends with themselves.")

        # Prevent duplicate friendships in reverse order
        if Friendship.objects.filter(
            Q(user=self.friend, friend=self.user) | Q(
                user=self.user, friend=self.friend)
        ).exists():
            raise ValidationError("This friendship already exists.")

    def save(self, *args, **kwargs):
        """
        Saves the Friendship instance and ensures reciprocal friendship.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.clean()
        super().save(*args, **kwargs)

        if self.confirmed:
            reciprocal, created = Friendship.objects.get_or_create(
                user=self.friend,
                friend=self.user,
                defaults={'confirmed': True}
            )
            if not created and not reciprocal.confirmed:
                Friendship.objects.filter(id=reciprocal.id).update(confirmed=True)

