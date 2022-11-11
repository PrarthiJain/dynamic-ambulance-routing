import datetime
import cv2
from utils import *
from darknet import Darknet
import numpy as np
from azure.storage.blob import BlobClient, ContainerClient
import tensorflow.compat.v1 as tf
from azure.identity import DefaultAzureCredential
from io import BytesIO, TextIOWrapper
import pytz
import sys

account_name = 'cs5412storage'
account_url = ""
account_key = ''
connection_string = ''

default_credential = DefaultAzureCredential()

container_name = sys.argv[1]
stream = BytesIO()
utc = pytz.UTC

container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container_name)
last = datetime.datetime(2021, 6, 13, 17, 57, 41, 613329, tzinfo=utc)

for blob in container.list_blobs():
    if blob.last_modified > last:
        last = blob.last_modified
        latest_blob = blob

blob_name = latest_blob.name
blob_client = BlobClient(account_url, container_name, blob_name, credential=account_key)
data = blob_client.download_blob()
blob_content = data.readall()

# # use numpy to construct an array from the bytes
x = np.fromstring(blob_content, dtype='uint8')

# decode the array into an image
image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
original_image = image
# # show it
# cv2.imshow("Image Window", img)


# path_name = sys.argv[1]
# image = cv2.imread(path_name)
# file_name = os.path.basename(path_name)
# filename, ext = file_name.split(".")


gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.98)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
PATH_TO_CKPT = 'frozen_inference_graph.pb'

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.98)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.compat.v1.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.compat.v1.import_graph_def(od_graph_def, name='')

    sess = tf.compat.v1.Session(graph=detection_graph)
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

image_expanded = np.expand_dims(image, axis=0)

# Perform the actual detection by running the model with the image as input
(boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                         feed_dict={image_tensor: image_expanded})

min_score_thresh = 0.8
ambulance = False
bb = np.squeeze(boxes)
ss = np.squeeze(scores)
# box=bb[0]
for i in range(bb.shape[0]):
    if ss is None or ss[i] > min_score_thresh:
        ambulance = True
        # box=bb[i]

if ambulance:
    print("EMV detected in...", blob_name)
    # Set the NMS Threshold
    score_threshold = 0.6
    # Set the IoU threshold
    iou_threshold = 0.4
    cfg_file = "cfg/yolov3.cfg"
    weight_file = "weights/yolov3.weights"
    namesfile = "data/coco.names"
    m = Darknet(cfg_file)
    m.load_weights(weight_file)
    class_names = load_class_names(namesfile)
    # m.print_network()
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(original_image, (m.width, m.height))
    # detect the objects
    boxes = detect_objects(m, img, iou_threshold, score_threshold)

    # plot the image with the bounding boxes and corresponding object class labels
    plot_boxes(original_image, boxes, class_names, plot_labels=True)

for blob in container.list_blobs():
    try:
        container.delete_blob(blob, if_unmodified_since=last)
    except:
        continue
