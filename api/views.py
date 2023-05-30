import json
import os

from PIL import Image
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from media.main import checkUser
from todo_drf import settings
from .serializers import UserSerializer
from rest_framework.parsers import MultiPartParser

from .models import User


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/user-list/',
        'Detail View': '/user-detail/<str:pk>/',
        'Create': '/user-create/',
        'Delete': '/user-delete/<str:pk>/',
        'Check': '/user-check/',
        'Check Image': '/user-check-img/',
    }

    return Response(api_urls)


@api_view(['GET'])
def userList(request):
    user = User.objects.all().order_by('-id')
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def userDetail(request, pk):
    tasks = User.objects.get(id=pk)
    serializer = UserSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def userDelete(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    image_src = serializer.data.get('user_finger_img')

    os.remove(f".{image_src}")

    user.delete()

    return Response('Item succsesfully delete!')


@api_view(['POST'])
@parser_classes([MultiPartParser])
def userCreate(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def userCheck(request):
    image = request.FILES["image"]

    with Image.open(image) as img:
        img.save(f"media/{image.name}")

    source, file_name = checkUser(f"./media/{image.name}")

    if file_name:
        user = User.objects.get(user_finger_img=f"images/{file_name}")
        serializer = UserSerializer(user, many=False)

        os.remove(f"./media/{image.name}")
        return JsonResponse({
            "message": "Image uploaded successfully.",
            "user": serializer.data,
            "source": source
        })
    else:
        os.remove(f"./media/{image.name}")
        return JsonResponse({
            "message": "User is not found",
        })


@api_view(['GET'])
def getCheckImage(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'check_img.BMP')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            img = f.read()
            return HttpResponse(img, content_type="image/BMP")
    else:
        return JsonResponse({"error": "Image not found."})



