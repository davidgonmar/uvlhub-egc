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
        min_uvl="", max_uvl="", min_size=None, max_size=None, size_unit="bytes", **kwargs):

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
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .join(FeatureModel.files)
            .join(hubfile_alias, hubfile_alias.feature_model_id == FeatureModel.id)  # Primer unión de Hubfile
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
            datasets = datasets.group_by(DataSet.id).having(func.count(hubfile_alias.id) <= int(max_uvl))

        # Filtrado por tamaño
        def convert_to_bytes(size: float, unit: str) -> int:
            units = {
                "bytes": 1,
                "KB": 1024,
                "MB": 1024 ** 2,
                "GB": 1024 ** 3,
            }
            return int(size * units.get(unit, 1))

        if min_size:
            min_size_bytes = convert_to_bytes(float(min_size), size_unit)
        else:
            min_size_bytes = 0  # Valor predeterminado para min_size

        if max_size:
            max_size_bytes = convert_to_bytes(float(max_size), size_unit)
        else:
            max_size_bytes = float('inf')  # Valor predeterminado para max_size (sin límite superior)

        if min_size_bytes > 0:
            datasets = datasets.having(func.sum(hubfile_alias.size) >= min_size_bytes)

        if max_size_bytes < float('inf'):
            datasets = datasets.having(func.sum(hubfile_alias.size) <= max_size_bytes)

        # Ordenar por fecha de creación
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()


