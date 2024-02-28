import csv
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    batch_size = 30

    pre_ds_to_path = {
        "Segmentation": "/home/alex/DATASETS/TODO/DeepFish/Segmentation",
        "Classification": "/home/alex/DATASETS/TODO/DeepFish/Classification",
        "Localization": "/home/alex/DATASETS/TODO/DeepFish/Localization",
    }

    images_folder = "images"
    masks_folder = "masks"

    def create_ann(image_path):
        labels = []
        tags = []

        img_height = 1080
        img_wight = 1920

        habitat_val = im_path_to_habitat[image_path]
        habitat_meta = index_to_meta[habitat_val]
        habitat_tag = sly.Tag(habitat_meta)
        tags.append(habitat_tag)

        if len(image_path.split("empty")) > 1:
            empty_tag = sly.Tag(no_fish_meta)
            tags.append(empty_tag)

        if ds_pre_name == "Localization":
            counts_val = im_path_to_count[image_path]
            counts_tag = sly.Tag(count_fish_meta, value=counts_val)
            tags.append(counts_tag)

        mask_path = image_path.replace(images_folder, masks_folder).replace(".jpg", ".png")

        if file_exists(mask_path) and ds_pre_name != "Localization":
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            mask = mask_np == 255
            ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
            for i in range(1, ret):
                obj_mask = curr_mask == i
                curr_bitmap = sly.Bitmap(obj_mask)
                if curr_bitmap.area > 100:
                    curr_label = sly.Label(curr_bitmap, obj_class)
                    labels.append(curr_label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    obj_class = sly.ObjClass("fish", sly.Bitmap)

    no_fish_meta = sly.TagMeta("no fish", sly.TagValueType.NONE)
    count_fish_meta = sly.TagMeta("fish count", sly.TagValueType.ANY_NUMBER)

    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=[no_fish_meta, count_fish_meta])

    index_to_habitat = [
        ("7482", "Low complexity reef"),
        ("7398", "Sandy mangrove prop roots"),
        ("7426", "Complex reef"),
        ("7463", "Seagrass bed"),
        ("7434", "Low algal bed"),
        ("7623", "Reef trench"),
        ("7490", "Boulders"),
        ("7585", "Mixed substratum mangrove - prop roots"),
        ("7117", "Rocky Mangrove - prop roots"),
        ("7393", "Upper Mangrove - medium Rhizophora"),
        ("9907", "Rock shelf"),
        ("9894", "Mangrove - mixed pneumatophore prop root"),
        ("7268", "Sparse algal bed"),
        ("9866", "Muddy mangrove - pneumatophores and trunk"),
        ("9908", "Large boulder and pneumatophores"),
        ("9898", "Rocky mangrove - large boulder and trunk"),
        ("9892", "Bare substratum"),
        ("9852", "Upper mangrove - tall rhizophora"),
        ("9862", "Large boulder"),
        ("9870", "Muddy mangrove - pneumatophores"),
    ]

    index_to_meta = {}
    for i in index_to_habitat:
        tag_meta = sly.TagMeta(i[1].lower(), sly.TagValueType.NONE)
        meta = meta.add_tag_meta(tag_meta)
        index_to_meta[i[0]] = tag_meta

    api.project.update_meta(project.id, meta.to_json())

    for ds_pre_name, path in pre_ds_to_path.items():

        for splitter in ["train.csv", "val.csv", "test.csv"]:

            ds_name = ds_pre_name.lower() + " " + get_file_name(splitter)
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

            split_path = os.path.join(path, splitter)

            im_path_to_habitat = {}
            im_path_to_count = {}
            with open(split_path, "r") as file:
                csvreader = csv.reader(file)
                for idx, row in enumerate(csvreader):
                    if idx == 0:
                        continue
                    if ds_pre_name == "Localization":
                        im_path_to_habitat[os.path.join(path, images_folder, row[0] + ".jpg")] = (
                            row[2]
                        )
                        im_path_to_count[os.path.join(path, images_folder, row[0])] = int(row[1])
                    elif ds_pre_name == "Classification":
                        im_path_to_habitat[os.path.join(path, row[0] + ".jpg")] = row[1]
                    else:
                        im_path_to_habitat[os.path.join(path, images_folder, row[0] + ".jpg")] = (
                            row[1]
                        )

            images_pathes = list(im_path_to_habitat.keys())

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

            for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
                img_names_batch = [get_file_name(im_path) + ".jpg" for im_path in img_pathes_batch]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns_batch = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))

    return project
