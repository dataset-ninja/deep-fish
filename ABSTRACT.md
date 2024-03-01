The authors introduced **DeepFish Dataset** as a benchmark suite accompanied by a vast dataset tailored for training and evaluating various computer vision tasks. This dataset comprises roughly 40,000 images captured underwater across 20 distinct habitats in the tropical waters of Australia. Initially, the dataset solely featured classification labels. However, recognizing the need for a more comprehensive fish analysis benchmark, the authors augmented it by collecting segmentation labels. These labels empower models to autonomously monitor fish populations, pinpoint their locations, and estimate their sizes, thereby enhancing the dataset's utility for diverse analytical purposes.

## Motivation

Effective monitoring of fish populations in their natural habitats is essential for promoting sustainable fisheries practices. In regions like New South Wales, Australia, where the fisheries industry was valued at over 100 million Australian dollars in 2012–2014, such monitoring plays a crucial role. By providing insights into areas requiring protection and restoration, it helps maintain robust fish populations vital for both human consumption and environmental conservation. The automation of monitoring processes can significantly reduce labor costs and enhance efficiency, leading to positive sustainability outcomes and contributing to the preservation of a healthy ecosystem.

Deep learning techniques have consistently demonstrated remarkable performance in image analysis tasks. However, the automatic analysis of underwater fish habitats presents a unique and challenging application, demanding a sophisticated and accurate computer vision system. Extensive research endeavors have been directed towards developing such systems, aiming to understand the complexities of marine environments and differentiate between various fish species. These efforts rely on publicly available fish datasets. Nevertheless, existing datasets are limited in size and fail to fully capture the variability and intricacies of real-world underwater habitats. These habitats often feature adverse water conditions, significant resemblance between fish and background elements such as rocks, and occlusions among fish, posing additional challenges for accurate analysis.

## Dataset description

The authors introduce DeepFish as a benchmark specifically designed for analyzing fish in underwater marine environments, leveraging a dataset derived from in-situ field recordings. This dataset comprises around 40,000 high-resolution (1,920 × 1,080) images captured underwater across 20 distinct marine habitats in tropical Australia. These images span a wide range of coastal and nearshore benthic habitats commonly inhabited by fish species in the region, providing a comprehensive representation of underwater environments.

<img src="https://github.com/dataset-ninja/deep-fish/assets/120389559/b0dd14df-0e47-4c6a-b98e-a488f59fb1af" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Locations where the DeepFish images were acquired.</span>

Moreover, the authors extend beyond the initial classification labels by obtaining point-level and semantic segmentation labels, enabling additional computer vision tasks. These labels empower models to gain insights into fish habitats from various angles, including understanding fish behavior, monitoring population counts, and estimating their sizes and shapes. To assess the dataset's properties and establish preliminary results for this benchmark, state-of-the-art methods are evaluated using these labels.

<img src="https://github.com/dataset-ninja/deep-fish/assets/120389559/189815b8-ad7d-42b0-8c08-cbe80bfd5615" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">DeepFish image samples across 20 different habitats.</span>

