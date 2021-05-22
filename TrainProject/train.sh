#!/bin/bash
python train.py --data dataSet/bdd100k-data1.yaml \
	     --hyp bdd100k/hyp.bdd100k1.yaml \
	     --cfg bdd100k/bdd100kx1.yaml \
	     --batch-size 80 \
	     --epochs 160 \
	     --weights ../weights/yolov5x.pt
