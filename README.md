#algunos comandos que debes usar antes de hacer las pruebas
    python3 -m venv venv
    source venv/bin/activate
    export PYTHONPATH=$(pwd)
    pip install pytest   


# Proyecto_codigo_limpio
---
# 📦 Gestor de Inventario y Ventas  
Sistema para gestionar productos, ventas y usuarios en un entorno retail. Permite:  
- **Control de inventario**: Agregar, eliminar y actualizar productos.  
- **Registro de ventas**: Validar stock y generar historial.  
- **Gestión de usuarios**: Roles (Admin/Empleado) y autenticación segura.

---
# Diagrama de clases
![Diagrama drawio](https://github.com/user-attachments/assets/19b05e6d-76de-480b-904b-ddb99b561995) 

---
# 📋 Tabla de Casos de Prueba (54 Total)

## 🔧 **Módulo de Inventario**  
| ID  | Descripción                          | Entrada                                     | Salida Esperada                          | Tipo        |
|-----|--------------------------------------|---------------------------------------------|------------------------------------------|-------------|
| 1   | Agregar producto                     | `Producto(1, "Lápiz", 500, 10, "Escolar")` | Inventario con 1 producto                | Normal      |
| 2   | Eliminar producto existente          | `ID=1`                                      | Mensaje de éxito                         | Normal      |
| 3   | Actualizar stock válido              | `ID=1, cantidad=10`                         | Stock actualizado a 20                   | Normal      |
| 4   | Filtrar stock bajo                   | Productos con stock bajo                    | Lista de productos                       | Normal      |
| 5   | Eliminar múltiples productos         | `ID=1`                                      | Inventario con 1 producto restante       | Normal      |
| 6   | Actualizar stock interno             | `cantidad=5`                                | Stock=10                                 | Normal      |
| 7   | Producto duplicado                   | Producto con ID repetido                    | `ProductoDuplicadoError`                 | Error       |
| 8   | Eliminar producto inexistente        | `ID=99`                                     | `ProductoNoEncontradoError`              | Error       |
| 9   | Actualizar stock negativo            | `cantidad=-5`                               | `StockInvalidoError`                     | Error       |
| 10  | Filtrar sin productos                | Inventario vacío                            | `NoHayProductosError`                    | Error       |
| 11  | Nombre de producto vacío             | `nombre=""`                                 | `ProductoInvalidoError`                  | Error       |
| 12  | Actualizar stock producto inexistente| `ID=99`                                     | `ProductoNoEncontradoError`              | Error       |
| 13  | Categoría numérica                   | `categoria="1234"`                          | `CategoriaInvalidaError`                 | Extremo     |
| 14  | Stock máximo excedido (1001)         | `cantidad=1001`                             | `StockInvalidoError`                     | Extremo     |
| 15  | Precio cero                          | `precio=0`                                  | `PrecioInvalidoError`                    | Extremo     |

---

## 👤 **Módulo de Usuarios**  
| ID  | Descripción                          | Entrada                                     | Salida Esperada                          | Tipo        |
|-----|--------------------------------------|---------------------------------------------|------------------------------------------|-------------|
| 16  | Crear usuario                        | `Usuario(1, "Ana", "admin", "Pass123")`     | Mensaje de éxito                         | Normal      |
| 17  | Validar rol                          | `ID=1, rol="admin"`                         | `True`                                   | Normal      |
| 18  | Eliminar usuario                     | `ID=3`                                      | Mensaje de eliminación                   | Normal      |
| 19  | Iniciar sesión exitoso               | `contraseña="1234"`                         | `True`                                   | Normal      |
| 20  | Cambiar contraseña                   | `nueva_contraseña="4321"`                   | Contraseña actualizada                   | Normal      |
| 21  | Iniciar sesión fallido               | `contraseña="0000"`                         | `False`                                  | Normal      |
| 22  | Usuario duplicado                    | ID repetido                                 | `UsuarioDuplicadoError`                  | Error       |
| 23  | Validar rol inexistente              | `ID=99`                                     | `UsuarioNoEncontradoError`               | Error       |
| 24  | Eliminar usuario inexistente         | `ID=99`                                     | `UsuarioNoEncontradoError`               | Error       |
| 25  | Contraseña vacía                     | `contraseña=""`                             | `ContraseñaInvalidaError`                | Error       |
| 26  | Credenciales inválidas               | `contraseña="wrong"`                        | `CredencialesInvalidasError`             | Error       |
| 27  | Cambio a contraseña inválida         | `nueva_contraseña=""`                       | `ContraseñaInvalidaError`                | Error       |
| 28  | Rol con emojis                       | `rol="admin🔥"`                             | `RolInvalidoError`                       | Extremo     |
| 29  | Nombre de 100 caracteres             | `nombre="A"*100`                            | `NombreUsuarioInvalidoError`             | Extremo     |
| 30  | Contraseña expirada                  | Fecha="01/01/2020"                          | `ContraseñaExpiradaError`                | Extremo     |

---

## 💰 **Módulo de Ventas**  
| ID  | Descripción                          | Entrada                                     | Salida Esperada                          | Tipo        |
|-----|--------------------------------------|---------------------------------------------|------------------------------------------|-------------|
| 31  | Registrar venta simple               | Venta con 2 productos                       | Historial con 1 venta                    | Normal      |
| 32  | Validar stock en venta               | `cantidad=2`                                | `True`                                   | Normal      |
| 33  | Registrar múltiples ventas           | 3 ventas                                    | Historial con 3 registros                | Normal      |
| 34  | Calcular total                       | `precio=500, cantidad=2`                    | Total=1000                               | Normal      |
| 35  | Validar stock post-venta             | Venta de 2 unidades                         | Stock reducido                           | Normal      |
| 36  | Generar historial                    | Venta registrada                            | Historial completo                       | Normal      |
| 37  | Precio negativo                      | `precio=-100`                               | `ProductoInvalidoError`                  | Error       |
| 38  | Stock negativo                       | `cantidad=-5`                               | `ProductoInvalidoError`                  | Error       |
| 39  | Producto duplicado                   | Producto repetido                           | `ProductoDuplicadoError`                 | Error       |
| 40  | Stock insuficiente                   | `cantidad=100` (stock=10)                   | `StockInsuficienteError`                 | Error       |
| 41  | Cantidad negativa en venta           | `cantidad=-5`                               | `VentaInvalidaError`                     | Error       |
| 42  | Fecha inválida                       | `fecha="32/13/25"`                          | `FechaInvalidaError`                     | Error       |
| 43  | Venta producto no registrado         | Producto inexistente                        | `VentaProductoNoRegistradoError`         | Extremo     |
| 44  | Descuento >100%                      | `descuento=150%`                            | `DescuentoInvalidoError`                 | Extremo     |
| 45  | Venta sin productos                  | Lista vacía                                 | `VentaInvalidaError`                     | Extremo     |
| 46  | Total negativo                       | `total=-50`                                 | `TotalInvalidoError`                     | Extremo     |
| 47  | Venta sin empleado                   | `id_empleado=None`                          | `VentaSinEmpleadoError`                  | Extremo     |
| 48  | Categoría inválida                   | `categoria="Fantasma"`                      | `CategoriaInvalidaError`                 | Extremo     |
| 49  | Rol inexistente                      | `rol="superheroe"`                          | `RolInvalidoError`                       | Extremo     |
| 50  | Nombre usuario vacío                 | `nombre=""`                                 | `NombreUsuarioInvalidoError`             | Extremo     |
| 51  | Validar rol usuario eliminado        | Usuario previamente eliminado               | `UsuarioNoEncontradoError`               | Extremo     |
| 52  | Producto con caracteres especiales   | `nombre="@@Lápiz!!"`                        | `ProductoInvalidoError`                  | Extremo     |
| 53  | Categoría vacía                      | `categoria=""`                              | `CategoriaInvalidaError`                 | Extremo     |
| 54  | Precio negativo en venta             | `precio=-50`                                | `PrecioInvalidoError`                    | Extremo     |

---
