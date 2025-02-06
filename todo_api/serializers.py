from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "note",
            "due_date",
            "is_complete",
            "user"
        ]
