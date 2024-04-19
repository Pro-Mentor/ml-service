import logging
import joblib
import pickle

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import CountVectorizer

from skills.models import Category, Skill, Job, JobGuide
from skills.serializers import CategorySerializer, SkillSerializer, JobSerializer, SkillUploadSerializer
from .utils import TextPreprocessor, ListMethods

# get the logger
logger = logging.getLogger(__name__)

cv = joblib.load('model/vectorizer-2.pkl')
model = joblib.load('model/classifier-2.pkl')
# train = open('train', 'rb')
# Load the training data (if needed)
# with open('train', 'rb') as train_file:
#     x_train = pickle.load(train_file)

# cv.fit(x_train)

@csrf_exempt
def category_list(request):
    
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    
@csrf_exempt
def category_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    
@csrf_exempt
def skill_list(request):
    
    if request.method == 'GET':
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

@csrf_exempt
def skill_upload(request):
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        skills_to_save = []

        if isinstance(data.get('value'), list):
            existing_skills = Skill.objects.filter(value__in=data['value'], category_id=data.get('category_id'))
            existing_skill_values = set(skill.value for skill in existing_skills)
            
            for value in data['value']:
                if value not in existing_skill_values:
                    skills_to_save.append({'value': value, 'category_id': data.get('category_id')})

            serializer = SkillSerializer(data=skills_to_save, many=True)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201, safe=False)
            return JsonResponse(serializer.errors, status=400)
        
        return JsonResponse({'error': 'Invalid request body'}, status=400)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    
@csrf_exempt
def skill_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        skill = Skill.objects.get(pk=pk)
    except Skill.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SkillSerializer(skill, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        skill.delete()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
      
@csrf_exempt
def request_path(request):
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        skills = data.get('skills')
        preprocessed_skills = TextPreprocessor.preprocess_text(skills)
        sentence_trans = cv.transform([preprocessed_skills])
        prediction = model.predict(sentence_trans)

        job = Job.objects.filter(value = prediction[0])

        serializer = JobSerializer(job, many=True)
        guides = serializer.data[0]['job']

        skillList = skills.split(',') if skills else []

        careerGuide = []

        for guide in guides:
            if ListMethods.check_skill_in_array(skillList, guide['skills']):
                careerGuide.append({
                    "id": guide["id"],
                    "value": guide["value"],
                    "needToImprove": False
                })
            else:
                careerGuide.append({
                    "id": guide["id"],
                    "value": guide["value"],
                    "needToImprove": True
                })

        return JsonResponse({
            "job": prediction[0],
            "guides": careerGuide
        }, safe=False)
    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
