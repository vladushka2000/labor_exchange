from abstracts.unit_of_work import UnitOfWork
from core.security import create_access_token, hash_password, verify_password
from dto import LoginSchema, TokenSchema, UserSchema, UserInSchema
from repository.alchemy_orm.models import User as OrmUser


class AuthException(Exception):
    pass


async def register(
    user_data: UserInSchema,
    uow: UnitOfWork,
) -> UserSchema:
    async with uow:
        user = await uow.repository.get_by_email(user_data.email)

        if user is not None:
            raise AuthException()

        user = OrmUser(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hash_password(user_data.password),
            is_company=user_data.is_company
        )

        uow.repository.add(user)
        await uow.commit()
        await uow.repository.refresh(user)

        return UserSchema(
            id=str(user.id),
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_company=user.is_company,
            created_at=user.created_at
        )


async def login(
    login_data: LoginSchema,
    uow: UnitOfWork,
) -> TokenSchema:
    async with uow:
        user = await uow.repository.get_by_email(login_data.email)

        if user is None or not verify_password(login_data.password, user.hashed_password):
            raise AuthException()

        return TokenSchema(
            access_token=create_access_token({"sub": user.email}),
            token_type="Bearer"
        )
