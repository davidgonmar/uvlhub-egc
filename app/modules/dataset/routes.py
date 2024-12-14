import logging
import os
# import json
import re
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from zipfile import ZipFile
from app.modules.dataset.transformation_aux import transformation, delete_transformation
from app import db

from app.modules.featuremodel.services import FMRatingService
from flask import (
    redirect,
    render_template,
    request,
    jsonify,
    send_from_directory,
    make_response,
    abort,
    url_for,
    session
)
from flask_login import login_required, current_user

from app.modules.dataset.forms import DataSetForm
from app.modules.dataset.models import (
    DSDownloadRecord
)
from app.modules.dataset import dataset_bp
from app.modules.dataset.services import (
    AuthorService,
    DSDownloadRecordService,
    DSMetaDataService,
    DSViewRecordService,
    DataSetService,
    DSRatingService,
    DOIMappingService
)

from app.modules.zenodo.services import ZenodoService
from app.modules.fakenodo.services import FakenodoService
from app.modules.explore.services import ExploreService

logger = logging.getLogger(__name__)


dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
zenodo_service = ZenodoService()
fakenodo_service = FakenodoService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()
ds_rating_service = DSRatingService()
fm_rating_service = FMRatingService()


@dataset_bp.route("/dataset/upload", methods=["GET", "POST"])
@login_required
def create_dataset():
    form = DataSetForm()
    if request.method == "POST":
        dataset = None

        # Validate form submission
        if not form.validate_on_submit():
            return jsonify({"message": form.errors}), 400

        try:
            logger.info("Creating dataset...")
            dataset = dataset_service.create_from_form(form=form, current_user=current_user)
            logger.info(f"Created dataset: {dataset}")
            dataset_service.move_feature_models(dataset)
        except Exception as exc:
            logger.exception(f"Exception while creating dataset data locally: {exc}")
            return jsonify({"message": f"Exception while creating dataset: {str(exc)}"}), 400

        try:
            # Get the publication DOI (if provided) or fall back to dataset DOI
            publication_doi = form.publication_doi.data if form.publication_doi.data else None

            # Create a new deposition in Fakenodo (or Zenodo) using the dataset
            fakenodo_response_json = fakenodo_service.create_new_deposition(dataset, publication_doi=publication_doi)

            # Log the response for debugging purposes
            logger.info(f"Fakenodo response: {fakenodo_response_json}")

            # Check if the response contains the necessary deposition information (deposition_id and doi)
            if 'deposition_id' in fakenodo_response_json and 'doi' in fakenodo_response_json:
                deposition_id = fakenodo_response_json.get("deposition_id")  # Get the deposition ID
                deposition_doi = fakenodo_response_json.get("doi")  # Get the DOI from the response

                # Update dataset metadata with the deposition ID and DOI from Fakenodo
                dataset_service.update_dsmetadata(dataset.ds_meta_data_id,
                                                  deposition_id=deposition_id,
                                                  dataset_doi=deposition_doi)

                # Return success message with DOI
                return jsonify({
                    "status": "success",
                    "message": "Dataset successfully uploaded and DOI generated.",
                    "deposition_doi": deposition_doi
                }), 200
            else:
                # Handle failure case if no DOI or deposition ID is returned
                logger.error("Failed to create deposition, missing deposition_id or DOI.")
                return jsonify({"status": "error", "message": "Deposition creation failed, missing required information."}), 500

        except Exception as e:
            # Log and handle errors during the process
            logger.exception(f"Error while creating or processing the deposition: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


        # Delete temp folder
        file_path = current_user.temp_folder()
        if os.path.exists(file_path) and os.path.isdir(file_path):
            shutil.rmtree(file_path)

        msg = "Everything works!"
        return jsonify({"message": msg}), 200

    return render_template("dataset/upload_dataset.html", form=form)



@dataset_bp.route("/dataset/edit/<path:doi>/", methods=["GET", "POST"])
@login_required
def edit_dataset(doi):
    # Buscar el dataset por DOI
    ds_meta_data = dsmetadata_service.filter_by_doi(doi)

    # Si no se encuentra el dataset, devolver un error 404
    if not ds_meta_data:
        abort(404)

    # Obtener el dataset asociado
    dataset = ds_meta_data.data_set

    # Verificar que el usuario sea el propietario
    if dataset.user_id != current_user.id:
        return jsonify({"message": "You do not have permission to edit this dataset."}), 403

    # Solo permitir edición si está en modo borrador
    if not dataset.ds_meta_data.is_draft_mode and request.method == "POST":
        return jsonify({"message": "This dataset is already published and cannot be edited."}), 400

    if request.method == "POST":
        data = request.get_json()

        # Validar los datos recibidos
        title = data.get("title")
        description = data.get("description")
        tags = data.get("tags")
        publish = data.get("publish")  # Si el dataset debe publicarse

        if not title or not description:
            return jsonify({"message": "Title and description are required."}), 400

        try:
            # Actualizar los metadatos
            dataset.ds_meta_data.title = title
            dataset.ds_meta_data.description = description
            dataset.ds_meta_data.tags = ",".join(tags) if tags else dataset.ds_meta_data.tags

            # Publicar el dataset si corresponde
            if publish:
                dataset.ds_meta_data.is_draft_mode = False

            db.session.commit()
            return jsonify({"message": "Dataset updated successfully.", "is_draft_mode": dataset.ds_meta_data
                            .is_draft_mode}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    # Renderizar el HTML para editar el dataset (GET)
    return render_template("dataset/staging_area_dataset.html", dataset=dataset)


@dataset_bp.route("/dataset/list", methods=["GET", "POST"])
@login_required
def list_dataset():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )


@dataset_bp.route("/dataset/file/upload", methods=["POST"])
@login_required
def upload():
    file = request.files["file"]
    temp_folder = current_user.temp_folder()
    publication_doi = request.form.get("publication_doi")

    if not file or not file.filename.endswith(".uvl"):
        return jsonify({"message": "No valid file"}), 400

    if publication_doi:
        # Regex to check the DOI format "10.xxxx"
        if not re.match(r"^10\.\d{4}$", publication_doi):
            return jsonify({"message": "Invalid DOI format. Please enter a valid DOI like 10.xxxx"}), 400

    # create temp folder
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    file_path = os.path.join(temp_folder, file.filename)

    if os.path.exists(file_path):
        # Generate unique filename (by recursion)
        base_name, extension = os.path.splitext(file.filename)
        i = 1
        while os.path.exists(
            os.path.join(temp_folder, f"{base_name} ({i}){extension}")
        ):
            i += 1
        new_filename = f"{base_name} ({i}){extension}"
        file_path = os.path.join(temp_folder, new_filename)
    else:
        new_filename = file.filename

    try:
        file.save(file_path)
        transformation(file_path)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return (
        jsonify(
            {
                "message": "UVL uploaded and validated successfully",
                "filename": new_filename,
            }
        ),
        200,
    )


@dataset_bp.route("/dataset/file/delete", methods=["POST"])
def delete():
    data = request.get_json()
    filename = data.get("file")
    temp_folder = current_user.temp_folder()
    filepath = os.path.join(temp_folder, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        delete_transformation(filepath)
        return jsonify({"message": "File deleted successfully"})

    return jsonify({"error": "Error: File not found"})


@dataset_bp.route("/dataset/download/<int:dataset_id>", methods=["GET"])
def download_dataset(dataset_id):
    dataset = dataset_service.get_or_404(dataset_id)

    file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset_id}.zip")

    with ZipFile(zip_path, "w") as zipf:
        for subdir, dirs, files in os.walk(file_path):
            for file in files:
                full_path = os.path.join(subdir, file)

                relative_path = os.path.relpath(full_path, file_path)

                zipf.write(
                    full_path,
                    arcname=os.path.join(
                        os.path.basename(zip_path[:-4]), relative_path
                    ),
                )

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(
            uuid.uuid4()
        )  # Generate a new unique identifier if it does not exist
        # Save the cookie to the user's browser
        resp = make_response(
            send_from_directory(
                temp_dir,
                f"dataset_{dataset_id}.zip",
                as_attachment=True,
                mimetype="application/zip",
            )
        )
        resp.set_cookie("download_cookie", user_cookie)
    else:
        resp = send_from_directory(
            temp_dir,
            f"dataset_{dataset_id}.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

    # Check if the download record already exists for this cookie
    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        # Record the download in your database
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    return resp


@dataset_bp.route("/doi/<path:doi>/", methods=["GET"])
def subdomain_index(doi):

    # Check if the DOI is an old DOI
    new_doi = doi_mapping_service.get_new_doi(doi)
    if new_doi:
        # Redirect to the same path with the new DOI
        return redirect(url_for('dataset.subdomain_index', doi=new_doi), code=302)

    # Try to search the dataset by the provided DOI (which should already be the new one)
    ds_meta_data = dsmetadata_service.filter_by_doi(doi)

    if not ds_meta_data:
        abort(404)

    # Get dataset
    dataset = ds_meta_data.data_set

    # Save the cookie to the user's browser
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)

    average_rating = ds_rating_service.get_average_by_dataset(dataset.id) or 0.0
    user_rating = None
    if current_user.is_authenticated:
        user_rating_obj = ds_rating_service.get(dataset.id, current_user.id)
        user_rating = user_rating_obj.rating if user_rating_obj else 0

    fm_rating_data = {}
    for feature_model in dataset.feature_models:
        for _ in feature_model.files:
            file_average_rating = fm_rating_service.get_average_by_feature_model(feature_model.id) or 0.0
            file_user_rating = None
            if current_user.is_authenticated:
                file_user_rating_obj = fm_rating_service.get(feature_model.id, current_user.id)
                file_user_rating = file_user_rating_obj.rating if file_user_rating_obj else 0
            fm_rating_data[feature_model.id] = {
                'average_rating': round(file_average_rating, 2),
                'user_rating': file_user_rating or 0
            }

    resp = make_response(render_template(
        "dataset/view_dataset.html",
        dataset=dataset,
        average_rating=round(average_rating, 2),
        user_rating=user_rating or 0,
        fm_rating_data=fm_rating_data
    ))
    resp.set_cookie("view_cookie", user_cookie)

    return resp


@dataset_bp.route("/dataset/unsynchronized/<int:dataset_id>/", methods=["GET"])
@login_required
def get_unsynchronized_dataset(dataset_id):

    # Get dataset
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)

    if not dataset:
        abort(404)

    return render_template("dataset/view_dataset.html", dataset=dataset)


