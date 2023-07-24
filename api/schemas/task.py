from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str | None = Field(None, example="クリーニングを取りに行く")


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")


class TaskCreate(TaskBase):
    pass

    model_config = ConfigDict(from_attributes=True)


class TaskCreateResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
