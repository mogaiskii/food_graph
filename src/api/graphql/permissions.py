from strawberry import BasePermission
from strawberry.types import Info

from api.graphql.utils import get_user
from core.interactors.users.exceptions import WrongAuthToken


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source, info: Info, **kwargs) -> bool:
        try:
            await get_user(info.context['db'], info.context['request'])
        except WrongAuthToken:
            return False
        return True
