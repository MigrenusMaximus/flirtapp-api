import base64
import json

# import cv2
import requests
import time
from FlirtAPI.settings import PLACES_API_KEY, PLACES_SEARCH_RADIUS, FIREBASE_SEND_URL, FIREBASE_API_KEY, BASE_DIR
from django.contrib.auth import hashers
from django.core.files.base import ContentFile
from web_api.models import User, Place, Message


def register(imei, gender):
    #if User.objects.filter(imei=imei).exists():
    #    return {
    #        'error': 'User already exists'
    #    }

    imei_hash = hashers.make_password(
        imei,
        salt='this_is_my_secret_salt_dont_show_it_to_anyone',
        hasher='pbkdf2_sha256'
    )

    user = None
    if User.objects.filter(imei=imei):
        user = User.objects.get(imei=imei)
        user.gender = gender
        user.imei_hash = imei_hash
    else:
        user, success = User.objects.create(
            imei=imei,
            imei_hash=imei_hash,
            gender=gender
        )
        
    user.save()

    final_hash = user.imei_hash.split('$')[-1:][0]

    return {
        'imei_hash': final_hash
    }


def authenticate(imei, imei_hash, fcm_id):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    user.is_authenticated = True
    user.fcm_id = fcm_id
    user.save()

    return {
        'success': 'Authentication successful'
    }


def update_fcm_id(imei, imei_hash, fcm_id):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    user.fcm_id = fcm_id
    user.save()

    return {
        'success': 'FCM token updated'
    }


def login(imei, imei_hash, place_id, name, place_type, latitude, longitude):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    # if the place doesn't exist yet,
    # we will create it
    if not Place.objects.filter(place_id=place_id).exists():
        place = Place.objects.create(
            place_id=place_id,
            name=name,
            type=place_type,
            latitude=latitude,
            longitude=longitude
        )
    else:
        place = Place.objects.get(place_id=place_id)

    place.add_user(user)
    place.save()

    # user_imeis = list(place.current_users.exclude(imei=imei).values_list('imei', flat=True))
    # user_photo_urls = []
    # user_genders = []

    user.login_time = int(time.time())
    # user.last_check = int(time.time())
    user.save()

    return {
        'success': 'Login successful'
    }

    # for imei_iter in user_imeis:
    #     # if imei_iter == imei:
    #     #     continue
    #     curr_user = User.objects.get(imei=imei_iter)
    #     user_photo_urls.append('/'.join(curr_user.photo.url.split('/')[-3:]))
    #     user_genders.append(curr_user.gender)

    # return {
    #     'current_users': user_imeis,
    #     'user_photo_urls': user_photo_urls,
    #     'user_genders': user_genders
    # }


def get_messages(imei, imei_hash):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    messages = list(Message.objects.values_list('message_text', flat=True))
    
    return {
        'messages': messages
    }


def send_message(imei, imei_hash, recipient_imei, message_id):
    # if the sender doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    from_user = User.objects.get(imei=imei)

    # if the sender's hash doesn't match
    if from_user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not from_user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    # if the recipient doesn't exist
    if not User.objects.filter(imei=recipient_imei).exists():
        return {
            'error': 'Recipient does not exist'
        }

    to_user = User.objects.get(imei=recipient_imei)

    request_data = {
        'to': to_user.fcm_id,
        'data': {
            'sender_imei': from_user.imei,
            'sender_photo_url': '/'.join(from_user.photo.url.split('/')[-3:]),
            'message_num': str(message_id)
        }
    }

    print(json.dumps(request_data))

    request_headers = {
        'Authorization': 'key=' + FIREBASE_API_KEY
    }

    response = requests.post(FIREBASE_SEND_URL, json=request_data, headers=request_headers)

    print(response.text)

    # # we delete all previous messages,
    # # because only the last one is important
    # messages = Message.objects.filter(to_user=to_user, from_user=from_user)
    # for message in messages:
    #     message.delete()
    #
    # Message.objects.create(
    #     message_id=message_id,
    #     from_user=from_user,
    #     to_user=to_user
    # ).save()

    return {
        'success': 'Message sent successfully'
    }


def get_matches(imei, imei_hash):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    matches = user.get_matches()
    try:
        matches.remove(user.imei)
    except ValueError as e:
        print('', end='')

    photo_urls = []
    for imei_iter in matches:
        # if imei_iter == imei:
        #     continue
        curr_user = User.objects.get(imei=imei_iter)
        photo_urls.append('/'.join(curr_user.photo.url.split('/')[-3:]))

    return {
        'matches': matches,
        'match_photo_urls': photo_urls
    }


def logout(imei, imei_hash):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    places = Place.objects.filter(current_users__imei__contains=user.imei)
    # if place is None, that means
    # the user isn't registered anywhere
    if places is None or places == []:
        return {
            'error': 'User is already logged out'
        }

    # we remove the user from all
    # places he's been registered in
    # note: there shouldn't be more than one place
    for place in places:
        place.current_users.remove(user)
        place.save()

    user.is_authenticated = False
    user.save()

    return {
        'success': 'Successfully logged out'
    }


def upload_photo(imei, imei_hash, photo):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    photo_data = base64.b64decode(photo)
    user.photo = ContentFile(photo_data, 'selfie.jpg')
    user.save()

    photo_url = '/'.join(user.photo.url.split('/')[-3:])
    # print(photo_url)
    # print(user.photo.url)

