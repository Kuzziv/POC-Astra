from ninja import ModelSchema, Schema
from CMS.models import User, Character, ParentPhone, Race, Religion


class LoginSchema(Schema):
    username: str
    password: str

class RegisterSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TokenSchema(Schema):
    access: str
    refresh: str


# CharacterSchema to serialize Character model data
class CharacterSchema(ModelSchema):
    class Meta:
        model = Character
        fields = ("id", "name", "xp")


# ParentPhoneSchema to serialize ParentPhone model data
class ParentPhoneSchema(ModelSchema):
    class Meta:
        model = ParentPhone
        fields = ("id", "phone_number", "parent_name")


# UserSchema to serialize User model data
class UserSchema(ModelSchema):
    characters: list[
        CharacterSchema
    ]  # Annotate a list of CharacterSchema to represent related characters
    parent_phones: list[
        ParentPhoneSchema
    ]  # Annotate a list of ParentPhoneSchema to represent related parent phone numbers

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "personal_phone",
            "create_time",
            "update_time",
        )  # 'characters' and 'parent_phones' handled separately

    @staticmethod
    def resolve_characters(user):
        # Custom resolution method to retrieve all related characters for the user
        return [
            CharacterSchema.from_orm(character) for character in user.characters.all()
        ]

    @staticmethod
    def resolve_parent_phones(user):
        # Custom resolution method to retrieve all related parent phones for the user
        return [ParentPhoneSchema.from_orm(phone) for phone in user.parent_phones.all()]


# RaceSchema to serialize Race model data
class RaceSchema(ModelSchema):
    class Meta:
        model = Race
        fields = ("id", "name", "description")


# ReligionSchema to serialize Religion model data
class ReligionSchema(ModelSchema):
    class Meta:
        model = Religion
        fields = ("id", "name", "description")
