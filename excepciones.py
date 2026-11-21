# ==============================================================================
# Archivo: excepciones.py
# Curso: Programación (213023) - UNAD | Fase 4 - Prácticas simuladas
# Descripción: Excepciones personalizadas para el control de errores del sistema.
# ==============================================================================


class ErrorInventario(Exception):
    """Clase base para todas las excepciones del sistema de inventario."""
    pass  # Hereda la funcionalidad básica de la clase Exception de Python


class CantidadInvalidaError(ErrorInventario):
    """Se lanza cuando la cantidad ingresada es menor o igual a cero."""

    def __init__(self, cantidad, mensaje="La cantidad debe ser un número entero mayor a cero."):
        self.cantidad = cantidad  # Almacena el valor incorrecto recibido
        self.mensaje = f"{mensaje} Valor recibido: {cantidad}"  # Construye el detalle del error
        super().__init__(self.mensaje)  # Envía el mensaje a la clase padre Exception


class StockInsuficienteError(ErrorInventario):
    """Se lanza cuando se solicitan más unidades de las disponibles en inventario."""

    def __init__(self, codigo_equipo, disponibles, solicitadas):
        self.codigo_equipo = codigo_equipo  # Guarda el código del equipo consultado
        self.disponibles = disponibles  # Guarda las unidades disponibles actualmente
        self.solicitadas = solicitadas  # Guarda las unidades solicitadas en el préstamo
        mensaje = (
            f"Stock insuficiente para el equipo '{codigo_equipo}'. "
            f"Disponibles: {disponibles} | Solicitadas: {solicitadas}"
        )  # Redacta un mensaje claro del fallo
        super().__init__(mensaje)  # Inicializa la excepción con el mensaje construido


class EquipoNoEncontradoError(ErrorInventario):
    """Se lanza cuando el código del equipo no existe en el inventario."""

    def __init__(self, codigo_equipo):
        self.codigo_equipo = codigo_equipo  # Guarda el código buscado
        super().__init__(f"No existe ningún equipo registrado con el código '{codigo_equipo}'.")  # Mensaje de error