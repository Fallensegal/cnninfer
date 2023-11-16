from mmdet.apis import DetInferencer

sparse_rcnn = DetInferencer("sparse-rcnn_r50_fpn_1x_coco", device="cpu")
detr = DetInferencer("ddq-detr-4scale_r50_8xb2-12e_coco", device="cpu")
faster_rcnn = DetInferencer("faster-rcnn_r50_fpn_1x_coco", device="cpu")


