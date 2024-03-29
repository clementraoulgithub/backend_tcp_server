"""User controller"""

from typing import Annotated

from fastapi import APIRouter, File
from fastapi.responses import StreamingResponse
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.models.models import (
    UserIn_Pydantic,
    UserInCreation_Pydantic,
    UserInPicture_Pydantic,
    Users,
)

router = APIRouter()


@router.get(
    "/user/{username}",
    response_model=UserInPicture_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str, password: str):
    """
    Get user by username and password

    Args:
        username (str): username of the user
        password (str): password of the user

    Returns:
        UserInPicture_Pydantic: user
    """
    return await UserInPicture_Pydantic.from_queryset_single(
        Users.get(username=username, password=password)
    )


@router.get(
    "/users/username",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_users_username():
    """
    Get all users username

    Returns:
        Users: users
    """
    users = await Users.all()
    return [user.username for user in users]


@router.get(
    "/user/{username}/picture",
    response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user_avatar(username: str):
    """
    Get user avatar by username

    Args:
        username (str): username of the user

    Returns:
        StreamingResponse: user avatar
    """
    user = await UserIn_Pydantic.from_queryset_single(Users.get(username=username))

    return StreamingResponse(
        iter([user.picture]),
        media_type="application/octet-stream",
    )


@router.get(
    "/user/{username}/creation-date",
    response_model=UserInPicture_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_creation_date(username: str):
    """
    Get user creation date by username

    Args:
        username (str): username of the user

    Returns:
        Users: user
    """
    return await UserInPicture_Pydantic.from_queryset_single(
        Users.get(username=username)
    )


@router.post("/register", responses={404: {"model": HTTPNotFoundError}})
async def create_user(user: UserInCreation_Pydantic):
    """
    Create user

    Args:
        user (UserInCreation_Pydantic): user to create
    """
    await Users.create(
        **user.dict(exclude_unset=True, exclude_defaults=True, exclude_none=True)
    )


@router.put("/user/{user_name}", responses={404: {"model": HTTPNotFoundError}})
async def create_file(user_name: str, file: Annotated[bytes, File()]):
    """
    Update user avatar

    Args:
        user_name (str): username of the user
        file (Annotated[bytes, File): avatar of the user
    """
    await Users.filter(username=user_name).update(picture=file)


@router.patch("/user/{user_name}", responses={404: {"model": HTTPNotFoundError}})
async def update_user_connection_status(user_name: str, is_connected: bool):
    """
    Update user connection status

    Args:
        user_name (str): username of the user
        is_connected (bool): connection status of the user
    """
    await Users.filter(username=user_name).update(is_connected=is_connected)


@router.patch(
    "/user/{user_name}/description", responses={404: {"model": HTTPNotFoundError}}
)
async def update_user_description(user_name: str, description: str):
    """
    Update user description

    Args:
        user_name (str): username of the user
        description (str): description of the user
    """
    await Users.filter(username=user_name).update(description=description)
