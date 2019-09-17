import glob
import tensorflow as tf
import numpy as np
import data_process
from PIL import Image
import matplotlib.pyplot as plt

# 模型目录
TRAINMODEL_FILE = 'train_dir/model.pb'
INCEPTION_FILE = 'inceptionV3/tensorflow_inception_graph.pb'
# inception-v3 模型中代表瓶颈层结果的张量名称
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
# 图像输入张量所对应的名称
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'


# 图片预处理与显示
def imgPreTreatment(imgPath):
    img = Image.open(imgPath)
    # 使用PIL缩放图片
    out = img.resize((299, 299),Image.ANTIALIAS)
    out.save(imgPath)
    plt.figure("Image") # 图像窗口名称
    plt.imshow(out)
    plt.axis('on') # 关掉坐标轴为 off
    plt.title('image') # 图像题目
    plt.show()   

# 识别函数
def flowerRecognization(imgPath):
    with tf.Session() as sess:
        # 导入inceptionV3模型,并返回数据输入张量和瓶颈层输出张量
        with tf.gfile.FastGFile(INCEPTION_FILE, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(graph_def, name='', return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])
        # 读取数据
        image_raw_data = tf.gfile.FastGFile('./tmp.jpg', 'rb').read()
        # 读取并解析图片，使用inception-v3处理图片获取特征向量
        image_value = sess.run(bottleneck_tensor, {jpeg_data_tensor: image_raw_data})
        # 将图片转化为299*299以方便inception-v3模型来处理，将四维数组压缩成一维数组
        # 由于全连接层输入时有batch的维度，所以用列表作为输入
        image_value = np.squeeze(image_value)
        print(image_value.shape)

    with tf.Session() as sess:
        # 导入已经训练好的模型，并返回输入张量和final_tensor的结果张量
        with tf.gfile.FastGFile(TRAINMODEL_FILE, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            input_data, predict_res = tf.import_graph_def(graph_def, name='',return_elements=['BottleneckInputPlaceholder:0','output/prob:0'])
            # Cannot feed value of shape (2048,) for Tensor 'BottleneckInputPlaceholder:0', which has shape '(?, 2048)'
            # 所以feed_dict中input_data需要加中括号
            # predict_res 是模型中的final_tensor
            predict_res = sess.run(predict_res, feed_dict={input_data: [image_value]})
            label_res = np.argmax(predict_res)
    
    # 读取labels标签和结果的数字对应
    labels = np.load('./flower_processed_data.npy')[6]
    print(labels)
    print("Flower recognition: 结果为 "+labels[label_res])
    return labels[label_res]



