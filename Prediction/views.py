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
from .models import Task
from .serializers import PaiementSerializer
from .models import Paiement
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def object_detection_view(request):
    model_path = '/home/wecode/Rendu/G-paie/Prozect/MachineLearning/Project/APIProjectFolder/Prediction/last.pt'
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
        if score>=0.8:
            detected_objects.append({
                'class_id': int(class_id),
                'score': score,
                'bbox': [int(x1), int(y1), int(x2), int(y2)]
            })
        # detected_objects.append(result)
    return Response(detected_objects)
# Create your views here.
@api_view(['GET'])
def taskList(request,pk):
    tasks = Task.objects.get(id=pk)
    print(tasks)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)

# @api_view(['POST'])
# def add_items(request):
#     item = TaskSerializer(data=request.data)
 
#     # validating for already existing data
#     if Task.objects.filter(**request.data).exists():
#         raise serializers.ValidationError('This data already exists')
 
#     if item.is_valid():
#         item.save()
#         return Response(item.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
# @api_view(['GET'])
# def taskList(request,pk):
#     tasks = Paiement.objects.get()
#     print(tasks)
#     serializer = PaiementSerializer(tasks, many=False)
#     return Response(serializer.data)


@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = Paiement.objects.filter(**request.query_params.dict())
    else:
        items = Paiement.objects.all()
 
    # if there is something in items else raise error
    if items:
        serializer = PaiementSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status="status.HTTP_404_NOT_FOUND")
    
@api_view(['POST'])
def add_items(request):
    item = PaiementSerializer(data=request.data)
 
    # validating for already existing data
    if Paiement.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_items(request, pk):
    item = Paiement.objects.get(pk=pk)
    data = PaiementSerializer(instance=item, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Paiement, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

