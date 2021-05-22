import ijson
from pathlib import Path

dw = 1280
dh = 720
all_categories = ["person", "car", "bus", "truck","motor","rider","bike","traffic sign"]
label2id =  {"person": 0,"car": 1,"bus": 2,"truck": 3,"motor":4,"rider":4, "bike":4,"traffic sign":5} 

label_train = Path('./bdd100k/labels/100k/train')
label_val = Path('./bdd100k/labels/100k/val')

def _filter_by_box(w, h):
    #size ratio 
    #过滤到过于小的小目标
    threshold = 0.001
    if float(w*h)/(dw*dh) < threshold:
        return True 
    return False 

def parse_json(path, for_train=True):
    with open(path, 'r', encoding='utf-8') as f:
        if for_train:
            f_prefix = label_train
        else:
            f_prefix = label_val
        objects = ijson.items(f, 'item')
        while True:
            try:
                k = objects.__next__()
                fp_path = Path(k['name'])
                label_list = []
                for label in k['labels']:
                    if 'box2d' in label.keys() and label['category'] in all_categories:
                        index = label2id[label["category"]]
                        wH  = label["box2d"]["x2"] - label["box2d"]["x1"]
                        hH  = label["box2d"]["y2"] - label["box2d"]["y1"]
                        if(_filter_by_box(wH, hH)):
                            continue
                        cx = float(label["box2d"]["x1"] + label["box2d"]["x2"]) / 2.0 / dw
                        cy = float(label["box2d"]["y1"] + label["box2d"]["y2"]) / 2.0 / dh
                        w = float(label["box2d"]["x2"] - label["box2d"]["x1"]) / dw
                        h = float(label["box2d"]["y2"] - label["box2d"]["y1"]) / dh
                        if w <= 0 or h <= 0:
                            continue
                        # 根据图片尺寸进行归一化 在上面
                        # cx, cy, w, h = cx * dw, cy * dh, w * dw, h * dh
                        line = str(index) + ' ' + str(round(cx, 6)) + ' ' + str(round(cy, 6)) + ' ' + str(
                            round(w, 6)) + ' ' + str(round(h, 6)) + '\n'
                        label_list.append(line)
                with open(f_prefix / fp_path.with_suffix('.txt'), 'w') as label_fh:
                    for line in label_list:
                        label_fh.write(line)
                #print(str(fp_path)+"  done.")
            except StopIteration as e:
                print("数据读取完成")
                break


if __name__ == "__main__":
    # bdd_label_dir = "./BDD100K/train"
    # cvt = Bdd2yolov5()
    # for path in search_file(bdd_label_dir, r"\.json$"):
    #     cvt.bdd2yolov5(path)
    # cvt = Bdd2yolov5()
    parse_json('./bdd100k_labels_images_train.json', True)
    parse_json('./bdd100k_labels_images_val.json', False)
