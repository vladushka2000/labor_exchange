from fastapi import Depends
from core.security import JWTBearer, decode_access_token


class UserDependencies:
    @staticmethod
    async def get_user_email(token: str = Depends(JWTBearer())) -> str:
        payload = decode_access_token(token)

        if payload is None:
            raise ValueError()

        email: str = payload.get("sub")

        if email is None:
            raise ValueError()

        return email
