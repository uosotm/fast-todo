from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result

import api.models.task as task_model
import api.schemas.task as task_schema


def get_task(db: Session, task_id: int) -> task_model.Task | None:
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    return result.scalars().first()


# TODO: この返り値はモデルの型を使うことは出来ないのか？
def get_tasks_with_done(db: Session) -> list[tuple[int, str, bool]]:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    return result.all()


def create_task(db: Session, task_create: task_schema.TaskCreate) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    db.commit()
    # Fill object with remaining data like task id
    db.refresh(task)
    return task


def update_task(
    db: Session, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()