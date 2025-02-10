from rest_framework import serializers
from .models import Todo
from datetime import date

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "note",
            "due_date",
            "is_complete",
            "user"
        ]

    def is_valid(self, *, raise_exception=False):
        res = super().is_valid(raise_exception=raise_exception)

        if self.initial_data['due_date'] < str(date.today()):
            self._errors['err_message'] = ["Due date cannot be in the past."]
            return False
        
        return res

