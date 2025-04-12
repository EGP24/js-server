from typing import Annotated

from serpyco_rs.metadata import CustomEncoder

from src.entities.user import PresentedUser, User
from src.helpers.urls import check_image_url

ImageUrlEncoder = Annotated[str, CustomEncoder[str, str](serialize=check_image_url, deserialize=check_image_url)]


def map_user_to_presented_user(user: User) -> PresentedUser:
    return PresentedUser(
        id=user.id,
        name=user.name,
        about=user.about,
        avatar=user.avatar,
        cohort=user.cohort,
    )
