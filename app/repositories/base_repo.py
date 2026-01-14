from typing import (
    Sequence,
    Generic,
    TypeVar,
    Type,
)

from fastapi import HTTPException
from starlette import status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepo(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model


    async def get_all(
        self,
        session: AsyncSession,
    ) -> Sequence[ModelType]:
        try:
            stmt = await session.execute(
                select(self.model)
                .order_by(self.model.id)
            )
            result = stmt.scalars().all()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not found",
                )
            return result

        except Exception as e:
            raise e


    async def get_by_id(
            self,
            session: AsyncSession,
            model_id: int,
    ) -> ModelType:
        try:
            stmt = await session.execute(
                select(self.model)
                .filter_by(id=model_id)
            )
            result = stmt.scalar_one_or_none()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ID '{model_id}' not found",
                )
            return result
        except Exception as e:
            raise e


    async def create(
            self,
            session: AsyncSession,
            create_schema: CreateSchemaType,
    ) -> ModelType:
        try:
            create_data = create_schema.model_dump()
            model_obj = self.model(**create_data)
            session.add(model_obj)
            await session.commit()
            await session.refresh(model_obj)
            return model_obj

        except Exception as e:
            raise e


    async def update(
            self,
            session: AsyncSession,
            update_schema: UpdateSchemaType,
            model_id: int,
    ) -> ModelType:
        try:
            model_obj = await self.get_by_id(
                session=session,
                model_id=model_id,
            )
            if not model_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{ModelType.__name__} with ID {model_id} not found",
                )
            update_data = update_schema.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(model_obj, field, value)
            session.add(model_obj)
            await session.commit()
            await session.refresh(model_obj)
            return model_obj

        except Exception as e:
            raise e


    async def delete(
            self,
            session: AsyncSession,
            model_id: int,
    ):
        try:
            result = await self.get_by_id(
                session=session,
                model_id=int(model_id),
            )

            await session.delete(result)
            await session.commit()
            return HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )

        except Exception as e:
            raise e