The authors aimed to develop a benchmark that could significantly advance understanding of fish habitats. Consequently, they meticulously examined the quality of data acquisition, preparation, and annotation protocol. They began by selecting a dataset established by [Bradley and colleagues](https://jagworks.southalabama.edu/cgi/viewcontent.cgi?article=1060&context=usa_faculty_staff_pubs), which encompasses a vast collection of images (approximately 40 thousand) capturing a wide range of underwater fish habitats with high variability. The dataset's diversity and size render it well-suited for training and evaluating deep learning techniques. To enhance the dataset and create a more comprehensive testbed conducive to inspiring new, specialized algorithms for this problem domain, the authors tailored it accordingly, naming it DeepFish.

Videos for DeepFish were gathered across 20 habitats situated in remote coastal marine settings of tropical Australia. These videos were captured using cameras affixed to metal frames, strategically deployed over the side of a vessel to capture underwater footage. Submerged cameras were lowered to the seabed, where they recorded the natural fish community, while the vessel maintained a distance of 100 meters. The depth and precise map coordinates of the cameras were meticulously recorded using an acoustic depth sounder and GPS, respectively. Video recordings were conducted during daylight hours and under conditions of relatively low turbidity to ensure optimal visibility. The video clips were captured in full HD resolution (1,920 × 1,080 pixels) using a digital camera, resulting in a total of 39,766 frames. This method of image acquisition employs a low-disturbance approach, allowing for the accurate assessment of fish habitat associations in challenging and often inaccessible environments.

| Habitats                     | Fish Clf | Fish Loc | Fish Seg |
|------------------------------|----------|----------|----------|
| Low complexity reef          | 4,977    | 357      | 77       |
| Sandy mangrove prop roots    | 4,162    | 322      | 42       |
| Complex reef                 | 4,018    | 190      | 16       |
| Seagrass bed                 | 3,255    | 328      | 16       |
| Low algal bed                | 2,795    | 282      | 17       |
| Reef trench                  | 2,653    | 187      | 48       |
| Boulders                     | 2,314    | 227      | 16       |
| Mixed substratum mangrove    | 2,139    | 177      | 28       |
| Rocky Mangrove—prop roots    | 2,119    | 211      | 27       |
| Upper Mangrove               | 2,101    | 129      | 21       |
| Rock shelf                   | 1,848    | 186      | 19       |
| Mangrove                     | 1,542    | 157      | 33       |
| Sparse algal bed             | 1,467    | 0        | 0        |
| Muddy mangrove               | 1,117    | 113      | 79       |
| Large boulder and pneumatophores | 900     | 91       | 37       |
| Rocky mangrove—large boulder | 560      | 57       | 28       |
| Bare substratum              | 526      | 55       | 32       |
| Upper mangrove               | 475      | 49       | 28       |
| Large boulder                | 434      | 45       | 27       |
| Muddy mangrove               | 364      | 37       | 29       |
| **Total**                    | **39,766** | **3,200** | **620** |

<span style="font-size: smaller; font-style: italic;">DeepFish dataset statistics. Number of images annotated for each sub-dataset: FishClf for classification, FishLoc for counting/localization, and FishSeg for semantic segmentation.</span>

The original labels of the dataset are limited to classification tasks, providing binary information indicating the presence or absence of fish in each video frame, regardless of the fish count. While these labels serve a purpose in analyzing fish utilization across different habitats by categorizing images based on fish presence, they lack the granularity needed for detailed habitat analysis. To overcome this limitation, they obtained point-level and semantic segmentation labels. These additional annotations enable models to perform more advanced computer vision tasks such as object counting, localization, and segmentation. With these labels, the models can learn to accurately analyze and interpret the complexities of underwater habitats, facilitating a deeper understanding of fish dynamics and habitat characteristics.

## Dataset splits

The authors establish sub-datasets tailored for each specific computer vision task: FishClf for classification, FishLoc for counting and localization, and FishSeg for segmentation. To ensure robustness and representativeness in their splits, they implement a systematic approach rather than a random allocation method. Their approach involves partitioning the annotated images into training, validation, and test sets, considering the diversity of fish habitats and maintaining a balanced representation of fish populations across splits. Specifically, they initially categorize images within each habitat into those containing no fish (background) and those with at least one fish (foreground). Subsequently, they allocate 50% of images for training, 20% for validation, and 30% for testing for each habitat, ensuring an equal distribution of background and foreground images within each split. Afterward, the authors aggregate the selected training images from all habitats to form the training split for the dataset, following the same procedure for validation and testing splits. This meticulous approach results in a distinctive split comprising 19,883, 7,953, and 11,930 images (for training, validation, and test sets respectively) for FishClf, 1,600, 640, and 960 images for FishLoc, and 310, 124, and 186 images for FishSeg.



