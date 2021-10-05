from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from api.models import Autor, Genero, Libro
from api.serializer import *

# Create your views here.

@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    data = JSONParser().parse(request)
    try:
        username = data['username']
        pwd = data['password']
    except:
        return JsonResponse({
            'message':'Username o password required',
            'success':'error'
            }, safe=False)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({
            'message':'Usuario no existe',
            'success':'error'
            }, safe=False)
    pwd_valid = check_password(pwd, user.password)
    if not pwd_valid:
        return JsonResponse({
            'message':'Contraseña invalida',
            'success':'error'
            }, safe=False)
    token, created = Token.objects.get_or_create(user=user)
    # print(token.key)
    return JsonResponse({
        'token':token.key,
        'success':'ok'
        }, safe=False)

@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    data = JSONParser().parse(request)
    user_serializer = CreateUserSerializer(data=data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse({
            'success':'ok',
            'data':user_serializer.data
        }, safe=False, status=201)
    return JsonResponse({
            'success':'error',
            'message':user_serializer.errors
        }, safe=False, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return JsonResponse({
        'message': 'Se ha cerrado sesion exitosamente',
        'success':'ok'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_books(request):
    libros = Libro.objects.all()
    libros_serializer = LibroSerializer(libros, many=True)

    return JsonResponse({
        'success':'ok',
        'data':libros_serializer.data
    }, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_generos(request):
    generos = Genero.objects.all()
    generos_serializer = GeneroSerializer(generos, many=True)
    return JsonResponse({
        'success':'ok',
        'data':generos_serializer.data
    }, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_autores(request):
    autores = Autor.objects.all()
    autores_serializer = AutorSerializer(autores, many=True)
    return JsonResponse({
        'success':'ok',
        'data':autores_serializer.data
    }, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_libro(request):
    data = JSONParser().parse(request)
    libro_serializer = LibroSerializerCreate(data=data)
    if libro_serializer.is_valid():
        libro_serializer.save()
        return JsonResponse({
            'success':'ok',
            'data':libro_serializer.data
        }, safe=False, status=201)
    return JsonResponse({
            'success':'error',
            'message':libro_serializer.errors
        }, safe=False, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    titulo = request.query_params.get('titulo')
    autor = request.query_params.get('autor')
    genero = request.query_params.get('genero')
    if titulo:
        libros = Libro.objects.filter(titulo__contains=titulo)
    elif autor:
        libros = Libro.objects.filter(autor__nombre__contains=autor)
    elif genero:
        libros = Libro.objects.filter(genero__nombre__contains=genero)
    libros_serializer = LibroSerializer(libros, many=True)

    return JsonResponse({
        'success':'ok',
        'data':libros_serializer.data
    }, safe=False)