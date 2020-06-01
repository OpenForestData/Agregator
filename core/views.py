from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pyDataverse

class HelloView(APIView):
    """
    Basic view
    """
    permission_classes = ()



    def get(self, request):
        content = {'message': "Hello, is it me you're looking for?"}
        return Response(content)
