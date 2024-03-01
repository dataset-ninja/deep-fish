from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "DeepFish"
PROJECT_NAME_FULL: str = "DeepFish Dataset"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.MIT(
    source_url="https://github.com/alzayats/DeepFish/blob/master/LICENSE"
)
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Research.Environmental(),
    Industry.Fishery(),
]
CATEGORY: Category = Category.Environmental(extra=[Category.Livestock()])

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.Classification(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.Counting(),
    CVTask.Localization(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2020

HOMEPAGE_URL: str = "https://alzayats.github.io/DeepFish/"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 14369556
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/deep-fish"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = (
    "http://data.qld.edu.au/public/Q5842/2020-AlzayatSaleh-00e364223a600e83bd9c3f5bcd91045-DeepFish/DeepFish.tar"
)
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = (
    "https://www.nature.com/articles/s41598-020-71639-x"
)
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {
    "GitHub": "https://github.com/alzayats/DeepFish"
}

CITATION_URL: Optional[str] = None
AUTHORS: Optional[List[str]] = [
    "Alzayat Saleh",
    "Issam Laradji",
    "Dmitry Konovalov",
    "Michael Bradley",
    "David Vazquez",
    "Marcus Sheaves",
]
AUTHORS_CONTACTS: Optional[List[str]] = ["alzayat.saleh@my.jcu.edu.au"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = [
    "James Cook University, Australia",
    "University of British Columbia, Canada",
    "Element AI, Canada",
]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = [
    "https://www.jcu.edu.au/",
    "https://www.ubc.ca/",
    "https://www.osler.com/",
]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "habitats": [
        "low complexity reef",
        "sandy mangrove prop roots",
        "complex reef",
        "seagrass bed",
        "low algal bed",
        "reef trench",
        "boulders",
        "mixed substratum mangrove - prop roots",
        "rocky mangrove - prop roots",
        "upper mangrove - medium rhizophora",
        "rock shelf",
        "mangrove - mixed pneumatophore prop root",
        "sparse algal bed",
        "muddy mangrove - pneumatophores and trunk",
        "large boulder and pneumatophores",
        "rocky mangrove - large boulder and trunk",
        "bare substratum",
        "upper mangrove - tall rhizophora",
        "large boulder",
        "muddy mangrove - pneumatophores",
    ],
    "__POSTTEXT__": "Additionally, some images marked with ***no fish*** and ***fish count*** tags",
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
