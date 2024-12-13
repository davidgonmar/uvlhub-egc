import os
import re
import ast


def validate_migrations():
    base_dir = "migrations/versions"
    files = [f for f in os.listdir(base_dir) if f.endswith(".py")]

    revision_map = {}
    no_revise_files = []
    all_down_revisions = set()

    # Cargar las revisiones y construir el mapa de migraciones
    for file in files:
        path = os.path.join(base_dir, file)
        with open(path, "r") as f:
            content = f.read()

        # Buscar el 'revision' en el archivo
        revision = re.search(r"revision\s*=\s*'([\w\d]+)'", content)
        if not revision:
            raise ValueError(f"Archivo {file} no contiene 'revision'")

        revision_id = revision.group(1)

        # Buscar el 'down_revision' en el archivo
        revises = re.search(r"down_revision\s*=\s*(\([^\)]*\)|'[\w\d, ]+')", content)
        if revises:
            down_revision_str = revises.group(1).strip()

            if down_revision_str.startswith("(") and down_revision_str.endswith(")"):
                try:
                    down_revision = ast.literal_eval(down_revision_str)
                    if isinstance(down_revision, tuple):
                        down_revision = list(down_revision)
                    else:
                        down_revision = []
                except (SyntaxError, ValueError):
                    down_revision = []
            else:
                down_revision = [down_revision_str.strip("'")]
        else:
            down_revision = []

        revision_map[revision_id] = down_revision

        if not down_revision:
            no_revise_files.append(revision_id)
        else:
            all_down_revisions.update(down_revision)

    # Verificar que haya exactamente un archivo sin 'down_revision'
    if len(no_revise_files) != 1:
        raise ValueError("Debe haber exactamente un archivo HEAD (sin down_revision). " +
                         f"Encontrados: {len(no_revise_files)}")

    # Verificar que el número de revisiones y down_revisions únicas difiera en exactamente 1
    all_revisions = set(revision_map.keys())
    difference = len(all_revisions) - len(all_down_revisions)

    if difference != 1:
        raise ValueError(
            "Error en la cadena de migraciones, compruebe la sucesión de down_revisions. Debe acabar en un archivo " +
            "HEAD (down_revision = None)."
        )

    print("Validación completada con éxito. La lista de revisiones y down_revisions cumple con la condición.")


if __name__ == "__main__":
    validate_migrations()
