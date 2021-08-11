from fastapi import FastAPI     # 1 , 3
from pydantic import BaseModel  #เป็นการ cover type ตามที่รับค่าเข้ามา     2
from typing import Optional
from pydantic.utils import truncate
from starlette.routing import Router
from tortoise import models     #ตัวเลือกว่าจะกรอกหรือไม่กรอกก็ได้          2
from router import coffee           # 3
#from tortoise.contrib.fastapi import register_tortoise
#from models.todo import Todos, Todos_Pydantic, TodosIn_Pydantic


#-------------------------------------Basic API ที่ยังไม่เชื่อมต่อ Database---------------------------------------------------------------------


class coffee(BaseModel) :                                              # 2
    name : str
    description : Optional[str] = None
    price : float
    star : int

coffee_db = [                                                           # 2
    {
    'name' : 'Espresso',
    'description' : 'กาแฟดำเข้มที่สุด',
    'price' : 60,
    'star' : 5
    },
    {
    'name' : 'Americano',
    'description' : 'กาแฟดำผสมน้ำเปล่า',
    'price' : 55,
    'star' : 5
   }
 ]


app = FastAPI()                                        # 1 , 2

@app.get("/")                                          # 2   เอาข้อมูลใน coffee_db มาแสดงเฉยๆ
async def root():
   return coffee_db


@app.get("/coffee/{id}")                                # 2     เอา id ที่รับมา ไปหาใน coffee_db
async def coffee_id(id :int):      
    coffee = coffee_db[id -1]                                   # -1 เพราะ list ช่องแรกเริ่มที่ 0
    return coffee

@app.post("/coffee")                                # 2     
async def create_coffee(coffee: coffee):            # (pydantic) รับ coffee เข้ามา แต่จะถูกครอบด้วย type Coffee(class) ที่เราสร้างขึ้นมา ปก.ด้วย name,price...                             
   pass                                             # คำสั่งเอาไว้ดูว่ามันขึ้น post แล้สยัง                    

@app.post("/coffee")                                    
async def create_coffee(coffee: coffee):            # 2                            
   coffee = coffee_db.append(coffee)                # เพิ่ม coffee (name,price...)
   return coffee_db[-1]                                                      

@app.delete("/coffee/{id}")                         # 2
async def delete_coffee(id :int):                   # ลบ coffee
    coffee = coffee_db[id-1]
    coffee_db.pop(id-1)
    result = {"msg", f"{coffee['name']} was deleted"}
    return result                                # แสดงผลว่าลบอันไหนไป

@app.put("/coffee/{id}")                         # 2
async def update_coffee(id :int, coffee: coffee):                 # update 
    coffee_db[id-1].update(**coffee.dict())
    result = {"msg", f"coffee id {id} was updated"}
    return result


#@app.get("/")                                          # 1
#async def root():
#    return {"message": "Hello World"}

# สร้างหลาย /                                            # 1
#@app.get("/fastapi")
#async def fastapi():
#    return {"message": "many path"}
    
# สร้างหลาย / และรับค่า                                    # 1
#@app.get("/fastapi/{id}")
#async def fastapi(id :int):
 #   print(id)       
   # return {"message": "many path"}

# path ที่ใหญ่มาก่อนเสมอ ถ้าเอา para ขึ้นก่อนไม่ได้               # 1
#@app.get("/fastapi/current")
#async def current():
 #   return {"message": "current_path"}

# สร้างหลาย / และรับค่าprameter แสดงผล                     # 1
#@app.get("/fastapi/{id}")
#async def fastapi(id :int):      
#    return {"message": f"many path{id}"}   # f เป็น format
    


#---------------------เชื่อมต่อ server หรือดึงข้อมูลมาจาก db อื่น (coffee.py)-----------------------------------------------------------------------------------
'''app = FastAPI()                                        # 3

@app.get("/")                                          # 3   เอาข้อมูลใน coffee_db ออก ไปยังอีก serverนึง 
async def root():
   return {'hello' : 'python'}

def config_router():                                    # 3  สร้างฟังก์ชันเพื่อเรียก router
    app.include_router(coffee.router)


config_router()                                         # 3 เป็นฟังก์ชัน

'''

#---------------------------------------เชื่อมต่อ DB ด้วย tortoise orm (db ของ python) (todo.py)   !!!!!!!!! ติดดดดดดดดดดดดดดดดดดด-------------------------------------------------------------

'''app = FastAPI()


@app.get("/")
def route():
    return {'msg': 'well come FastAPI todo list'}


@app.get('/todos')
async def show_all_todos():
    return await Todos_Pydantic.from_queryset(Todos.all())


@app.get('/todo/{todo_id}')
async def todo_by_id(todo_id: int):
    return await Todos_Pydantic.from_queryset_single(Todos.get(id=todo_id))


@app.post('/todo')
async def create_todo(todo: TodosIn_Pydantic):
    todo_obj = await Todos.create(**todo.dict(exclude_unset=True))
    return await TodosIn_Pydantic.from_tortoise_orm(todo_obj)


@app.put('/todo/{todo_id}')
async def update_todo(todo_id:int, todo: TodosIn_Pydantic):
    await Todos.filter(id=todo_id).update(**todo.dict(exclude_unset=True))
    return await Todos_Pydantic.from_queryset_single(Todos.get(id=todo_id))


@app.delete('/todo/{todo_id}')
async def delete_todo(todo_id: int):
    todo_count = await Todos.filter(id=todo_id).delete()
    if not todo_count:
        return {'msg': f"Todo {todo_id} not found!"}
    return {'msg': f"Todo {todo_id} delete successfull!"}


register_tortoise(
    app,
    db_url='sqlite://db.sqlite2',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
'''
