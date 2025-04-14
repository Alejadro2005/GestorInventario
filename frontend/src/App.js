// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [productos, setProductos] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [nuevoProducto, setNuevoProducto] = useState({
    id: '',
    nombre: '',
    precio: '',
    cantidad: '',
    categoria: '',
    stock_minimo: ''
  });
  const [nuevoUsuario, setNuevoUsuario] = useState({
    id: '',
    nombre: '',
    rol: '',
    contraseña: ''
  });
  const [nuevaVenta, setNuevaVenta] = useState({
    fecha: '',
    id_empleado: '',
    productos: [{ id: '', cantidad: '' }]
  });

  // Cargar datos iniciales
  useEffect(() => {
    fetch('http://localhost:5000/api/productos')
      .then(res => res.json())
      .then(data => setProductos(data))
      .catch(err => console.error(err));

    fetch('http://localhost:5000/api/usuarios')
      .then(res => res.json())
      .then(data => setUsuarios(data))
      .catch(err => console.error(err));

    fetch('http://localhost:5000/api/ventas')
      .then(res => res.json())
      .then(data => setVentas(data))
      .catch(err => console.error(err));
  }, []);

  // Manejar la adición de un nuevo producto
  const agregarProducto = () => {
    fetch('http://localhost:5000/api/productos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevoProducto)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.mensaje);
        setProductos([...productos, nuevoProducto]);
        setNuevoProducto({ id: '', nombre: '', precio: '', cantidad: '', categoria: '', stock_minimo: '' });
      })
      .catch(err => console.error(err));
  };

  // Manejar la eliminación de un producto
  const eliminarProducto = (id) => {
    fetch(`http://localhost:5000/api/productos/${id}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(data => {
        alert(data.mensaje);
        setProductos(productos.filter(p => p.id !== id));
      })
      .catch(err => console.error(err));
  };

  // Manejar la adición de un nuevo usuario
  const agregarUsuario = () => {
    fetch('http://localhost:5000/api/usuarios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevoUsuario)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.mensaje);
        setUsuarios([...usuarios, nuevoUsuario]);
        setNuevoUsuario({ id: '', nombre: '', rol: '', contraseña: '' });
      })
      .catch(err => console.error(err));
  };

  // Manejar la eliminación de un usuario
  const eliminarUsuario = (id) => {
    fetch(`http://localhost:5000/api/usuarios/${id}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(data => {
        alert(data.mensaje);
        setUsuarios(usuarios.filter(u => u.id !== id));
      })
      .catch(err => console.error(err));
  };

  // Manejar la adición de una nueva venta
  const agregarVenta = () => {
    fetch('http://localhost:5000/api/ventas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevaVenta)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.mensaje);
        setVentas([...ventas, nuevaVenta]);
        setNuevaVenta({ fecha: '', id_empleado: '', productos: [{ id: '', cantidad: '' }] });
      })
      .catch(err => console.error(err));
  };

  return (
    <div className="App">
      <h1>Gestor de Inventario</h1>

      {/* Gestión de Productos */}
      <div>
        <h2>Gestión de Productos</h2>
        <input
          type="number"
          placeholder="ID"
          value={nuevoProducto.id}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, id: parseInt(e.target.value) })}
        />
        <input
          type="text"
          placeholder="Nombre"
          value={nuevoProducto.nombre}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, nombre: e.target.value })}
        />
        <input
          type="number"
          placeholder="Precio"
          value={nuevoProducto.precio}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, precio: parseFloat(e.target.value) })}
        />
        <input
          type="number"
          placeholder="Cantidad"
          value={nuevoProducto.cantidad}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, cantidad: parseInt(e.target.value) })}
        />
        <input
          type="text"
          placeholder="Categoría (electronica/escolar)"
          value={nuevoProducto.categoria}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, categoria: e.target.value })}
        />
        <input
          type="number"
          placeholder="Stock Mínimo"
          value={nuevoProducto.stock_minimo}
          onChange={(e) => setNuevoProducto({ ...nuevoProducto, stock_minimo: parseInt(e.target.value) })}
        />
        <button onClick={agregarProducto}>Agregar Producto</button>

        <h3>Inventario</h3>
        <ul>
          {productos.map(producto => (
            <li key={producto.id}>
              {producto.nombre} - ${producto.precio} - Stock: {producto.cantidad} - Categoría: {producto.categoria}
              <button onClick={() => eliminarProducto(producto.id)}>Eliminar</button>
            </li>
          ))}
        </ul>
      </div>

      {/* Gestión de Usuarios */}
      <div>
        <h2>Gestión de Usuarios</h2>
        <input
          type="number"
          placeholder="ID"
          value={nuevoUsuario.id}
          onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, id: parseInt(e.target.value) })}
        />
        <input
          type="text"
          placeholder="Nombre"
          value={nuevoUsuario.nombre}
          onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, nombre: e.target.value })}
        />
        <input
          type="text"
          placeholder="Rol (admin/empleado/gerente)"
          value={nuevoUsuario.rol}
          onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, rol: e.target.value })}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={nuevoUsuario.contraseña}
          onChange={(e) => setNuevoUsuario({ ...nuevoUsuario, contraseña: e.target.value })}
        />
        <button onClick={agregarUsuario}>Agregar Usuario</button>

        <h3>Usuarios</h3>
        <ul>
          {usuarios.map(usuario => (
            <li key={usuario.id}>
              {usuario.nombre} - Rol: {usuario.rol}
              <button onClick={() => eliminarUsuario(usuario.id)}>Eliminar</button>
            </li>
          ))}
        </ul>
      </div>

      {/* Registrar Venta */}
      <div>
        <h2>Registrar Venta</h2>
        <input
          type="text"
          placeholder="Fecha (DD/MM/AAAA)"
          value={nuevaVenta.fecha}
          onChange={(e) => setNuevaVenta({ ...nuevaVenta, fecha: e.target.value })}
        />
        <input
          type="number"
          placeholder="ID Empleado"
          value={nuevaVenta.id_empleado}
          onChange={(e) => setNuevaVenta({ ...nuevaVenta, id_empleado: parseInt(e.target.value) })}
        />
        <div>
          <h3>Productos de la Venta</h3>
          {nuevaVenta.productos.map((prod, index) => (
            <div key={index}>
              <input
                type="number"
                placeholder="ID Producto"
                value={prod.id}
                onChange={(e) => {
                  const newProductos = [...nuevaVenta.productos];
                  newProductos[index].id = parseInt(e.target.value);
                  setNuevaVenta({ ...nuevaVenta, productos: newProductos });
                }}
              />
              <input
                type="number"
                placeholder="Cantidad"
                value={prod.cantidad}
                onChange={(e) => {
                  const newProductos = [...nuevaVenta.productos];
                  newProductos[index].cantidad = parseInt(e.target.value);
                  setNuevaVenta({ ...nuevaVenta, productos: newProductos });
                }}
              />
            </div>
          ))}
          <button onClick={() => setNuevaVenta({ ...nuevaVenta, productos: [...nuevaVenta.productos, { id: '', cantidad: '' }] })}>
            Agregar Otro Producto
          </button>
        </div>
        <button onClick={agregarVenta}>Registrar Venta</button>

        <h3>Historial de Ventas</h3>
        <ul>
          {ventas.map(venta => (
            <li key={venta.id}>
              Venta #{venta.id} - Fecha: {venta.fecha} - Total: ${venta.total} - Empleado ID: {venta.empleado}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App; 
