from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

# Importaciones directas desde la raíz (sin app.)
from database import create_db_and_tables, get_session
from models import Producto, Pedido

app = FastAPI(
    title="API de Gestión de Productos y Pedidos",
    description="API RESTful desplegada en AWS EC2",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- ENDPOINTS PRODUCTOS ---
@app.post("/productos/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Producto, session: Session = Depends(get_session)):
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@app.get("/productos/", response_model=List[Producto])
def listar_productos(session: Session = Depends(get_session)):
    return session.exec(select(Producto)).all()

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, datos: Producto, session: Session = Depends(get_session)):
    db_producto = session.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    prod_data = datos.model_dump(exclude_unset=True)
    for key, value in prod_data.items():
        setattr(db_producto, key, value)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"mensaje": "Producto eliminado exitosamente"}

# --- ENDPOINTS PEDIDOS ---
@app.post("/pedidos/", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: Pedido, session: Session = Depends(get_session)):
    producto = session.get(Producto, pedido.producto_id)
    if not producto:
        raise HTTPException(status_code=400, detail="El producto asociado no existe")
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

@app.get("/pedidos/", response_model=List[Pedido])
def listar_pedidos(session: Session = Depends(get_session)):
    return session.exec(select(Pedido)).all()