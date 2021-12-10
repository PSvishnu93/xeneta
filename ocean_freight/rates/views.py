from rates.services import get_day_average
from rates.serializers import RateRequestSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(('GET', ))
def average(request):
    serializer = RateRequestSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    data = get_day_average(serializer.data) 
    return Response(data=data, status=status.HTTP_200_OK)
