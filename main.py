from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum



app = FastAPI(
    title="Todo APP",
    description="A our Basic Todo app",
    version="1.0",

)


class Category(Enum):
    """Category for a todo"""
    PERSONAL = "personal"
    WORK = "work"


class Todo(BaseModel):
    title: str
    completed: bool
    id: int
    category: Category


todos = {
    1: Todo(title="test1", completed=True, id=1, category=Category.PERSONAL),
    2: Todo(title="Submit taxes", completed=False, id=2, category=Category.WORK),
}


@app.get('/')
def index() -> dict[str, dict[int, Todo]]:
    return {"todos": todos}


@app.get("/todos/{todo_id}")
def get_todo_by_id(todo_id: int) -> Todo:
    if todo_id not in todos:
        raise HTTPException(
            status_code=404, detail=f'ID {todo_id} does not exist')
    return todos[todo_id]


@app.get('/todos/')
def query_todo_by_completed(completed: bool | None = None) -> dict[str, list[Todo]]:
    filtered_todos = [
        todo for todo in todos.values() if todo.completed is completed]
    return {'todos': filtered_todos}


@app.post('/', tags=['todos'])
def create_todo(todo: Todo) -> dict[str, Todo]:
    if todo.id in todos:
        raise HTTPException(
            status_code=400, detail=f'ID {todo.id} already exists')

    todos[todo.id] = todo
    return {'todo': todo}


@app.put('/todos/{todo_id}')
def update_todo(todo_id, todo: Todo) -> dict[str, Todo]:
    todos[todo_id] = todo
    return {'todo': todo}


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int) -> dict[str, Todo]:
    if todo_id not in todos:
        raise HTTPException(
            status_code=404, detail=f'ID {todo_id} does not exist')

    todo = todos.pop(todo_id)
    return {'todo': todos[todo_id]}
