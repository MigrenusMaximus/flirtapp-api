import base64
import json

from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web_api import handlers
from web_api.models import User

ERR_MISSING_DATA = {
    'error': 'Missing data'
}


# Create your views here.

@csrf_exempt
def register(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'gender' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.register(
        data['imei'],
        data['gender']
    ))


@csrf_exempt
def authenticate(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'fcm_id' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.authenticate(
        data['imei'],
        data['imei_hash'],
        data['fcm_id']
    ))


@csrf_exempt
def update_fcm_id(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'fcm_id' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.update_fcm_id(
        data['imei'],
        data['imei_hash'],
        data['fcm_id']
    ))


@csrf_exempt
def upload_photo(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'photo' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    # user = User.objects.get(imei=data['imei'])
    # if user.imei_hash.split('$')[-1:][0] != data['imei_hash']:
    #     return JsonResponse({
    #         'error': 'Bad NaCl'
    #     })
    #
    # # requests.post
    #
    # photo_data = base64.b64decode(data['photo'])
    # user.photo = ContentFile(photo_data, 'selfie.jpg')
    # user.save()

    return JsonResponse(handlers.upload_photo(
        data['imei'],
        data['imei_hash'],
        data['photo']
    ))


@csrf_exempt
def login(request):
    data = json.loads(request.body.decode('utf-8', 'ignore'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'place_id' not in data or \
                    'name' not in data or \
                    'type' not in data or \
                    'latitude' not in data or \
                    'longitude' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.login(
        data['imei'],
        data['imei_hash'],
        data['place_id'],
        data['name'],
        data['type'],
        data['latitude'],
        data['longitude']
    ))


@csrf_exempt
def select_likes(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'liked_user_imeis' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.select_likes(
        data['imei'],
        data['imei_hash'],
        data['liked_user_imeis']
    ))


@csrf_exempt
def update_users(request):
    data = json.loads(request.body.decode('utf-8', 'ignore'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'place_id' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.update_users(
        data['imei'],
        data['imei_hash'],
        data['place_id']
    ))


@csrf_exempt
def get_matches(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.get_matches(
        data['imei'],
        data['imei_hash']
    ))


@csrf_exempt
def send_message(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'recipient_imei' not in data or \
                    'message_id' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.send_message(
        data['imei'],
        data['imei_hash'],
        data['recipient_imei'],
        data['message_id']
    ))


@csrf_exempt
def get_messages(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.get_messages(
        data['imei'],
        data['imei_hash']
    ))


@csrf_exempt
def logout(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.logout(
        data['imei'],
        data['imei_hash']
    ))


@csrf_exempt
def get_location_info(request):
    data = json.loads(request.body.decode('utf-8'))
    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'latitude' not in data or \
                    'longitude' not in data or \
                    'type' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.get_location_info(
        data['imei'],
        data['imei_hash'],
        data['latitude'],
        data['longitude'],
        data['type']
    ))


@csrf_exempt
def get_user_counts(request):
    data = json.loads(request.body.decode('utf-8'))

    if 'imei' not in data or \
                    'imei_hash' not in data or \
                    'place_ids' not in data:
        return JsonResponse(ERR_MISSING_DATA)

    return JsonResponse(handlers.get_user_counts(
        data['imei'],
        data['imei_hash'],
        data['place_ids']
    ))

# @csrf_exempt
# def get_user(request):
#     data = json.loads(request.body.decode('utf-8'))
#     user = User.objects.get(imei=data['imei'])
#     # if there is no user with the supplied id
#     # we create a new one
#     if user is None:
#         if data['gender' not in data:
#             return JsonResponse({
#                 'error': 'Missing data'
#             })
#         user = User.objects.create(
#             imei=data['imei'],
#             gender=data['gender']
#         )
#         user.save()
#         return JsonResponse(user.get_persistent_data_dict())
#
#     # if we get a heartbeat request,
#     # we only send back the messages
#     if data['heartbeat'] is not None:
#         return JsonResponse(user.get_messages())
#
#     # if there is a place id we get the place
#     # or add it if we have to
#     if data['place_id'] is not None:
#         place = Place.objects.get(place_id=data['place_id'])
#         if place is None:
#             if data['name' not in data or \
#                             data['type' not in data or \
#                             data['latitude' not in data or \
#                             data['longitude' not in data:
#                 return JsonResponse({
#                     'error': 'Missing data'
#                 })
#             place = Place.objects.create(
#                 place_id=data['place_id'],
#                 name=data['name'],
#                 type=data['type'],
#                 latitude=data['latitude'],
#                 longitude=data['longitude'],
#             )
#
#         place.add_user(user)
#         place.save()
#         return HttpResponse('OK')
#
#     # if there is an imei and a picture
#     # we save the photo and wait for a list
#     # of liked users
#     if len(request.FILES) != 0 and data['place_id'] is not None:
#         user.photo = request.FILES['photo']
#         user.save()
#         return JsonResponse(Place.objects.get(place_id=data['place_id']).get_all_data_dict())
#
#     # if there is a list of liked users
#     # we add them to the database and check
#     # if there are any matches
#     if data['liked_users'] is not None:
#         for imei in data['liked_users']:
#             user.liked_users.add(User.objects.get(imei=imei))
#         user.save()
#         return JsonResponse()
#
#     return HttpResponse("OK")
#
#
# @csrf_exempt
# def get_place(request):
#     data = json.loads(request.body.decode('utf-8'))
#     return JsonResponse(Place.objects.get(place_id=data['place_id']).get_all_data_dict())
