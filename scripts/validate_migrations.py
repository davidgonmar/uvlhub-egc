import os
import re


def validate_migrations():
    base_dir = "migrations/versions"
    files = [f for f in os.listdir(base_dir) if f.endswith(".py")]

    revision_map = {}
    no_revise_files = []

    for file in files:
        path = os.path.join(base_dir, file)
        with open(path, "r") as f:
            content = f.read()

        # Extraer revision
        revision = re.search(r"revision\s*=\s*'([\w\d]+)'", content)
        if not revision:
            raise ValueError(f"Archivo {file} no contiene 'revision'")

        revision_id = revision.group(1)

        # Extraer down_revision, permitiendo tuplas o None
        revises = re.search(r"down_revision\s*=\s*(\([^\)]*\)|'[\w\d, ]+')", content)
        if revises:
            down_revision_str = revises.group(1).strip()
            print(f"Procesando archivo: {file} - down_revision_str: {down_revision_str}")  # Depuración

            # Verificar si down_revision tiene algún valor
            if down_revision_str:
                # Si está en formato tupla, se evalúa, de lo contrario, es una cadena simple
                if down_revision_str.startswith("(") and down_revision_str.endswith(")"):
                    try:
                        down_revision = eval(down_revision_str)  # Evaluamos como tupla
                        if isinstance(down_revision, tuple):
                            print(f"down_revision (tupla): {down_revision}")  # Depuración
                        else:
                            down_revision = None
                    except (SyntaxError, ValueError):
                        down_revision = None
                else:
                    # Si no está en formato tupla, lo tratamos como una cadena simple
                    down_revision = (down_revision_str.strip("'"),)  # Eliminar comillas extra
                    print(f"down_revision (cadena simple): {down_revision}")  # Depuración
            else:
                down_revision = None
        else:
            down_revision = None

        revision_map[revision_id] = down_revision

        # Solo agregar a no_revise_files si realmente no tiene down_revision
        if down_revision is None:
            no_revise_files.append(revision_id)

    # Mostrar los archivos sin down_revision para depuración
    print(f"Archivos sin down_revision: {no_revise_files}")

    # Validar que solo un archivo no tiene "down_revision"
    if len(no_revise_files) != 1:
        raise ValueError(f"Debe haber exactamente un archivo sin down_revision. Encontrados: {no_revise_files}")

    # Rastrear revisiones alcanzables desde la raíz
    root_revision = no_revise_files[0]
    reachable = set()
    stack = [root_revision]

    while stack:
        current = stack.pop()
        if current in reachable:
            raise ValueError("Se ha detectado un bucle en las referencias de revisiones.")
        reachable.add(current)

        # Agregar las revisiones conectadas hacia abajo
        for rev, down_revs in revision_map.items():
            if down_revs and current in down_revs:
                stack.append(rev)

        # Depuración: mostrar la revisión actual y las siguientes alcanzables
        print(f"Procesando revisión: {current} -> next_revisions: {revision_map.get(current)}")

    # Validar que todas las revisiones sean alcanzables
    all_revisions = set(revision_map.keys())
    if reachable != all_revisions:
        unreachable = all_revisions - reachable
        raise ValueError(f"Las siguientes revisiones no son alcanzables desde la raíz: {unreachable}")

    print("Validación completada con éxito. Todas las revisiones forman una cadena o grafo continuo.")


if __name__ == "__main__":
    validate_migrations()
