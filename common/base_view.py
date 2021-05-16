from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    def resource_deleted_response(self, message):
        return Response(
            {"detail": message},
            status=status.HTTP_200_OK,
        )

    def bad_request_response(self, message):
        # Handles Error Objects Internally by Converting them To String
        return Response(
            {"detail": str(message)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    class Meta:
        abstract = True
