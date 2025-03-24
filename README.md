![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pruebas](https://img.shields.io/badge/Pruebas-54_total-ff69b4)
![Cobertura](https://img.shields.io/badge/Cobertura-83%25-green)
# 📦 Gestor de Inventario y Ventas  
Sistema para gestionar productos, ventas y usuarios en un entorno retail. Permite:  
- **Control de inventario**: Agregar, eliminar y actualizar productos.  
- **Registro de ventas**: Validar stock y generar historial.  
- **Gestión de usuarios**: Roles (Admin/Empleado)
## ⚙️ Configuración Inicial

```bash
# Configuración Inicial (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
$env:PYTHONPATH = "$(Get-Location)"
pip install pytest
```

## 📌 Diagrama de Clases
![Diagrama de Clases](https://github.com/user-attachments/assets/02442fa2-5d86-40f2-b4dd-3cf747bbd67c)

## 🧪 Casos de Prueba (54 Total)

### 🔧 **Módulo de Inventario** (18 Pruebas)
| ID  | Descripción                          | Tipo        | Estado |
|-----|--------------------------------------|-------------|--------|
| 1   | Agregar producto                     | Normal      | ✅     |
| 2   | Eliminar producto existente          | Normal      | ✅     |
| 3   | Actualizar stock válido              | Normal      | ✅     |
| 7   | Producto duplicado                   | Error       | ✅     |
| 14  | Stock máximo excedido (1001)         | Extremo     | ✅     |
| 18  | Precio negativo en venta             | Extremo     | ✅     |

### 👤 **Módulo de Usuarios** (16 Pruebas)
| ID  | Descripción                          | Tipo        | Estado |
|-----|--------------------------------------|-------------|--------|
| 19  | Crear usuario                        | Normal      | ❌     |
| 25  | Usuario duplicado                    | Error       | ❌     |
| 31  | Rol con emojis                       | Extremo     | ✅     |
| 36  | Validar rol usuario eliminado        | Extremo     | ✅     |

### 💰 **Módulo de Ventas** (20 Pruebas)
| ID  | Descripción                          | Tipo        | Estado |
|-----|--------------------------------------|-------------|--------|
| 37  | Registrar venta simple               | Normal      | ✅     |
| 46  | Stock insuficiente                   | Error       | ❌     |
| 50  | Descuento >100%                      | Extremo     | ✅     |
| 54  | Categoría inválida                   | Extremo     | ✅     |



## 🚨 Problemas Conocidos

```markdown
- **Errores Críticos en Ventas:**  
  ❌ `TypeError: Tienda() missing 1 required argument: 'inventario'`  
  ❌ Validación de stock falla en múltiples ventas (IDs 46, 39)

- **Problemas de Usuarios:**  
  ❌ Duplicación de IDs en pruebas consecutivas  
  ❌ `RolInvalidoError` al crear usuario (ID 19)

- **Mejoras Pendientes:**  
  ⚠️ Añadir paginación al historial de ventas  
  ⚠️ Implementar búsqueda por categoría
```

## ▶️ Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v --cov=src

# Ejecutar pruebas específicas
pytest tests/test_tienda.py -k "test_stock_insuficiente"

# Generar reporte HTML de cobertura
pytest --cov=src --cov-report=html
```

