import click
import requests

BASE_URL = "http://localhost:5000/lista/v1"


@click.group()
def todo():
    """
    Aplicación de gestión de tareas cliente.
    Utiliza comandos para interactuar con el servidor.
    """
    pass


@todo.command()
@click.argument("description")
@click.argument("status", type=bool)
def add(description, status):
    """
    Añade una nueva tarea con la descripción y estado proporcionados.
    Uso: add "descripcion" True|False
    """
    response = requests.post(f"{BASE_URL}/tareas",
                             json={"descripcion": description,
                                   "completada": status})
    if response.status_code == 201:
        print("Nueva tarea añadida:")
        tarea = response.json()["tarea"]
        print(f"URI: {tarea['uri']} - {tarea['descripcion']} -",
              'Completada' if tarea['completada'] else 'Pendiente')
    else:
        print("Error al añadir la nueva tarea.")
        print("Código de estado:", response.status_code)


@todo.command()
def list():
    """
    Obtiene la lista completa de tareas desde el servidor.
    Uso: list
    """
    response = requests.get(f"{BASE_URL}/tareas")
    if response.status_code == 200:
        tareas = response.json()["tareas"]
        if not tareas:
            print("No hay tareas en la lista.")
        else:
            for tarea in tareas:
                print(f"URI: {tarea['uri']} - {tarea['descripcion']} -",
                      'Completada' if tarea['completada'] else 'Pendiente')
    else:
        print("Error al obtener la lista de tareas.")
        print("Código de estado:", response.status_code)


@todo.command()
@click.argument("task_id", type=int)
def check(task_id):
    """
    Marca la tarea con el ID proporcionado como completada.
    Uso: check <id>
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}",
                            json={"completada": True})
    if response.status_code == 200:
        print(f"Tarea {task_id} marcada como completada.")
    elif response.status_code == 404:
        print(f"Error: la tarea {task_id} no existe.")
    else:
        print(f"Error al marcar la tarea {task_id} como completada.")
        print("Código de estado:", response.status_code)


# comados nuevos

@todo.command()
@click.argument("task_id", type=int)
def uncheck(task_id):
    """
    Marca la tarea con el ID proporcionado como NO completada.
    Uso: uncheck <id>
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}",
                            json={"completada": False})
    if response.status_code == 200:
        print(f"Tarea {task_id} marcada como NO completada.")
    elif response.status_code == 404:
        print(f"Error: la tarea {task_id} no existe.")
    else:
        print(f"Error al marcar la tarea {task_id} como no completada.")
        print("Código de estado:", response.status_code)


@todo.command()
@click.argument("task_id", type=int)
def delete(task_id):
    """
    Borra la tarea indicada de la lista.
    Uso: delete <id>
    """
    response = requests.delete(f"{BASE_URL}/tarea/{task_id}")
    if response.status_code == 200:
        print(f"Tarea {task_id} eliminada correctamente.")
    elif response.status_code == 404:
        print(f"Error: la tarea {task_id} no existe.")
    else:
        print(f"Error al eliminar la tarea {task_id}.")
        print("Código de estado:", response.status_code)


@todo.command()
@click.argument("task_id", type=int)
@click.argument("new_description")
def edit(task_id, new_description):
    """
    Modifica la descripción de una tarea existente.
    Uso: edit <id> \"nueva descripcion\"
    (si tiene espacios, usar comillas)
    """
    response = requests.put(f"{BASE_URL}/tarea/{task_id}",
                            json={"descripcion": new_description})
    if response.status_code == 200:
        print(f"Descripción de la tarea {task_id} actualizada a: {new_description}")
    elif response.status_code == 404:
        print(f"Error: la tarea {task_id} no existe.")
    else:
        print(f"Error al actualizar la tarea {task_id}.")
        print("Código de estado:", response.status_code)





if __name__ == "__main__":
    todo()
