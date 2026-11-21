# ==============================================================================
# Archivo: main.py
# Curso: Programación (213023) - UNAD | Fase 4 - Prácticas simuladas
# Descripción: Menú interactivo y validación secuencial con try/except/finally.
# ==============================================================================

# Importa la clase gestora del inventario y las excepciones personalizadas
from modelos import InventarioLab
from excepciones import (
    CantidadInvalidaError,
    StockInsuficienteError,
    EquipoNoEncontradoError,
)


def solicitar_entero(mensaje: str) -> int:
    """Solicita un número entero al usuario y controla errores de conversión (ValueError)."""
    texto = input(mensaje).strip()  # Lee la entrada del usuario y elimina espacios externos
    try:
        numero = int(texto)  # Intenta convertir la cadena ingresada a entero
    except ValueError as err:
        # Captura el error si el usuario escribe letras, decimales o texto vacío
        raise ValueError(f"Entrada no válida ('{texto}'). Debe ingresar un número entero.") from err
    return numero  # Retorna el número entero válido


def ejecutar_sistema():
    """Controla el flujo principal del programa y gestiona excepciones por operación."""
    inventario = InventarioLab("Laboratorio de Sistemas UNAD")  # Crea el objeto del inventario

    # Precarga inicial de equipos para realizar pruebas secuenciales
    inventario.registrar_equipo("EQ-01", "Multímetro Digital", 10)
    inventario.registrar_equipo("EQ-02", "Osciloscopio", 4)

    while True:  # Ciclo repetitivo del menú hasta que el usuario elija salir
        print(f"\n=== {inventario.nombre_lab} ===")
        print("1. Registrar equipo")
        print("2. Prestar equipo")
        print("3. Devolver equipo")
        print("4. Consultar equipo")
        print("5. Salir")

        opcion = input("Elija una opción (1-5): ").strip()  # Captura la opción del menú

        try:
            if opcion == "1":
                codigo = input("Código del equipo: ")  # Solicita código
                nombre = input("Nombre del equipo: ")  # Solicita nombre
                cantidad = solicitar_entero("Cantidad inicial: ")  # Solicita y valida entero
                equipo = inventario.registrar_equipo(codigo, nombre, cantidad)  # Registra equipo
                print(f"[ÉXITO] Equipo registrado: {equipo}")  # Confirma el registro

            elif opcion == "2":
                codigo = input("Código del equipo a prestar: ")  # Solicita código
                equipo = inventario.buscar_equipo(codigo)  # Busca el equipo o lanza excepción
                cantidad = solicitar_entero("Cantidad a prestar: ")  # Solicita cantidad entera
                restantes = equipo.prestar(cantidad)  # Ejecuta el préstamo con validaciones
                print(f"[ÉXITO] Préstamo realizado. Disponibles: {restantes}")  # Muestra nuevo stock

            elif opcion == "3":
                codigo = input("Código del equipo a devolver: ")  # Solicita código
                equipo = inventario.buscar_equipo(codigo)  # Busca el equipo o lanza excepción
                cantidad = solicitar_entero("Cantidad a devolver: ")  # Solicita cantidad entera
                disponibles = equipo.devolver(cantidad)  # Ejecuta la devolución con validaciones
                print(f"[ÉXITO] Devolución registrada. Disponibles: {disponibles}")  # Muestra stock

            elif opcion == "4":
                codigo = input("Código del equipo a consultar: ")  # Solicita código
                equipo = inventario.buscar_equipo(codigo)  # Busca el equipo o lanza excepción
                print(f"[CONSULTA] {equipo}")  # Imprime la información del equipo

            elif opcion == "5":
                print("Finalizando la aplicación...")  # Mensaje de cierre del sistema
                break  # Sale del ciclo while

            else:
                # Maneja opciones fuera del rango 1-5 sin interrumpir el programa
                print("[AVISO] Seleccione una opción válida entre 1 y 5.")

        except (CantidadInvalidaError, StockInsuficienteError, EquipoNoEncontradoError) as err_negocio:
            # Atrapa las excepciones propias del dominio del inventario
            print(f"[ERROR DE REGLA] {err_negocio}")

        except ValueError as err_valor:
            # Atrapa errores de formato numérico, duplicados o campos obligatorios vacíos
            print(f"[ERROR DE DATO] {err_valor}")

        except Exception as err_general:
            # Captura cualquier otro error inesperado para mantener la estabilidad del programa
            print(f"[ERROR INESPERADO] {err_general}")

        finally:
            # Se ejecuta siempre al finalizar cada iteración del bloque try/except
            print("-" * 50)


# Ejecuta la función principal únicamente si el archivo se corre directamente
if __name__ == "__main__":
    ejecutar_sistema()  # Arranca el menú del sistema