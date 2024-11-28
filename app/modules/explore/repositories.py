import re
from sqlalchemy import any_, or_, func
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.repositories.BaseRepository import BaseRepository
from datetime import datetime
from sqlalchemy.orm import aliased


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=None, start_date="", end_date="",
               min_uvl="", max_uvl="", min_size=None, max_size=None, size_unit="KB", **kwargs):

        if tags is None:
            tags = []

        # Normaliza y limpia el texto de búsqueda
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
        for word in cleaned_query.split():
            filters.append(DSMetaData.title.ilike(f"%{word}%"))
            filters.append(DSMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(FMMetaData.uvl_filename.ilike(f"%{word}%"))
            filters.append(FMMetaData.title.ilike(f"%{word}%"))
            filters.append(FMMetaData.description.ilike(f"%{word}%"))
            filters.append(FMMetaData.publication_doi.ilike(f"%{word}%"))
            filters.append(FMMetaData.tags.ilike(f"%{word}%"))
            filters.append(DSMetaData.tags.ilike(f"%{word}%"))

        # Alias para Hubfile para poder hacer múltiples uniones
        hubfile_alias = aliased(Hubfile)

        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .outerjoin(DataSet.feature_models)  # Unión externa con FeatureModel
            .outerjoin(FeatureModel.fm_meta_data)  # Unión externa con FMMetaData
            .outerjoin(FeatureModel.files)  # Unión externa con archivos
            .outerjoin(hubfile_alias, hubfile_alias.feature_model_id == FeatureModel.id)  # Unión externa con Hubfile
            .group_by(DataSet.id)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Excluir datasets sin DOI
            )

        # Filtrado por tipo de publicación
        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        # Filtrado por tags
        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Filtrado por fechas
        def safe_parse_date(date, date_format, default_date=None):
            try:
                return datetime.strptime(date, date_format)
            except ValueError:
                return default_date

        date_format = '%Y-%m-%d'

        if start_date:
            date_obj = safe_parse_date(start_date, date_format)
            datasets = datasets.filter(func.date(DataSet.created_at) >= date_obj)

        if end_date:
            date_obj = safe_parse_date(end_date, date_format)
            datasets = datasets.filter(func.date(DataSet.created_at) <= date_obj)

        # Filtrar por cantidad de UVL
        if min_uvl.isdigit():
            datasets = datasets.group_by(DataSet.id).having(func.count(hubfile_alias.id)/2 >= int(min_uvl))

        if max_uvl.isdigit():
            datasets = datasets.group_by(DataSet.id).having(func.count(hubfile_alias.id)/2 <= int(max_uvl))

        # Ordenar por fecha de creación
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        def safe_convert_to_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        # Filtrado por tamaño (en KB, pero puede ser convertido a bytes si es necesario)
        def convert_to_bytes(size: float, unit: str):
            if size is None:
                return None
            if unit == "bytes":
                return size
            elif unit == "KB":
                return size * 1024
            elif unit == "MB":
                return size * 1024 * 1024
            elif unit == "GB":
                return size * 1024 * 1024 * 1024
            return None  # Manejo por defecto si la unidad es desconocida

        # Convertir tamaños mínimos y máximos a números válidos antes de pasarlos
        min_size = safe_convert_to_float(min_size)
        max_size = safe_convert_to_float(max_size)

        # Convertir tamaños a bytes según la unidad
        min_size = convert_to_bytes(min_size, size_unit) if min_size is not None else None
        max_size = convert_to_bytes(max_size, size_unit) if max_size is not None else None

        # Depuración
        print(f"Min Size: {min_size} bytes, Max Size: {max_size} bytes, Size Unit: {size_unit}")

        # Obtener todos los resultados y filtrar por tamaño usando get_file_total_size()
        # Después de la consulta inicial y la ordenación:
        filtered_datasets = []
        for dataset in datasets.all():
            # Obtener el tamaño total usando el método definido
            total_size = dataset.get_file_total_size()

            # Asegúrate de que los datos se impriman para depuración
            print(f"Dataset ID: {dataset.id}, Total size: {total_size} bytes")

            # Validar el rango del tamaño
            if min_size is not None and total_size <= min_size:
                print(f"Excluido por ser menor al mínimo ({min_size} bytes).")
                continue
            if max_size is not None and total_size >= max_size:
                print(f"Excluido por ser mayor al máximo ({max_size} bytes).")
                continue

            # Si pasa las condiciones, añadirlo a la lista final
            filtered_datasets.append(dataset)

        # Imprimir resumen del filtrado
        print(f"Total datasets mostrados: {len(filtered_datasets)}")

        for Dataset in datasets:
            print("Total size: " + str(Dataset.get_file_total_size()))

        return filtered_datasets
