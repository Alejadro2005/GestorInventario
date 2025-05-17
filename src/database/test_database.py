from typing import Dict, Any, List, Optional
from src.database.database_interface import DatabaseInterface
from src.errores.usuario_duplicado import UsuarioDuplicadoError
from src.errores.productos_duplicados import ProductoDuplicadoError

class DatabaseTest(DatabaseInterface):
    """Implementación de base de datos en memoria para pruebas."""
    
    def __init__(self, config=None):
        self.usuarios = {}
        self.productos = {}
        self.ventas = {}
        self.detalle_ventas = {}  # {(venta_id, producto_id): detalle}
        self.next_id = 1
    
    def connect(self) -> None:
        """No es necesario conectar en la base de datos de prueba."""
        pass
    
    def disconnect(self) -> None:
        """No es necesario desconectar en la base de datos de prueba."""
        pass
    
    def create_tables(self) -> None:
        """No es necesario crear tablas en la base de datos de prueba."""
        pass
    
    def drop_tables(self) -> None:
        """Limpia todos los datos de prueba."""
        self.usuarios.clear()
        self.productos.clear()
        self.ventas.clear()
        self.detalle_ventas.clear()
        self.next_id = 1
    
    def create_user(self, user_data):
        """Crea un nuevo usuario y retorna su ID."""
        for u in self.usuarios.values():
            if u['nombre'] == user_data['nombre']:
                raise UsuarioDuplicadoError(f"El usuario con nombre '{user_data['nombre']}' ya existe.")
        user_id = self.next_id
        self.next_id += 1
        user = user_data.copy()
        user['id'] = user_id
        self.usuarios[user_id] = user
        return user_id
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.usuarios.get(user_id)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        if user_id not in self.usuarios:
            return False
        self.usuarios[user_id].update(user_data)
        return True
    
    def delete_user(self, user_id: int) -> bool:
        if user_id in self.usuarios:
            del self.usuarios[user_id]
            return True
        return False
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        return list(self.usuarios.values())
    
    def create_product(self, product_data):
        """Crea un nuevo producto y retorna su ID."""
        for p in self.productos.values():
            if p['nombre'] == product_data['nombre']:
                raise ProductoDuplicadoError(f"El producto con nombre '{product_data['nombre']}' ya existe en el inventario.")
        product_id = self.next_id
        self.next_id += 1
        product = product_data.copy()
        product['id'] = product_id
        self.productos[product_id] = product
        return product_id
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        return self.productos.get(product_id)
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        if product_id not in self.productos:
            return False
        self.productos[product_id].update(product_data)
        return True
    
    def delete_product(self, product_id: int) -> bool:
        if product_id in self.productos:
            del self.productos[product_id]
            return True
        return False
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        return list(self.productos.values())
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        if product_id not in self.productos:
            return False
        self.productos[product_id]['cantidad'] += quantity
        return True
    
    def create_sale(self, sale_data: Dict[str, Any]) -> int:
        sale_id = self.next_id
        self.next_id += 1
        sale = sale_data.copy()
        sale['id'] = sale_id
        self.ventas[sale_id] = sale
        return sale_id
    
    def insert_sale_detail(self, detail_data: Dict[str, Any]) -> None:
        venta_id = detail_data['venta_id']
        producto_id = detail_data['producto_id']
        key = (venta_id, producto_id)
        self.detalle_ventas[key] = {
            'venta_id': venta_id,
            'producto_id': producto_id,
            'cantidad': detail_data['cantidad'],
            'precio': detail_data['precio']
        }
    
    def get_sale(self, sale_id: int) -> Optional[Dict[str, Any]]:
        if sale_id not in self.ventas:
            return None
        venta = self.ventas[sale_id].copy()
        usuario = self.usuarios.get(venta['id_usuario'])
        if usuario:
            venta['usuario_nombre'] = usuario['nombre']
        return venta
    
    def get_sale_details(self, sale_id: int) -> List[Dict[str, Any]]:
        detalles = []
        for (v_id, p_id), detalle in self.detalle_ventas.items():
            if v_id == sale_id:
                detalle_copy = detalle.copy()
                producto = self.productos.get(p_id)
                if producto:
                    detalle_copy['producto_nombre'] = producto['nombre']
                detalles.append(detalle_copy)
        return detalles
    
    def get_all_sales(self) -> List[Dict[str, Any]]:
        return [self.get_sale(sale_id) for sale_id in self.ventas]
    
    def get_all_sale_details(self) -> List[Dict[str, Any]]:
        detalles = []
        for (v_id, p_id), detalle in self.detalle_ventas.items():
            detalle_copy = detalle.copy()
            producto = self.productos.get(p_id)
            if producto:
                detalle_copy['producto_nombre'] = producto['nombre']
            detalles.append(detalle_copy)
        return detalles
    
    def get_sales_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        return [venta for venta in self.get_all_sales() if venta['id_usuario'] == user_id]
    
    def get_sale_details_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        detalles = []
        for venta in self.get_sales_by_user(user_id):
            detalles.extend(self.get_sale_details(venta['id']))
        return detalles
    
    def delete_all_sales(self) -> None:
        self.ventas.clear()
        self.detalle_ventas.clear()
    
    def insert_product(self, *args, **kwargs):
        pass

    def insert_sale(self, *args, **kwargs):
        pass

    def insert_user(self, *args, **kwargs):
        pass

    def clear_all(self):
        self.drop_tables() 