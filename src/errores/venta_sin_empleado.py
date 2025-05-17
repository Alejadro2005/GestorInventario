class VentaSinEmpleadoError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una venta sin especificar el empleado.
    
    Esta excepción se utiliza para indicar que se intentó registrar una venta
    sin asignar un empleado responsable de la misma.
    """
    pass