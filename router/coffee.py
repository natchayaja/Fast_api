from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router   = APIRouter(                                    # set up router                    
 prefix="/coffee",                                      #อะไรก็ตามที่ /coffee มันจะวิ่งมาที่ coffee
 tags= ['coffee'],                                           # แสดงหน้า swagger UI บอกว่า /(route นี้เป็นของอันไหน)
 responses= {404 : {
     'message': "Not Found"
        }
    }
)

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

@router.get('')                                             # 3 
async def show_all_coffee():
    return coffee_db
    

@router.get("/coffee/{id}")                                # 2     เอา id ที่รับมา ไปหาใน coffee_db
async def coffee_id(id :int):      
    coffee = coffee_db[id -1]                                   # -1 เพราะ list ช่องแรกเริ่มที่ 0
    return coffee

#@app.post("/coffee")                                # 2     
#async def create_coffee(coffee: coffee):            # (pydantic) รับ coffee เข้ามา แต่จะถูกครอบด้วย type Coffee(class) ที่เราสร้างขึ้นมา ปก.ด้วย name,price...                             
#   pass                                             # คำสั่งเอาไว้ดูว่ามันขึ้น post แล้สยัง                    

@router.post("/coffee")                                    
async def create_coffee(coffee: coffee):            # 2                            
   coffee = coffee_db.append(coffee)                # เพิ่ม coffee (name,price...)
   return coffee_db[-1]                                                      

@router.delete("/coffee/{id}")                         # 2
async def delete_coffee(id :int):                   # ลบ coffee
    coffee = coffee_db[id-1]
    coffee_db.pop(id-1)
    result = {"msg", f"{coffee['name']} was deleted"}
    return result                                # แสดงผลว่าลบอันไหนไป

@router.put("/coffee/{id}")                         # 2
async def update_coffee(id :int, coffee: coffee):                 # update 
    coffee_db[id-1].update(**coffee.dict())
    result = {"msg", f"coffee id {id} was updated"}
    return result