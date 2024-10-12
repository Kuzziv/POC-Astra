# CMS_backend/CMS/api.py

from ninja import NinjaAPI
from CMS.models import User, Character, ParentPhone, Race, Religion
from CMS.schemas import (
    UserSchema,
    CharacterSchema,
    ParentPhoneSchema,
    RaceSchema,
    ReligionSchema,
    TokenSchema,
    RegisterSchema,
    LoginSchema,
)
from django.shortcuts import get_object_or_404
from typing import List
import uuid
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.errors import HttpError
#from django.contrib.auth.hashers import check_password


app = NinjaAPI()

### USER LOGIN ENDPOINTS ###

# Login endpoint to authenticate a user and return JWT tokens
@app.post("/login/", response={200: TokenSchema, 401: dict})
def login(request, data: LoginSchema):
    # Manually fetch the user from the custom User model
    user = get_object_or_404(User, username=data.username)
    
    # Check if the password is correct using Django's check_password function
    #if not check_password(data.password, user.password):
    if data.password != user.password:
        # If password is incorrect, raise a 401 error
        raise HttpError(401, "Invalid username or password")
    
    # Generate JWT tokens for the authenticated user
    refresh = RefreshToken.for_user(user)
    
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

# A protected endpoint that requires a valid JWT
@app.get("/protected/", auth=JWTAuth())
def protected(request):
    return {"message": f"Hello {request.auth['username']}, you are authenticated!"}

# Create a new user
@app.post("/register/", response={200: TokenSchema})
def register_user(request, data: RegisterSchema):
    # Create the user with a hashed password
    user = User.objects.create(
        username=data.username,
        email=data.email,
        password=(data.password)  # Hash the password before saving
    )
    
    # Generate the JWT tokens for the newly created user
    refresh = RefreshToken.for_user(user)
    
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

### USER ENDPOINTS ###


# Get all users
@app.get("/users/", response=List[UserSchema])
def list_users(request):
    users = User.objects.all()
    return users


# Get a specific user by ID
@app.get("/user/{user_id}", response=UserSchema)
def get_user(request, user_id: uuid.UUID):
    user = get_object_or_404(User, id=user_id)
    return user

# Get the current user's information
@app.get("/user/", response=UserSchema, auth=JWTAuth())
def get_user_info(request):
    # The user is available via `request.auth` when using JWTAuth
    print("Request: ", request)  # Check what's being received
    print("Headers: ", request.headers.get('Authorization'))  # Check what's being received
    print("Auth object: ", request.auth)  # Check if user info is being set
    user = request.auth
    if user:
        return {
            "username": user.username,
            "email": user.email,
        }
    return {"detail": "User not found"}, 404

# Create a new user
@app.post("/user/", response=UserSchema)
def create_user(request, data: UserSchema):
    user = User.objects.create(**data.dict())
    return user


# Update an existing user by ID
@app.put("/user/{user_id}", response=UserSchema)
def update_user(request, user_id: uuid.UUID, data: UserSchema):
    user = get_object_or_404(User, id=user_id)
    for attr, value in data.dict().items():
        setattr(user, attr, value)
    user.save()
    return user


# Delete a user by ID
@app.delete("/user/{user_id}", response={204: None})
def delete_user(request, user_id: uuid.UUID):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return 204, None


### CHARACTER ENDPOINTS ###


# Get all characters for a user
@app.get("/user/{user_id}/characters/", response=List[CharacterSchema])
def list_characters_for_user(request, user_id: uuid.UUID):
    user = get_object_or_404(User, id=user_id)
    characters = user.characters.all()
    return characters


# Get a specific character by ID
@app.get("/characters/{character_id}", response=CharacterSchema)
def get_character(request, character_id: uuid.UUID):
    character = get_object_or_404(Character, id=character_id)
    return character


# Create a new character
@app.post("/characters/", response=CharacterSchema)
def create_character(request, data: CharacterSchema):
    character = Character.objects.create(**data.dict())
    return character


# Update an existing character by ID
@app.put("/characters/{character_id}", response=CharacterSchema)
def update_character(request, character_id: uuid.UUID, data: CharacterSchema):
    character = get_object_or_404(Character, id=character_id)
    for attr, value in data.dict().items():
        setattr(character, attr, value)
    character.save()
    return character


# Delete a character by ID
@app.delete("/characters/{character_id}", response={204: None})
def delete_character(request, character_id: uuid.UUID):
    character = get_object_or_404(Character, id=character_id)
    character.delete()
    return 204, None


### PARENT PHONE ENDPOINTS ###


# Get all parent phone numbers for a specific user
@app.get("/users/{user_id}/parent-phones/", response=List[ParentPhoneSchema])
def list_parent_phones(request, user_id: uuid.UUID):
    user = get_object_or_404(User, id=user_id)
    parent_phones = user.parent_phones.all()
    return parent_phones


# Add a new parent phone number for a user
@app.post("/users/{user_id}/parent-phones/", response=ParentPhoneSchema)
def create_parent_phone(request, user_id: uuid.UUID, data: ParentPhoneSchema):
    user = get_object_or_404(User, id=user_id)
    parent_phone = ParentPhone.objects.create(user=user, **data.dict())
    return parent_phone


# Delete a parent phone by ID
@app.delete("/parent-phones/{phone_id}", response={204: None})
def delete_parent_phone(request, phone_id: uuid.UUID):
    phone = get_object_or_404(ParentPhone, id=phone_id)
    phone.delete()
    return 204, None


### RACE ENDPOINTS ###


# Get all available races
@app.get("/races/", response=List[RaceSchema])
def list_races(request):
    races = Race.objects.all()
    return races


### RELIGION ENDPOINTS ###


# Get all available religions
@app.get("/religions/", response=List[ReligionSchema])
def list_religions(request):
    religions = Religion.objects.all()
    return religions
