from src.modelos.inventario import Inventario
from src.modelos.producto import Producto
from src.modelos.usuario import Usuario
from src.modulos.gestor_usuarios import GestorUsuarios
from src.modulos.tienda import Tienda
from src.modulos.persistencia import PersistenciaJSON
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.modelos.venta import Venta
from src.errores import *
from datetime import datetime
import os


def cargar_inventario(ruta: str = "data/inventario.json") -> Inventario:
    datos = PersistenciaJSON.cargar_datos(ruta)
    productos = [Producto(**p) for p in datos] if datos else []
    return Inventario(productos)


def guardar_inventario(inventario: Inventario):
    datos = [p.to_dict() for p in inventario.productos]
    PersistenciaJSON.guardar_datos("data/inventario.json", datos)


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_titulo(texto):
    print(f"\n{'=' * 50}")
    print(f"⚡ {texto.center(46)} ⚡")
    print(f"{'=' * 50}")


def menu_principal():
    mostrar_titulo("menú principal")
    print("1. Gestión de Productos")
    print("2. Gestión de Usuarios")
    print("3. Registrar Venta")
    print("4. Historial de Ventas")
    print("5. Salir")
    return input("\n📌 Seleccione una opción: ").strip()


def menu_productos():
    mostrar_titulo("gestión de productos")
    print("1. Agregar producto")
    print("2. Eliminar producto")
    print("3. Actualizar stock")
    print("4. Inventario")
    print("5. Volver al menú principal")
    return input("\n📌 Seleccione una opción: ").strip()


def menu_usuarios():
    mostrar_titulo("gestión de usuarios")
    print("1. Crear usuario")
    print("2. Eliminar usuario")
    print("3. Listar usuarios")
    print("4. Volver al menú principal")
    return input("\n📌 Seleccione una opción: ").strip()


