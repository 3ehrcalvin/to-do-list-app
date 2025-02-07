from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

# Create your views here.

class TodoDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        try:
            return Todo.objects.get(id=todo_id, user=user_id)
        except Todo.DoesNotExist:
            return None
        
    def get(self, request, *args, **kwargs):
        todo_instance = self.get_object(kwargs['todo_id'], request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Record does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        todo_instance = self.get_object(kwargs['todo_id'], request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Record does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'note': request.data.get('note'),
            'due_date': request.data.get('due_date'),
            'is_complete': request.data.get('is_complete'),
            'user': request.user.id
        }

        serializer = TodoSerializer(todo_instance, data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        todo_instance = self.get_object(kwargs['todo_id'], request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Record does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        todo_instance.delete()
        return Response(
            {"res": "Record has been deleted"},
            status=status.HTTP_200_OK
        )


class TodoApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'note': request.data.get('note'),
            'due_date': request.data.get('due_date'),
            'is_complete': False,
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
