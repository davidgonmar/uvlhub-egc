import json
import os
import shutil
from datetime import datetime, timedelta, timezone
import random
from dotenv import load_dotenv
from app.modules.auth.models import User
from app.modules.dataset.transformation_aux import transformation
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    Author
)

class DataSetSeeder(BaseSeeder):
    priority = 2

    def run(self):
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        ds_metrics = DSMetrics(number_of_models='5', number_of_features='50')
        seeded_ds_metrics = self.seed([ds_metrics])[0]

        custom_titles = [
            'Cats', 'Dog', 'Cats and Dogs', 'Never gonna give you up',
            'Monkeys', 'Lions', 'Tigers', 'Bears', 'Elephants', 'Giraffes'
        ]

        def random_date_within_last_three_years():
            today = datetime.now(timezone.utc)
            three_years_ago = today - timedelta(days=3 * 365)
            return three_years_ago + timedelta(days=random.randint(0, (today - three_years_ago).days))
        
                
        # Load dataset information from JSON file
        datasets_file = os.path.join(os.path.dirname(__file__), 'datasets.json')
        with open(datasets_file, 'r') as f:
            dataset_info = json.load(f)

        # Use the JSON data in your seeder
        ds_meta_data_list = [
            DSMetaData(
                deposition_id=1 + i,
                title=dataset_info[i]["title"],
                description=dataset_info[i]["description"],
                publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
                publication_doi=f'10.1234/dataset{i+1}',
                dataset_doi=f'10.1234/dataset{i+1}',
                tags=", ".join(dataset_info[i]["tags"]),
                ds_metrics_id=seeded_ds_metrics.id ) for i in range(len(custom_titles))
        ]    
        seeded_ds_meta_data = self.seed(ds_meta_data_list)

        authors = [
            Author(
                name=f'Author {i+1}',
                affiliation=f'Affiliation {i+1}',
                orcid=f'0000-0000-0000-000{i}',
                ds_meta_data_id=seeded_ds_meta_data[i % len(custom_titles)].id
            ) for i in range(len(custom_titles) * 2)
        ]
        self.seed(authors)

        datasets = [
            DataSet(
                user_id=user1.id if i % 2 == 0 else user2.id,
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=random_date_within_last_three_years()
            ) for i in range(len(custom_titles))
        ]
        seeded_datasets = self.seed(datasets)

        total_files = 30
        fm_meta_data_list = [
            FMMetaData(
                uvl_filename=f'file{i+1}.uvl',
                title=f'Feature Model {i+1}',
                description=f'Description for feature model {i+1}',
                publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
                publication_doi=f'10.1234/fm{i+1}',
                tags='tag1, tag2',
                uvl_version='1.0'
            ) for i in range(total_files)
        ]
        seeded_fm_meta_data = self.seed(fm_meta_data_list)

        fm_authors = [
            Author(
                name=f'Author {i+len(custom_titles)}',
                affiliation=f'Affiliation {i+len(custom_titles)}',
                orcid=f'0000-0000-0000-000{i+len(custom_titles)}',
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(total_files)
        ]
        self.seed(fm_authors)

        feature_models = [
            FeatureModel(
                data_set_id=seeded_datasets[i % len(custom_titles)].id,
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(total_files)
        ]
        seeded_feature_models = self.seed(feature_models)

        load_dotenv()
        working_dir = os.getenv('WORKING_DIR', '')
        src_folder = os.path.join(working_dir, 'app', 'modules', 'dataset', 'uvl_examples')

        file_distribution = [2, 2, 3, 5, 1, 2, 2, 4, 1, 2]
        current_file_index = 0
        for dataset_index, dataset in enumerate(seeded_datasets):
                user_id = dataset.user_id
                dest_folder = os.path.join(working_dir, 'uploads', f'user_{user_id}', f'dataset_{dataset.id}')
                os.makedirs(dest_folder, exist_ok=True)

                num_files = file_distribution[dataset_index] if dataset_index < len(file_distribution) else 0

                for file_number in range(num_files):
                    if current_file_index >= len(seeded_feature_models):
                        raise ValueError("Ran out of feature models to assign files.")
                    print(file_number)    
                    file_name = f'file{current_file_index + 1}.uvl'
                    feature_model = seeded_feature_models[current_file_index]
                    feature_model.data_set_id = dataset.id
                    self.seed([feature_model])

                    src_file_path = os.path.join(src_folder, file_name)
                    dest_file_path = os.path.join(dest_folder, file_name)

                    if os.path.exists(src_file_path):
                        shutil.copy(src_file_path, dest_file_path)
                    else:
                        with open(dest_file_path, 'w') as placeholder_file:
                            placeholder_file.write(f"Placeholder content for {file_name}")

                    uvl_file = Hubfile(
                        name=file_name,
                        checksum=f'checksum{current_file_index + 1}',
                        size=os.path.getsize(dest_file_path),
                        feature_model_id=feature_model.id
                    )
                    transformation(dest_file_path)
                    self.seed([uvl_file])
                    current_file_index += 1
