from fastapi import APIRouter

from dto import LoginSchema, TokenSchema, UserSchema, UserInSchema
from repository.alchemy_orm import OrmUserRepository
from service import auth as auth_service
from unit_of_work import AlchemyOrmUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema)
async def register(user_data: UserInSchema) -> UserSchema:
    return await auth_service.register(user_data, AlchemyOrmUnitOfWork(OrmUserRepository))


@router.post("/login", response_model=TokenSchema)
async def login(login_data: LoginSchema) -> TokenSchema:
    return await auth_service.login(login_data, AlchemyOrmUnitOfWork(OrmUserRepository))
