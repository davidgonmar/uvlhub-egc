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
    
    if not os.path.exists(file_path_json):
        os.makedirs(file_path_json) 
    json_file_name = base_name + ".json"
    
    shutil.copy(json.name, os.path.join(file_path_json, json_file_name))
    
    # Transformation to splx
    splx = tempfile.NamedTemporaryFile(suffix='.splx', delete=False)
    
    SPLOTWriter(splx.name, fm).transform()
    file_path__splx = os.path.join(static_path,  "type_splx")
    
    if not os.path.exists(file_path__splx):
        os.makedirs(file_path__splx)  
    splx_file_name = base_name + ".splx"
    
    shutil.copy(splx.name, os.path.join(file_path__splx, splx_file_name))
    
    # Transformation to cnf
    cnf = tempfile.NamedTemporaryFile(suffix='.cnf', delete=False)
    
    sat = FmToPysat(fm).transform()
    DimacsWriter(cnf.name, sat).transform()
    
    file_path_cnf = os.path.join(static_path,  "type_cnf")
    if not os.path.exists(file_path_cnf):
        os.makedirs(file_path_cnf)
    cnf_file_name = base_name + ".cnf"
    
    shutil.copy(cnf.name, os.path.join(file_path_cnf, cnf_file_name))
    
    for temp_file in [json.name, splx.name, cnf.name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            pass
