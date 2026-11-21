# ==============================================================================
# Archivo: modelos.py
# Curso: Programación (213023) - UNAD | Fase 4 - Prácticas simuladas
# Descripción: Clases Equipo e InventarioLab bajo Programación Orientada a Objetos.
# ==============================================================================

# Importa las excepciones personalizadas creadas en excepciones.py
from excepciones import (
    CantidadInvalidaError,
    StockInsuficienteError,
    EquipoNoEncontradoError,
)


class Equipo:
    """Representa un equipo tecnológico con control de unidades disponibles."""

    def __init__(self, codigo: str, nombre: str, cantidad_total: int):
        # Verifica que el código y el nombre no estén vacíos ni compuestos solo por espacios
        if not codigo.strip() or not nombre.strip():
            raise ValueError("El código y el nombre del equipo son obligatorios.")
        # Verifica que la cantidad inicial sea un entero positivo
        if cantidad_total <= 0:
            raise CantidadInvalidaError(cantidad_total, "La cantidad inicial debe ser mayor a cero.")

        self.codigo = codigo.strip().upper()  # Normaliza el código en mayúsculas sin espacios extremos
        self.nombre = nombre.strip()  # Guarda el nombre limpio del equipo
        self._cantidad_total = int(cantidad_total)  # Almacena la capacidad total registrada
        self._disponibles = int(cantidad_total)  # Inicializa las unidades disponibles igual al total

    @property
    def disponibles(self) -> int:
        """Retorna de forma segura las unidades disponibles actuales."""
        return self._disponibles  # Devuelve el atributo protegido _disponibles

    def prestar(self, cantidad: int) -> int:
        """Descuenta unidades prestadas si la cantidad es válida y hay stock suficiente."""
        if cantidad <= 0:  # Valida que no se presten cantidades cero o negativas
            raise CantidadInvalidaError(cantidad, "La cantidad a prestar debe ser mayor a cero.")
        if cantidad > self._disponibles:  # Comprueba si hay suficientes equipos disponibles
            raise StockInsuficienteError(self.codigo, self._disponibles, cantidad)
        self._disponibles -= cantidad  # Resta las unidades prestadas del stock disponible
        return self._disponibles  # Retorna el nuevo número de unidades disponibles

    def devolver(self, cantidad: int) -> int:
        """Reintegra unidades devueltas verificando que no superen el total del equipo."""
        if cantidad <= 0:  # Valida que la devolución sea mayor a cero
            raise CantidadInvalidaError(cantidad, "La cantidad a devolver debe ser mayor a cero.")
        if self._disponibles + cantidad > self._cantidad_total:  # Evita exceder el stock total original
            raise ValueError(
                f"No se pueden devolver {cantidad} unidades: excedería el total de {self._cantidad_total}."
            )
        self._disponibles += cantidad  # Suma las unidades devueltas a las disponibles
        return self._disponibles  # Retorna las unidades disponibles actualizadas

    def __str__(self) -> str:
        """Devuelve una representación legible del estado del equipo."""
        return (
            f"[{self.codigo}] {self.nombre} | "
            f"Disponibles: {self._disponibles}/{self._cantidad_total}"
        )  # Formatea la salida de texto del objeto


class InventarioLab:
    """Administra el conjunto de equipos registrados en el laboratorio."""

    def __init__(self, nombre_lab: str):
        self.nombre_lab = nombre_lab  # Guarda el nombre del laboratorio
        self.equipos = {}  # Diccionario para almacenar cuentas {codigo: instancia_Equipo}

    def registrar_equipo(self, codigo: str, nombre: str, cantidad_total: int) -> Equipo:
        """Registra un equipo nuevo evitando códigos duplicados."""
        codigo_limpio = codigo.strip().upper()  # Estandariza el código para buscarlo
        if codigo_limpio in self.equipos:  # Revisa si ya existe un equipo con ese código
            raise ValueError(f"Ya existe un equipo registrado con el código '{codigo_limpio}'.")
        nuevo_equipo = Equipo(codigo_limpio, nombre, cantidad_total)  # Crea la instancia de Equipo
        self.equipos[codigo_limpio] = nuevo_equipo  # Guarda el objeto en el diccionario
        return nuevo_equipo  # Retorna el equipo creado

    def buscar_equipo(self, codigo: str) -> Equipo:
        """Busca un equipo por su código y lanza excepción si no está registrado."""
        codigo_limpio = codigo.strip().upper()  # Limpia y convierte a mayúsculas el código
        if codigo_limpio not in self.equipos:  # Valida si el código existe en el inventario
            raise EquipoNoEncontradoError(codigo_limpio)
        return self.equipos[codigo_limpio]  # Retorna el objeto Equipo encontrado

