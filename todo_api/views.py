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
            'note': request.data.get('note') or todo_instance.note,
            'due_date': request.data.get('due_date') or todo_instance.due_date,
            'is_complete': request.data.get('is_complete') or todo_instance.is_complete,
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

    def _get_filters(self, request) :
        filter = {
            'user': request.user.id
        }

        # Filter texts
        if 'note' in request.query_params:
            filter['note__icontains'] = request.query_parameter['note']

        # Filter due_dates
        if 'start_date' in request.query_params and 'end_date' in request.query_params:
            filter['due_date__range'] = (request.query_params['start_date'], request.query_params['end_date'])
        elif 'start_date' in request.query_params:
            filter['due_date__gte'] = request.query_params['start_date']
        elif 'end_date' in request.query_params:
            filter['due_date__lte'] = request.query_params['end_date']

        # Filter completed todos
        if 'is_complete' in request.query_params:
            filter['is_complete'] = request.query_params['is_complete']

        return filter

    def get(self, request, *args, **kwargs):
        data_filters = self._get_filters(request)
        data = Todo.objects.filter(**data_filters)
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
