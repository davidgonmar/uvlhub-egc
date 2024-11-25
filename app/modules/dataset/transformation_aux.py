from flamapy.metamodels.fm_metamodel.transformations import UVLReader, GlencoeWriter
import tempfile
import os

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
    for temp_file in [json.name]:
        try:
            os.remove(temp_file)
        except FileNotFoundError:
            pass