def main():
    gestor = GestorUsuarios()
    inventario = cargar_inventario()
    tienda = Tienda(inventario)

    while True:
        limpiar_pantalla()
        opcion = menu_principal()

        if opcion == "1":  # Gestión de Productos
            while True:
                limpiar_pantalla()
                op = menu_productos()

                if op == "1":  # Agregar producto
                    try:
                        mostrar_titulo("nuevo producto")
                        id = int(input("ID del producto: "))
                        nombre = input("Nombre: ")
                        precio = float(input("Precio $: "))
                        cantidad = int(input("Cantidad inicial: "))
                        categoria = input("Categoría: ")
                        stock_minimo = int(input("Stock mínimo: "))

                        nuevo = Producto(id, nombre, precio, cantidad, categoria, stock_minimo)
                        inventario.agregar_producto(nuevo)
                        guardar_inventario(inventario)
                        print("\n✅ Producto agregado correctamente!")
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione Enter para continuar...")

                elif op == "2":  # Eliminar producto
                    try:
                        mostrar_titulo("eliminar producto")
                        id = int(input("ID del producto a eliminar: "))
                        print(f"\n{inventario.eliminar_producto(id)}")
                        guardar_inventario(inventario)
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione Enter para continuar...")

                elif op == "3":  # Actualizar stock
                    try:
                        mostrar_titulo("actualizar stock")
                        id = int(input("ID del producto: "))
                        cantidad = int(input("Nueva cantidad: "))
                        print(f"\n{inventario.actualizar_stock(id, cantidad)}")
                        guardar_inventario(inventario)
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione E4nter para continuar...")
                elif op == "4":  # Visualizar inventario completo
                    try:
                        mostrar_titulo("inventario completo")
                        if not inventario.productos:
                            print("\n📭 El inventario está vacío")
                        else:
                            print("\n📦 Lista de Productos:")
                            for p in inventario.productos:
                                # Formatear datos
                                nombre = p.nombre if len(p.nombre) <= 20 else p.nombre[:17] + "..."
                                categoria = p.categoria[:10] + "..." if len(p.categoria) > 10 else p.categoria

                                print(f"""
                        🆔 ID: {p.id}
                        📦 Producto: {nombre}
                        💲 Precio: ${p.precio:.2f}
                        📥 Stock: {p.cantidad} unidades
                        🚨 Mínimo requerido: {p.stock_minimo}
                        📂 Categoría: {categoria}
                        ───────────────────────────""")
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione Enter para continuar...")

        elif opcion == "2":  # Gestión de Usuarios
            while True:
                limpiar_pantalla()
                op = menu_usuarios()

                if op == "1":  # Crear usuario
                    try:
                        mostrar_titulo("nuevo usuario")
                        id = int(input("ID de usuario: "))
                        nombre = input("Nombre completo: ")
                        rol = input("Rol (admin/empleado/gerente): ").lower()
                        contraseña = input("Contraseña: ")

                        nuevo = Usuario(id, nombre, rol, contraseña)
                        print(f"\n{gestor.crear_usuario(nuevo)}")
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione Enter para continuar...")

                elif op == "2":  # Eliminar usuario
                    try:
                        mostrar_titulo("eliminar usuario")
                        id = int(input("ID de usuario a eliminar: "))
                        print(f"\n{gestor.eliminar_usuario(id)}")
                    except Exception as e:
                        print(f"\n❌ Error: {str(e)}")
                    input("\nPresione Enter para continuar...")

                elif op == "3":  # Listar usuarios
                    mostrar_titulo("usuarios registrados")
                    if not gestor.usuarios:
                        print("\n📭 No hay usuarios registrados")
                    else:
                        for id, usuario in gestor.usuarios.items():
                            print(f"🆔 ID: {id} | 👤 {usuario.nombre} | 🛠 Rol: {usuario.rol}")
                    input("\nPresione Enter para continuar...")

                elif op == "4":
                    break
                else:
                    print("\n⚠️ Opción inválida")
                    input("Presione Enter para continuar...")

        elif opcion == "3":  # Registrar Venta
            limpiar_pantalla()
            try:
                mostrar_titulo("nueva venta")
                id_venta = len(tienda.historial_ventas) + 1

                # Validación de fecha
                while True:
                    fecha = input("Fecha (DD/MM/AAAA): ").strip()
                    try:
                        day, month, year = map(int, fecha.split('/'))
                        if len(str(year)) == 2:
                            year += 2000
                        datetime(year, month, day)
                        fecha = f"{day:02d}/{month:02d}/{year}"
                        break
                    except ValueError:
                        print("❌ Formato inválido. Use DD/MM/AAAA (ej: 24/03/2025)\n")

                # Validación de empleado
                while True:
                    try:
                        id_empleado = int(input("ID de empleado: "))
                        usuario = gestor.obtener_usuario(id_empleado)
                        if usuario.rol != "empleado":
                            print("❌ El usuario no tiene rol de empleado\n")
                            continue
                        break
                    except UsuarioNoEncontradoError:
                        print("❌ El empleado no existe\n")
                    except ValueError:
                        print("❌ Ingrese un número válido\n")

                productos = []
                while True:
                    try:
                        entrada = input("\nID Producto (0 para terminar): ").strip()
                        if entrada in ["0", "T", "t"]:
                            break

                        id_producto = int(entrada)
                        producto = next(p for p in inventario.productos if p.id == id_producto)
                        cantidad = int(input("Cantidad: "))

                        if cantidad <= 0:
                            print("❌ La cantidad debe ser mayor a 0")
                            continue

                        productos.append((producto, cantidad))
                        print(f"✅ Añadido: {producto.nombre} x{cantidad}")
                    except StopIteration:
                        print("❌ Error: El producto no existe")
                    except ValueError:
                        print("❌ Error: Ingrese un número válido")

                if not productos:
                    print("\n⚠️ No se registraron productos en la venta")
                    input("\nPresione Enter para continuar...")
                    continue

                venta = Venta(id_venta, fecha, productos, id_empleado, inventario)
                resultado = tienda.registrar_venta(venta, inventario)
                guardar_inventario(inventario)
                print(f"\n{resultado}")
            except Exception as e:
                print(f"\n❌ Error crítico: {str(e)}")
            input("\nPresione Enter para continuar...")

        elif opcion == "4":  # Historial de Ventas
            limpiar_pantalla()
            mostrar_titulo("historial de ventas")
            historial = tienda.generar_historial()
            if not historial:
                print("\n📭 No hay ventas registradas")
            else:
                for venta in historial:
                    print(f"\n🛒 Venta #{venta['id']}")
                    print(f"📅 Fecha: {venta['fecha']}")
                    print("📦 Productos:")
                    for p in venta['productos']:
                        print(f"   - {p}")
                    print(f"💵 Total: ${venta['total']:.2f}")
                    print(f"👤 Empleado ID: {venta['empleado']}")
                    print("-" * 50)
            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            print("\n¡Gracias por usar el sistema! 👋")
            break

        else:
            print("\n⚠️ Opción inválida")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()