def create_and_send_zip(datasets, zip_name, include_files=None, include_folders=None):
    """
    Crea un archivo ZIP con los datasets especificados y lo envía como respuesta.

    :param datasets: Lista de datasets a incluir en el ZIP.
    :param zip_name: Nombre del archivo ZIP.
    :param include_files: Extensiones de archivos a incluir (ej: ['uvl']).
    :param include_folders: Subcarpetas a incluir para otros tipos de archivos (ej: ['type_cnf']).
    :return: Respuesta HTTP con el archivo ZIP adjunto.
    """
    # Crear una carpeta temporal para almacenar el archivo ZIP
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, zip_name)

    with ZipFile(zip_path, "w") as zipf:
        for dataset in datasets:
            dataset_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"
            if not os.path.exists(dataset_path):
                print(f"Skipping missing path: {dataset_path}")
                continue

            # Incluir archivos específicos en la raíz del dataset
            if include_files:
                for file in os.listdir(dataset_path):
                    if any(file.endswith(f".{ext}") for ext in include_files):
                        full_path = os.path.join(dataset_path, file)
                        relative_path = os.path.relpath(full_path, dataset_path)
                        zipf.write(full_path, arcname=os.path.join(str(dataset.id), relative_path))

            # Incluir archivos dentro de subcarpetas específicas
            if include_folders:
                for folder in include_folders:
                    specific_path = os.path.join(dataset_path, folder)
                    if not os.path.exists(specific_path):
                        print(f"Skipping missing folder: {specific_path}")
                        continue

                    for file in os.listdir(specific_path):
                        if any(file.endswith(f".{ext}") for ext in include_files):
                            full_path = os.path.join(specific_path, file)
                            relative_path = os.path.relpath(full_path, dataset_path)
                            zipf.write(full_path, arcname=os.path.join(str(dataset.id), relative_path))

    # Obtener o generar la cookie de usuario
    user_cookie = request.cookies.get("download_cookie", str(uuid.uuid4()))

    # Crear la respuesta con el archivo ZIP adjunto
    resp = make_response(
        send_from_directory(
            temp_dir,
            zip_name,
            as_attachment=True,
            mimetype="application/zip",
        )
    )
    resp.set_cookie("download_cookie", user_cookie)

    # Registrar la descarga
    for dataset in datasets:
        existing_record = DSDownloadRecord.query.filter_by(
            dataset_id=dataset.id,
            download_cookie=user_cookie
        ).first()

        if not existing_record:
            DSDownloadRecordService().create(
                user_id=None,
                dataset_id=dataset.id,
                download_date=datetime.now(timezone.utc),
                download_cookie=user_cookie,
            )

    # Limpiar el directorio temporal
    shutil.rmtree(temp_dir)

    return resp


