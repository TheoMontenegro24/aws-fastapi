from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
    pedidos: List["Pedido"] = Relationship(back_populates="producto")

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: int
    cliente: str
    producto_id: int = Field(foreign_key="producto.id")
    producto: Optional[Producto] = Relationship(back_populates="pedidos")