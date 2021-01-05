'''Handles authentication of a user'''
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from scentsibleapi.models import ScentsibleUser



@csrf_exempt
def login_user(request):
    """Handles the authentication of a ScentsibleUser
    Method arguments: Request -- the full HTTP request object
    """

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided; can't log in the user 
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    """Handles the creation of a new ScentsibleUser for authentication
    Method arguments:
      request -- The full HTTP request object
    """

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        email=req_body['email'],
        username=req_body['username'],
        password=req_body['password']
    )

    scentsible_user = ScentsibleUser.objects.create(
        user=new_user
    )

    scentsible_user.save()


    # Use REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)
