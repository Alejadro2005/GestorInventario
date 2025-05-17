from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DatabaseInterface(ABC):
    """Interfaz abstracta para la base de datos."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establece la conexión con la base de datos."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos."""
        pass
    
    @abstractmethod
    def create_tables(self) -> None:
        """Crea las tablas necesarias en la base de datos."""
        pass
    
    @abstractmethod
    def drop_tables(self) -> None:
        """Elimina todas las tablas de la base de datos."""
        pass
    
    # Métodos para Usuarios
    @abstractmethod
    def insert_user(self, user_data: Dict[str, Any]) -> int:
        """Inserta un nuevo usuario y retorna su ID."""
        pass
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un usuario por su ID."""
        pass
    
    @abstractmethod
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Actualiza los datos de un usuario."""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario por su ID."""
        pass
    
    @abstractmethod
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios."""
        pass
    
    # Métodos para Productos
    @abstractmethod
    def insert_product(self, product_data: Dict[str, Any]) -> int:
        """Inserta un nuevo producto y retorna su ID."""
        pass
    
    @abstractmethod
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un producto por su ID."""
        pass
    
    @abstractmethod
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Actualiza los datos de un producto."""
        pass
    
    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto por su ID."""
        pass
    
    @abstractmethod
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Obtiene todos los productos."""
        pass
    
    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Actualiza el stock de un producto."""
        pass
    
    # Métodos para Ventas
    @abstractmethod
    def insert_sale(self, sale_data: Dict[str, Any]) -> int:
        """Inserta una nueva venta y retorna su ID."""
        pass
    
    @abstractmethod
    def insert_sale_detail(self, detail_data: Dict[str, Any]) -> None:
        """Inserta un detalle de venta."""
        pass
    
    @abstractmethod
    def get_sale(self, sale_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una venta por su ID."""
        pass
    
    @abstractmethod
    def get_sale_details(self, sale_id: int) -> List[Dict[str, Any]]:
        """Obtiene los detalles de una venta."""
        pass
    
    @abstractmethod
    def get_all_sales(self) -> List[Dict[str, Any]]:
        """Obtiene todas las ventas."""
        pass
    
    @abstractmethod
    def get_all_sale_details(self) -> List[Dict[str, Any]]:
        """Obtiene todos los detalles de ventas."""
        pass
    
    @abstractmethod
    def get_sales_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtiene las ventas de un usuario específico."""
        pass
    
    @abstractmethod
    def get_sale_details_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtiene los detalles de ventas de un usuario específico."""
        pass
    
    @abstractmethod
    def delete_all_sales(self) -> None:
        """Elimina todas las ventas y sus detalles."""
        pass 