@dataset_bp.route("/dataset/download_all", methods=["GET"])
def download_all_datasets():
    # Obtener todos los datasets
    datasets = dataset_service.get_all()

    # Descargar todos los datasets como un archivo ZIP
    return create_and_send_zip(datasets, "all_datasets.zip")


@dataset_bp.route("/dataset/download_relevant_datasets", methods=["GET"])
def download_all_relevant_datasets():
    # Filtrar datasets según los criterios almacenados en la sesión
    criteria = session.get('explore_criteria')
    datasets = ExploreService().filter(**criteria)

    if not datasets or not isinstance(datasets, list):
        return jsonify({"error": "No datasets provided or invalid format"}), 400

    # Determinar qué tipos de archivos incluir
    include_uvl = request.args.get("uvl", "false").lower() == "true"
    include_cnf = request.args.get("cnf", "false").lower() == "true"
    include_json = request.args.get("json", "false").lower() == "true"
    include_splx = request.args.get("splx", "false").lower() == "true"

    # Configurar extensiones y carpetas permitidas
    include_files = []
    include_folders = []

    if include_uvl:
        include_files.append("uvl")
    if include_cnf:
        include_files.append("cnf")
        include_folders.append("type_cnf")
    if include_json:
        include_files.append("json")
        include_folders.append("type_json")
    if include_splx:
        include_files.append("splx")
        include_folders.append("type_splx")

    if not include_files:
        return jsonify({"error": "No valid file types specified."}), 400

    # Descargar los datasets relevantes como un archivo ZIP
    return create_and_send_zip(datasets, "all_relevant_datasets.zip", include_files, include_folders)



@dataset_bp.route("/dataset/rate", methods=["POST"])
@login_required
def rate():
    data = request.get_json()
    dataset_id = data.get("dataset_id")
    rating = data.get("rating")

    if not dataset_id or not rating:
        return jsonify({"message": "Invalid request"}), 400

    ds_rating_service.create_or_update(dataset_id, current_user.id, rating)

    return jsonify({
        "message": "Rating saved successfully",
    }), 200


@dataset_bp.route("/dataset/publish/<path:doi>/", methods=["POST"])
@login_required
def publish_dataset(doi):
    # Buscar el dataset por DOI
    ds_meta_data = dsmetadata_service.filter_by_doi(doi)

    if not ds_meta_data:
        abort(404)

    dataset = ds_meta_data.data_set

    # Verificar que el usuario sea el propietario
    if dataset.user_id != current_user.id:
        return jsonify({"message": "You do not have permission to publish this dataset."}), 403

    # Verificar si ya está publicado
    if not dataset.ds_meta_data.is_draft_mode:
        return jsonify({"message": "This dataset is already published."}), 400

    try:
        # Publicar el dataset
        dataset.ds_meta_data.is_draft_mode = False
        db.session.commit()
        return jsonify({"message": "Dataset published successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
