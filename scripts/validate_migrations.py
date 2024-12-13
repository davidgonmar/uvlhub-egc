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

        # Extraer revision y revises
        revision = re.search(r"revision\s*=\s*'([\w\d]+)'", content)
        revises = re.search(r"down_revision\s*=\s*'([\w\d]*)'", content)

        if not revision or not revises:
            raise ValueError(f"Archivo {file} no contiene revision o down_revision")

        revision_id = revision.group(1)
        down_revision = revises.group(1) or None

        revision_map[revision_id] = down_revision
        if down_revision is None:
            no_revise_files.append(file)

    # Validar que solo un archivo no tiene "down_revision"
    if len(no_revise_files) != 1:
        raise ValueError(f"Debe haber exactamente un archivo sin down_revision. Encontrados: {no_revise_files}")

    # Verificar que no haya bucles en la cadena de revisiones
    visited = set()
    current = list(revision_map.keys())[0]  # Iniciar desde el primer archivo

    while current:
        if current in visited:
            raise ValueError("Se ha detectado un bucle en las referencias de revisiones.")
        visited.add(current)
        current = revision_map[current]

    # Validar que todas las revisiones están conectadas
    if len(visited) != len(revision_map):
        raise ValueError("Las revisiones no forman una cadena continua.")

    print("Validación completada con éxito.")


if __name__ == "__main__":
    validate_migrations()
