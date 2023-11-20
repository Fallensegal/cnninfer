
from cnninfer.dto.coco import COCOModelMeta

sparse_rcnn_meta = COCOModelMeta(
    name="srcnn",
    s3_bucket="postimages-srcnn",
    savefile_dir="./srcnn"
)

faster_rcnn_meta = COCOModelMeta(
    name="frcnn",
    s3_bucket="postimages-frcnn",
    savefile_dir="./frcnn"
)

detr_meta = COCOModelMeta(
    name="detr",
    s3_bucket="postimages-detr",
    savefile_dir="./detr"
)