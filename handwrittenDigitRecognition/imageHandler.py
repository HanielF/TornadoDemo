from PIL import Image
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2
import mnist_train
import mnist_cnn as mnist_inference


# 将橙色的背景转换为黑色,将画笔的黑色转为白色
# input: RGBA格式图片数据
# output: 修改过的RGBA格式图片数据
def reveBlack(imageData):
    for i in range(0, len(imageData), 4):
        # 如果画笔为白色
        if imageData[i] == 0 and imageData[i + 1] == 0 and imageData[i +
                                                                     2] == 0:
            imageData[i] = imageData[i + 1] = imageData[i + 2] = 255
        # 如果背景为橙色
        if imageData[i] == 255 and imageData[i + 1] == 165 and imageData[
                i + 2] == 0:
            imageData[i] = imageData[i + 1] = imageData[i + 2] = 0
    return imageData


# 手写数字识别函数
# 输入: imageData,图片的RGBA数据数组,要求28*28像素,即数组大小为28*28*4=3136
def imageRecognize(imageData):
    # 背景转换为黑色,画笔转换为白色
    imageData = reveBlack(imageData)
    # 将图片数据转换为ndarray类型
    npData = np.array(imageData, dtype=np.uint8).reshape(28, 28, 4)
    # 将RGBA格式数组转换为图片
    image = Image.fromarray(npData, 'RGBA')
    # 保存临时图片
    image.save('static/images/npimg.png')

    # 用opencv读取图片的RGB数据
    rgbImage = cv2.imread('static/images/npimg.png', cv2.IMREAD_COLOR)
    # 将rgb图片转换为float32格式
    rgbImage = tf.image.convert_image_dtype(rgbImage, tf.float32)
    # 将图片灰度化得到(28,28,1)格式的tensor
    rgbImage = tf.image.rgb_to_grayscale(rgbImage)

    # 定义输入格式(1,28,28,1)
    x = tf.placeholder(
        tf.float32, [
            1, mnist_inference.IMAGE_SIZE, mnist_inference.IMAGE_SIZE,
            mnist_inference.NUM_CHANNEL
        ],
        name='x-input')
    # 直接通过调用封装好的函数来计算前向传播的结果
    y = mnist_inference.interence(x, None, None)

    # 使用tf.argmax(y, 1)就可以得到输入样例的预测类别
    prediction = tf.argmax(y, 1)

    # 通过变量重命名的方式来加载模型
    # 所有滑动平均的值组成的字典,处在/ExponentialMovingAverage下的值
    # 为了方便加载时重命名滑动平均量，tf.train.ExponentialMovingAverage类
    # 提供了variables_to_store函数来生成tf.train.Saver类所需要的变量
    # 这些值要从模型中提取
    variable_averages = tf.train.ExponentialMovingAverage(
        mnist_train.MOVING_AVERAGE_DECAY)
    variable_to_restore = variable_averages.variables_to_restore()
    saver = tf.train.Saver(variable_to_restore)

    # 用数据测试模型
    with tf.Session() as sess:
        # get_checkoutpoint_state()会通过checkoutpoint文件自动找到目录中最新模型的文件名
        ckpt = tf.train.get_checkpoint_state(mnist_train.MODEL_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            # 加载模型
            saver.restore(sess, ckpt.model_checkpoint_path)

            # 将tensor转换为np数组,这里也可以用np的reshape方法
            rgbNpData = tf.reshape(rgbImage, [
                1, mnist_inference.IMAGE_SIZE, mnist_inference.IMAGE_SIZE,
                mnist_inference.NUM_CHANNEL
            ])
            # 将tensor转换为ndarray
            reshaped_data = rgbNpData.eval(session=sess)
            # 将输入的测试数据格式调整为一个四维矩阵
            validate_feed = {x: reshaped_data}

            # 获得预测的结果数组
            predictionNum = sess.run(prediction, feed_dict=validate_feed)
            print("Number is %d" % (predictionNum[0]))

    tf.reset_default_graph()
    return predictionNum[0]
