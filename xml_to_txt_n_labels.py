"""
while we have to train yolo and we have xmls files of annotations then we have to convert these xmls to txt and generate
two text files.

1) train.txt-- contain path of images for training
2) test.txt-- contain path of images for testing

---this file have function "generate_test_train_labels()". this done the job.

"""


import os
import shutil
import xml.etree.ElementTree as ET

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

image_names = []

def xml_to_txt(xml_folder=None,text_folder=None,class_label=None):
    if class_label == None:
        return
    xml_files = os.listdir(xml_folder)
    for x_file in xml_files:
        tree = ET.parse(xml_folder+'/'+x_file)
        root  = tree.getroot()
        width =int(root.find('size').find('width').text)
        height =int(root.find('size').find('height').text)
        with open(text_folder+x_file.split('.')[0]+".txt","w")as file:

            for object in root.findall('object'):

                xmin = int(object.find('bndbox').find('xmin').text)
                xmax = int(object.find('bndbox').find('xmax').text)
                ymin = int(object.find('bndbox').find('ymin').text)
                ymax = int(object.find('bndbox').find('ymax').text)
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((width,height), b)
                file.write(str(class_label) + " " + " ".join([str(a) for a in bb]) + '\n')


def generate_test_train_labels(path):
    folders = os.listdir(path)
    test_list = []
    folders.pop(0)
    os.mkdir(f"{path}textfiles")
    with open(f"{path}textfiles/train.txt", "w") as train_file:
        for folder in folders:
            if folder == "textfiles":continue
            subpath = path + folder + "/JPEGImages/"
            xml_to_txt(path+folder+"/Annotations/",path+folder+"/labels/",0)
            files = os.listdir(subpath)
            test_list.append(subpath + files[0])
            for file in files:
                train_file.writelines(subpath + file + '\n')
    with open(f"{path}textfiles/test.txt", "w") as test_file:
        for test in test_list:
            test_file.write(test+'\n')

generate_test_train_labels(path="./snack/")   # this function generates text files in labels folder from xml file and test,train text files

