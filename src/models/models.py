from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    password = fields.CharField(max_length=30)
    picture = fields.BinaryField()


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
UserInPicture_Pydantic = pydantic_model_creator(
    Users, name="UserInPicture", exclude_readonly=True, exclude=["picture"]
)

class Messages(models.Model):
    message_id = fields.IntField(pk=True)
    sender = fields.CharField(max_length=30)
    message = fields.TextField()
    
Messages_Pydantic = pydantic_model_creator(Messages, name="Message")
MessagesIn_Pydantic = pydantic_model_creator(Messages, name="MessageIn", exclude_readonly=True)