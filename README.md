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

| ID  | Descripción                          | Entrada                                     | Salida Esperada                          | Tipo        |
|-----|--------------------------------------|---------------------------------------------|------------------------------------------|-------------|
| 19  | Crear usuario                        | Usuario(1, "Ana", "admin", "Pass123")     | Mensaje de éxito                         | Normal      |
| 20  | Validar rol                          | ID=1, rol="admin"                         | True                                   | Normal      |
| 21  | Eliminar usuario                     | ID=3                                      | Mensaje de eliminación                   | Normal      |
| 22  | Iniciar sesión exitoso               | contraseña="1234"                         | True                                   | Normal      |
| 23  | Cambiar contraseña                   | nueva_contraseña="4321"                   | Contraseña actualizada                   | Normal      |
| 24  | Iniciar sesión fallido               | contraseña="0000"                         | False                                  | Normal      |
| 25  | Usuario duplicado                    | ID repetido                                 | UsuarioDuplicadoError                  | Error       |
| 26  | Validar rol inexistente              | ID=99                                     | UsuarioNoEncontradoError               | Error       |
| 27  | Eliminar usuario inexistente         | ID=99                                     | UsuarioNoEncontradoError               | Error       |
| 28  | Contraseña vacía                     | contraseña=""                             | ContraseñaInvalidaError                | Error       |
| 29  | Credenciales inválidas               | contraseña="wrong"                        | CredencialesInvalidasError             | Error       |
| 30  | Cambio a contraseña inválida         | nueva_contraseña=""                       | ContraseñaInvalidaError                | Error       |
| 31  | Rol con emojis                       | rol="admin🔥"                             | RolInvalidoError                       | Extremo     |
| 32  | Nombre de 100 caracteres             | nombre="A"*100                            | NombreUsuarioInvalidoError             | Extremo     |
| 33  | Contraseña expirada                  | Fecha="01/01/2020"                          | ContraseñaExpiradaError                | Extremo     |
| 34  | Rol inexistente                      | rol="superheroe"                          | RolInvalidoError                       | Extremo     |
| 35  | Nombre usuario vacío                 | nombre=""                                 | NombreUsuarioInvalidoError             | Extremo     |
| 36  | Validar rol usuario eliminado        | Usuario previamente eliminado               | UsuarioNoEncontradoError               | Extremo     |

---

## 💰 **Módulo de Ventas**  
| ID  | Descripción                          | Entrada                                     | Salida Esperada                          | Tipo        |
|-----|--------------------------------------|---------------------------------------------|------------------------------------------|-------------|
| 37  | Registrar venta simple               | Venta con 2 productos                       | Historial con 1 venta                    | Normal      |
| 38  | Validar stock en venta               | cantidad=2                                | True                                   | Normal      |
| 39  | Registrar múltiples ventas           | 3 ventas                                    | Historial con 3 registros                | Normal      |
| 40  | Calcular total                       | precio=500, cantidad=2                    | Total=1000                               | Normal      |
| 41  | Validar stock post-venta             | Venta de 2 unidades                         | Stock reducido                           | Normal      |
| 42  | Generar historial                    | Venta registrada                            | Historial completo                       | Normal      |
| 43  | Precio negativo                      | precio=-100                               | ProductoInvalidoError                  | Error       |
| 44  | Stock negativo                       | cantidad=-5                               | ProductoInvalidoError                  | Error       |
| 45  | Producto duplicado                   | Producto repetido                           | ProductoDuplicadoError                 | Error       |
| 46  | Stock insuficiente                   | cantidad=100 (stock=10)                   | StockInsuficienteError                 | Error       |
| 47  | Cantidad negativa en venta           | cantidad=-5                               | VentaInvalidaError                     | Error       |
| 48  | Fecha inválida                       | fecha="32/13/25"                          | FechaInvalidaError                     | Error       |
| 49  | Venta producto no registrado         | Producto inexistente                        | VentaProductoNoRegistradoError         | Extremo     |
| 50  | Descuento >100%                      | descuento=150%                            | DescuentoInvalidoError                 | Extremo     |
| 51  | Venta sin productos                  | Lista vacía                                 | VentaInvalidaError                     | Extremo     |
| 52  | Total negativo                       | total=-50                                 | TotalInvalidoError                     | Extremo     |
| 53  | Venta sin empleado                   | id_empleado=None                          | VentaSinEmpleadoError                  | Extremo     |
| 54  | Categoría inválida                   | categoria="Fantasma"                      | CategoriaInvalidaError                 | Extremo     |
___


___
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

