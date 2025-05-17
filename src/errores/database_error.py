class DatabaseError(Exception):
    """
    Excepción lanzada cuando ocurre un error en las operaciones de base de datos.
    
    Esta excepción se utiliza para encapsular errores específicos de la base de datos,
    como problemas de conexión, errores en consultas SQL, o violaciones de restricciones.
    """
    pass 