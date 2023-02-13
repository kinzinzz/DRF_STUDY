from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CheckListSerializer, CheckSerializer
from .models import Check_list

@api_view(['GET'])
def check_list(request):
    checks = Check_list.objects.all()
    serializer = CheckListSerializer(checks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def check_detail(request, check_pk):
    check = get_object_or_404(Check_list, pk=check_pk)
    serializer = CheckSerializer(check)
    return Response(serializer.data)

@api_view(['POST'])
def create_check(request):
    serializer = CheckSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)