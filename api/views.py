from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Employee, Store, Visit
from .serializers import StoreSerializer, VisitSerializer


class PhoneAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        if not auth:
            raise AuthenticationFailed('No authentication credentials provided.')

        try:
            auth_type, phone_number = auth.split(' ')
            if auth_type != 'Phone':
                raise AuthenticationFailed('Invalid authentication type.')

            employee = Employee.objects.get(phone_number=phone_number)
        except (ValueError, Employee.DoesNotExist):
            raise AuthenticationFailed('Invalid phone number.')

        return employee, None


class StoreListView(APIView):
    authentication_classes = [PhoneAuthentication]

    def get(self, request):
        employee = request.user
        stores = employee.stores.all()

        if not stores.exists():
            return Response({"detail": "No stores found for this employee."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


class VisitCreateView(APIView):
    authentication_classes = [PhoneAuthentication]

    def post(self, request):
        employee = request.user
        store_id = request.data.get('store_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        try:
            store = Store.objects.get(id=store_id, employee=employee)
        except Store.DoesNotExist:
            return Response({"detail": "Invalid store for this employee."}, status=status.HTTP_400_BAD_REQUEST)

        visit = Visit.objects.create(
            store=store,
            employee=employee,
            latitude=latitude,
            longitude=longitude
        )

        serializer = VisitSerializer(visit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