#    image_path = BASE_DIR.replace('\\', '/') + '/' + photo_url
#    cascade_path = BASE_DIR.replace('\\', '/') + '/web_api/cv2_cascades/haarcascade_frontalface_default.xml'
#    face_cascade = cv2.CascadeClassifier(cascade_path)
#    image = cv2.imread(image_path)
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    faces = face_cascade.detectMultiScale(
#        gray,
#        scaleFactor=1.4,
#        minNeighbors=3,
#        minSize=(30, 30),
#        flags=cv2.CASCADE_SCALE_IMAGE
#    )
#    
#    if len(faces) < 1:
#        return {
#            'error': 'Face not detected. Please try again.'
#        }

    return {
        'photo_url': photo_url
    }


def select_likes(imei, imei_hash, liked_user_imeis):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    user.liked_users.clear()

    for liked_imei in liked_user_imeis:
        if User.objects.filter(imei=liked_imei).exists():
            liked_user = User.objects.get(imei=liked_imei)
            user.liked_users.add(liked_user)

            if liked_user.liked_users.filter(imei=imei).exists():
                request_data = {
                    'registration_ids': [liked_user.fcm_id, user.fcm_id],
                }

                print(json.dumps(request_data))

                request_headers = {
                    'Authorization': 'key=' + FIREBASE_API_KEY
                }

                response = requests.post(FIREBASE_SEND_URL, json=request_data, headers=request_headers)

                print(response.text)

    user.save()

    return {
        'success': 'Successfully selected liked users'
    }


def update_users(imei, imei_hash, place_id):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    # if the place doesn't exist
    if not Place.objects.filter(place_id=place_id):
        return {
            'error': 'Place does not exist'
        }

    place = Place.objects.get(place_id=place_id)

    if imei not in list(place.current_users.values_list('imei', flat=True)):
        return {
            'error': 'User not at location'
        }

    user_imeis = list(place.current_users.exclude(imei=imei).values_list('imei', flat=True))
    user_photo_urls = []
    user_genders = []
    new_users = []

    for imei_iter in user_imeis:
        # if imei_iter == imei:
        #     continue
        curr_user = User.objects.get(imei=imei_iter)
        if curr_user.photo.url is None:
            continue
        user_photo_urls.append('/'.join(curr_user.photo.url.split('/')[-3:]))
        user_genders.append(curr_user.gender)
        if curr_user.login_time > user.last_check:
            new_users.append(True)
        else:
            new_users.append(False)

    user.last_check = int(time.time())
    user.save()

    return {
        'current_users': user_imeis,
        'user_photo_urls': user_photo_urls,
        'user_genders': user_genders,
        'new_users': new_users
    }


# TODO: Merge get_user_counts and get_location_info into one request
def get_location_info(imei, imei_hash, latitude, longitude, place_type):
    PLACE_TYPES = [
        'bar',
        'cafe',
        'casino',
        'gym',
        'hospital',
        'library',
        'night_club',
        'restaurant',
        'school',
        'university',
    ]

    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    request_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + \
                  str(latitude) + ',' + str(longitude) + \
                  '&radius=' + str(PLACES_SEARCH_RADIUS) + \
                  '&key=' + str(PLACES_API_KEY)
    # '&type=' + str(place_type) +

    response = requests.get(request_url)

    response_dict = dict(response.json())
    response_dict['results'] = [result for result in response_dict['results'] if any(x in result['types'] for x in PLACE_TYPES)]
    
    place_ids = []    
    
#    for key in response_dict['results']:
#        if not any(x in response_dict['results'][key]['types'] for x in PLACE_TYPES):
#            del response_dict['results'][key]
#            continue
#        place_ids.append(response_dict['results'][key]['place_id'])
    
    for result in response_dict['results']:
        place_ids.append(result['place_id'])

    user_counts = get_user_counts(imei, imei_hash, place_ids)

    response_dict.update({
        'user_counts': user_counts
    })

    return response_dict


def get_user_counts(imei, imei_hash, place_ids):
    # if the user doesn't exist
    if not User.objects.filter(imei=imei).exists():
        return {
            'error': 'User does not exist'
        }

    user = User.objects.get(imei=imei)

    # if the user's hash doesn't match
    if user.imei_hash.split('$')[-1:][0] != imei_hash:
        return {
            'error': 'Bad NaCl'
        }

    # if the user isn't authenticated
    if not user.is_authenticated:
        return {
            'error': 'Not authenticated'
        }

    places = []
    male_counts = []
    female_counts = []

    # for every user in every place supplied
    # we get a count of male and a count of
    # female users and return those values
    for place_id in place_ids:
        if not Place.objects.filter(place_id=place_id).exists():
            places.append(place_id)
            male_counts.append(0)
            female_counts.append(0)
            continue

        curr_place = Place.objects.get(place_id=place_id)

        curr_users = list(curr_place.current_users.values_list('imei', flat=True))
        male_count = 0
        female_count = 0

        for imei in curr_users:
            if not User.objects.filter(imei=imei).exists():
                continue

            user = User.objects.get(imei=imei)

            if user.gender == 'M':
                male_count += 1
            elif user.gender == 'F':
                female_count += 1
            else:
                curr_users.remove(imei)

        places.append(place_id)
        male_counts.append(male_count)
        female_counts.append(female_count)

    return {
        'place_ids': places,
        'male_counts': male_counts,
        'female_counts': female_counts
    }
