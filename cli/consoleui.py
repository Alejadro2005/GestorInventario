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
from src.database.database_interface import DatabaseInterface


class ConsoleUI:
    def __init__(self, inventario: Inventario, gestor_usuarios: GestorUsuarios):
        self.gestor = gestor_usuarios
        self.inventario = inventario
        self.tienda = Tienda(self.inventario)

    def _cargar_inventario(self, ruta: str = "data/inventario.json") -> Inventario:
        datos = PersistenciaJSON.cargar_datos(ruta)

        # Manejar nuevo formato (diccionario) y antiguo (lista)
        if isinstance(datos, dict):
            productos_data = datos.values()  # Obtener solo los valores (datos del producto)
        else:
            productos_data = datos  # Compatibilidad con formato antiguo

        productos = [Producto(**p) for p in productos_data] if productos_data else []
        return Inventario(productos)

    def _guardar_inventario(self):
        # Guardar como diccionario con ID como clave
        datos = {str(p.id): p.to_dict() for p in self.inventario.productos}
        PersistenciaJSON.guardar_datos("data/inventario.json", datos)

    def _limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _mostrar_titulo(self, texto):
        print(f"\n{'=' * 50}")
        print(f"⚡ {texto.center(46)} ⚡")
        print(f"{'=' * 50}")

    def _menu_principal(self):
        self._mostrar_titulo("menú principal")
        print("1. Gestión de Productos")
        print("2. Gestión de Usuarios")
        print("3. Registrar Venta")
        print("4. Historial de Ventas")
        print("5. Salir")
        return input("\n📌 Seleccione una opción: ").strip()

    def _menu_productos(self):
        self._mostrar_titulo("gestión de productos")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar stock")
        print("4. Inventario")
        print("5. Volver al menú principal")
        return input("\n📌 Seleccione una opción: ").strip()

    def _menu_usuarios(self):
        self._mostrar_titulo("gestión de usuarios")
        print("1. Crear usuario")
        print("2. Eliminar usuario")
        print("3. Listar usuarios")
        print("4. Volver al menú principal")
        return input("\n📌 Seleccione una opción: ").strip()

    def _manejar_gestion_productos(self):
        while True:
            self._limpiar_pantalla()
            op = self._menu_productos()

            if op == "1":  # Agregar producto
                self._agregar_producto()
            elif op == "2":  # Eliminar producto
                self._eliminar_producto()
            elif op == "3":  # Actualizar stock
                self._actualizar_stock()
            elif op == "4":  # Mostrar inventario
                self._mostrar_inventario()
            elif op == "5":
                break
            else:
                self._mostrar_error("Opción inválida")

    def _manejar_gestion_usuarios(self):
        while True:
            self._limpiar_pantalla()
            op = self._menu_usuarios()

            if op == "1":  # Crear usuario
                self._crear_usuario()
            elif op == "2":  # Eliminar usuario
                self._eliminar_usuario()
            elif op == "3":  # Listar usuarios
                self._listar_usuarios()
            elif op == "4":
                break
            else:
                self._mostrar_error("Opción inválida")

    def _agregar_producto(self):
        try:
            self._mostrar_titulo("nuevo producto")
            id = int(input("ID del producto: "))
            nombre = input("Nombre: ")
            precio = float(input("Precio $: "))
            cantidad = int(input("Cantidad inicial: "))
            categoria = input("Categoría:(electronica o escolar en minuscula) ")
            stock_minimo = int(input("Stock mínimo: "))

            nuevo = Producto(id, nombre, precio, cantidad, categoria, stock_minimo)
            self.inventario.agregar_producto(nuevo)
            print("\n✅ Producto agregado correctamente!")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _eliminar_producto(self):
        try:
            self._mostrar_titulo("eliminar producto")
            id = int(input("ID del producto a eliminar: "))
            print(f"\n{self.inventario.eliminar_producto(id)}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _actualizar_stock(self):
        try:
            self._mostrar_titulo("actualizar stock")
            id = int(input("ID del producto: "))
            cantidad = int(input("Nueva cantidad: "))
            print(f"\n{self.inventario.actualizar_stock(id, cantidad)}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _mostrar_inventario(self):
        try:
            self._mostrar_titulo("inventario completo")
            productos = self.inventario.db.get_all_products()
            if not productos:
                print("\n📭 El inventario está vacío")
            else:
                print("\n📦 Lista de Productos:")
                for p in productos:
                    nombre = p['nombre'][:20] + "..." if len(p['nombre']) > 20 else p['nombre']
                    categoria = p['categoria'][:10] + "..." if len(p['categoria']) > 10 else p['categoria']
                    print(f"""
                🆔 ID: {p['id']}
                📦 Producto: {nombre}
                💲 Precio: {int(p['precio']):,}
                📥 Stock: {p['cantidad']} unidades
                🚨 Mínimo requerido: {p['stock_minimo']}
                📂 Categoría: {categoria}
                ───────────────────────────""")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _crear_usuario(self):
        try:
            self._mostrar_titulo("nuevo usuario")
            id = int(input("ID de usuario: "))
            nombre = input("Nombre completo: ")
            rol = input("Rol (admin/empleado): ").lower()
            contraseña = input("Contraseña: ")

            nuevo = Usuario(id, nombre, rol, contraseña)
            print(f"\n{self.gestor.crear_usuario(nuevo)}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _eliminar_usuario(self):
        try:
            self._mostrar_titulo("eliminar usuario")
            id = int(input("ID de usuario a eliminar: "))
            print(f"\n{self.gestor.eliminar_usuario(id)}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _listar_usuarios(self):
        try:
            self._mostrar_titulo("usuarios registrados")
            usuarios = self.gestor.db.get_all_users()
            if not usuarios:
                print("\n📭 No hay usuarios registrados")
            else:
                for usuario in usuarios:
                    print(f"🆔 ID: {usuario['id']} | 👤 {usuario['nombre']} | 🛠 Rol: {usuario['rol']}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        self._esperar_continuar()

    def _registrar_venta(self):
        try:
            self._mostrar_titulo("nueva venta")
            # Obtener el siguiente ID de venta basado en el historial actual
            historial = self.tienda.generar_historial()
            id_venta = len(historial) + 1

            # Validación de fecha
            while True:
                fecha = input("Fecha (DD/MM/AAAA) : ").strip()
                try:
                    day, month, year = map(int, fecha.split('/'))
                    if len(str(year)) == 2: year += 2000
                    datetime(year, month, day)
                    fecha = f"{day:02d}/{month:02d}/{year}"
                    break
                except ValueError:
                    print("❌ Formato inválido. Use DD/MM/AAAA (ej: 24/03/2025)\n")

            # Validación de empleado
            while True:
                try:
                    id_empleado = int(input("ID de empleado: "))
                    usuario = self.gestor.obtener_usuario(id_empleado)
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
                    if entrada in ["0", "T", "t"]: break

                    id_producto = int(entrada)
                    productos_db = self.inventario.db.get_all_products()
                    producto = next(p for p in productos_db if p['id'] == id_producto)
                    cantidad = int(input("Cantidad: "))

                    if cantidad <= 0:
                        print("❌ La cantidad debe ser mayor a 0")
                        continue

                    if producto['cantidad'] < cantidad:
                        print(f"❌ Stock insuficiente. Disponible: {producto['cantidad']}")
                        continue

                    productos.append((producto, cantidad))
                    print(f"✅ Añadido: {producto['nombre']} x{cantidad}")
                except StopIteration:
                    print("❌ Error: El producto no existe")
                except ValueError:
                    print("❌ Error: Ingrese un número válido")

            if not productos:
                print("\n⚠️ No se registraron productos en la venta")
                self._esperar_continuar()
                return

            venta = Venta(id_venta, fecha, productos, id_empleado, self.inventario)
            resultado = self.tienda.registrar_venta(venta, self.inventario)
            print(f"\n{resultado}")
        except Exception as e:
            print(f"\n❌ Error crítico: {str(e)}")
        self._esperar_continuar()

    def _mostrar_historial_ventas(self):
        while True:
            self._limpiar_pantalla()
            self._mostrar_titulo("historial de ventas")
            historial = self.tienda.generar_historial()
            if not historial:
                print("\n📭 No hay ventas registradas")
            else:
                for venta in historial:
                    print(f"\n🛒 Venta #{venta['id']}")
                    print(f"📅 Fecha: {venta['fecha']}")
                    print("📦 Productos:")
                    for p in venta['productos']: print(f"   - {p}")
                    print(f"💵 Total: {int(venta['total']):,}")
                    print(f"👤 Empleado ID: {venta['empleado']}")
                    print("-" * 50)
            print("\n1. Borrar historial de ventas")
            print("2. Volver al menú principal")
            op = input("\nSeleccione una opción: ").strip()
            if op == "1":
                mensaje = self.tienda.borrar_historial_ventas()
                print(f"\n✅ {mensaje}")
                self._esperar_continuar()
            elif op == "2":
                break
            else:
                print("\n❌ Opción inválida")
                self._esperar_continuar()

    def _mostrar_error(self, mensaje):
        print(f"\n❌ Error: {mensaje}")

    def _esperar_continuar(self):
        input("\nPresione Enter para continuar...")

    def ejecutar(self):
        while True:
            self._limpiar_pantalla()
            op = self._menu_principal()

            if op == "1":
                self._manejar_gestion_productos()
            elif op == "2":
                self._manejar_gestion_usuarios()
            elif op == "3":
                self._registrar_venta()
            elif op == "4":
                self._mostrar_historial_ventas()
            elif op == "5":
                print("\n👋 ¡Hasta pronto!")
                break
            else:
                self._mostrar_error("Opción inválida")
                self._esperar_continuar()
