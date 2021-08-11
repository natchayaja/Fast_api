from tortoise import fields, models
from tortoise.contrib import pydantic
from tortoise.contrib.pydantic import pydantic_model_creator

class Todos(models.MODEL):
    id = fields.Intfield(pk=True)
    title = fields.CharField(max_length=255)
    is_complete = fields.BooleanField(default=False)
    create_at = fields.DateTimeField(auto_now_add= True)
    modified_at = fields.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title

    
    Todos_Pydantic = pydantic_model_creator(Todos, name="Todo")
    Todos_Pydantic = pydantic_model_creator(Todos, name="TodoIn", exclude_readonly= True)
