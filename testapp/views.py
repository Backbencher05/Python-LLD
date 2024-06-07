from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from testapp.models import User, ShippingAddress
from testapp.serializers import UserSerializer, ShippingAddressSerializer, CreateShippingAddressSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

class UserListCreateAPIView(APIView):

    def get(self, request):
        users = User.objects.all().prefetch_related("shipping_addresses").select_related(
            "default_shipping_address"
        )
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)


    def post(self,request):
        serialized = UserSerializer(data=request.data)
        if not serialized.is_valid():
            return  Response(serialized.errors,status=400)

        serialized.save()
        return Response(serialized.data, status=201)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Let we want shipping address of paricular User or want to add
# the shipping addres to particular User
class ShippingAddressListcreateAPIView(APIView):

    serialized_class = CreateShippingAddressSerializer
    def get(self,request,user_id):
        user = get_object_or_404(ShippingAddress, pk =user_id)
        # serialized_class = CreateShippingAddressSerializer(user)
        serialized_class = ShippingAddressSerializer(user)
        return Response(serialized_class.data)

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serialized = CreateShippingAddressSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, status=400)

        shipping_address = ShippingAddress(
            street=serialized.validated_data["street"],
            city=serialized.validated_data["city"],
            state=serialized.validated_data["state"],
            zip_code=serialized.validated_data["zip_code"],
            country=serialized.validated_data["country"],
            user=user
        )

        shipping_address.save()

        return Response(ShippingAddressSerializer(
            shipping_address
        ).data, status=201)


class SetDefaultShippingAddress(APIView):

    def patch(self, request, user_id, address_id):

        user = get_object_or_404(User, pk=user_id)
        address = get_object_or_404(ShippingAddress, user_id=user_id, pk=address_id)

        user.default_shipping_address = address

        user.save()

        return Response(
            UserSerializer(User), 200
        )