from flamapy.metamodels.fm_metamodel.transformations import UVLReader, GlencoeWriter, SPLOTWriter
import tempfile
import os
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsWriter
import shutil


def transformation(filepath):
    fm = UVLReader(filepath).transform()
    base_name = os.path.basename(filepath)
    base_name = base_name.replace(".uvl", "")
    static_path = os.path.dirname(filepath)
    # Transformation to json
    json = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    GlencoeWriter(json.name, fm).transform()
    file_path_json = os.path.join(static_path,  "type_json")
    os.makedirs(file_path_json, exist_ok=True)
    json_file_name = base_name + ".json"
    shutil.copy(json.name, os.path.join(file_path_json, json_file_name))
    # Transformation to splx
    splx = tempfile.NamedTemporaryFile(suffix='.splx', delete=False)
    SPLOTWriter(splx.name, fm).transform()
    file_path__splx = os.path.join(static_path,  "type_splx")
    os.makedirs(file_path__splx, exist_ok=True)
    splx_file_name = base_name + ".splx"
    shutil.copy(splx.name, os.path.join(file_path__splx, splx_file_name))
    # Transformation to cnf
    cnf = tempfile.NamedTemporaryFile(suffix='.cnf', delete=False)
    sat = FmToPysat(fm).transform()
    DimacsWriter(cnf.name, sat).transform()
    file_path_cnf = os.path.join(static_path,  "type_cnf")
    os.makedirs(file_path_cnf, exist_ok=True)
    cnf_file_name = base_name + ".cnf"
    shutil.copy(cnf.name, os.path.join(file_path_cnf, cnf_file_name))
    for temp_file in [json.name, splx.name, cnf.name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            pass


def delete_transformation(filepath):
    base_name = os.path.basename(filepath)
    base_name = base_name.replace(".uvl", "")
    static_path = os.path.dirname(filepath)

    #Delete json file
    folder_path_json = os.path.join(static_path,  "type_json")
    json_file_name = base_name + ".json"
    file_path_json = os.path.join(folder_path_json, json_file_name)
    os.remove(file_path_json)
    
    #Delete splx file
    folder_path_splx = os.path.join(static_path,  "type_splx")
    splx_file_name = base_name + ".splx"
    file_path_splx = os.path.join(folder_path_splx, splx_file_name)
    os.remove(file_path_splx)
    
    #Delete cnf file
    folder_path_cnf = os.path.join(static_path,  "type_cnf")
    cnf_file_name = base_name + ".cnf"
    file_path_cnf = os.path.join(folder_path_cnf, cnf_file_name)
    os.remove(file_path_cnf)
