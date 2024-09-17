from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponseRedirect
import pandas as pd
from rest_framework.decorators import api_view , permission_classes
import numpy as np
import os
from ultralytics import YOLO
import cv2
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import TaskSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def object_detection_view(request):
    model_path = '/home/wecode/Rendu/MachineLearning/django-rest-allauth/core/authentication/last.pt'
    model = YOLO(model_path)

    image_file = request.FILES.get('image')
    if not image_file:
        return Response({"error": "No image file provided"}, status=400)

    image = np.fromstring(image_file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    if image is None:
        return Response({"error": "Failed to decode image"}, status=400)

    results = model(image)[0]
    detected_objects = []

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        detected_objects.append({
            'class_id': int(class_id),
            'score': score,
            'bbox': [int(x1), int(y1), int(x2), int(y2)]
        })
        # detected_objects.append(result)

    return Response(detected_objects)
# Create your views here.

def taskList(request,pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
    