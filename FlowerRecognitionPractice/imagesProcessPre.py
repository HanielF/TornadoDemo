'''
参考链接：
https://www.aiuai.cn/aifarm305.html
https://blog.csdn.net/XUEER88888888888888/article/details/86666614
https://blog.csdn.net/GAN_player/article/details/76559358
https://www.cnblogs.com/uestc-mm/p/7325449.html
https://blog.csdn.net/qq_38269799/article/details/80723718
https://www.cnblogs.com/zhangfengxian/p/10645332.html
tf.data
https://blog.csdn.net/u014061630/article/details/80728694
'''

from PIL import Image
import os
import tensorflow as tf

source_dir = "./static/images/Marigold/"
target_dir = "./static/images/CMarigold/"

# 功能：返回目录中所有JPG 图像的文件名列表获取文件名列表
# 参数：dirPath，目录名
def get_imlist(dirPath: str):
    return [os.path.join(dirPath, f) for f in os.listdir(dirPath) if f.endswith('.jpg')]


# 功能：调整图片尺寸为299*299
# 参数：imageName，包含目录名的图片名路径
def imageResize(imageName: str):
    im = Image.open(imageName)
    im = im.resize((299,299))
    im.save(imageName)


# 功能：对传入路径的图片进行处理，每张图片进行缩放、上下反转、左右反转、沿对角线反转、亮度饱度和色相随机调整
# 参数：imagePath，图片所在目录名
def imageProcess(Path: str):
    # 获取文件名列表
    imlist = get_imlist(Path)
    # 构造文件队列 string_input_producer会产生一个文件名队列
    file_queue = tf.train.string_input_producer(imlist)
    # 构造一个阅读器读取图片内容（默认读一张）reader从文件名队列中读数据。对应的方法是reader.read
    reader = tf.WholeFileReader()
    key,value = reader.read(file_queue)
    # 对读取的图片进行解码
    image = tf.image.decode_jpeg(value)
    # 批处理
#    image_batch = tf.train.batch([image],batch_size=10,num_threads=1,capacity=10)

    with tf.Session() as sess:
        # tf.train.string_input_producer定义了一个epoch变量，要对它进行初始化
        sess.run(tf.local_variables_initializer())
        # 协同启动的线程
        coord = tf.train.Coordinator() 
        # 启动线程运行队列, 使用start_queue_runners之后，才会开始填充队列
        threads = tf.train.start_queue_runners(sess=sess, coord=coord) 
        sess.run([image])
        # 停止所有的线程
        coord.request_stop() 
        coord.join(threads)

        # 修改图片数据类型
        image_uint8 = tf.image.convert_image_dtype(image, dtype = tf.uint8)

        # 修改图片尺寸
        image_resized = tf.image.resize_images(image_uint8,[299,299],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        encode_resized = tf.image.encode_jpeg(image_resized)
        # 左右翻转
        image_flipLR = tf.image.flip_left_right(image_resized)
        encode_flipLR = tf.image.encode_jpeg(image_flipLR)
        # 上下翻转
        image_flipUD = tf.image.flip_up_down(image_resized)
        encode_flipUD = tf.image.encode_jpeg(image_flipUD)
        # 对角线翻转
        image_flipX = tf.image.transpose_image(image_resized) 
        encode_flipX = tf.image.encode_jpeg(image_flipX)

        # 亮度在[-max_delta, max_delta)的范围随机调整
        image_random = tf.image.random_brightness(image_resized, max_delta=0.5)
        # 色相在[-max_delta, max_delta]的范围随机调整, max_delta取值为[0, 0.5]
        image_random = tf.image.random_hue(image_random, 0.5)
        # 饱和度在[lower, upper]的范围随机调整
        image_random = tf.image.random_saturation(image_random, 0, 5)
        encode_random=tf.image.encode_jpeg(image_random)

        print(image_random.eval())

        # for i in range(100):
        #     with tf.gfile.GFile(target_dir+str(i)+"_resized"+".jpg","wb") as f1:
        #         f1.write(encode_resized[i].eval())

        #     with tf.gfile.GFile(target_dir+str(i)+"_LR"+".jpg","wb") as f2:
        #         f2.write(encode_flipLR[i].eval())

        #     with tf.gfile.GFile(target_dir+str(i)+"_UD"+".jpg","wb") as f3:
        #         f3.write(encode_flipUD[i].eval())

        #     with tf.gfile.GFile(target_dir+str(i)+"_X"+".jpg","wb") as f4:
        #         f4.write(encode_flipX[i].eval())

        #     with tf.gfile.GFile(target_dir+str(i)+"_random"+".jpg","wb") as f5:
        #         f5.write(encode_random[i].eval())


if __name__=='__main__':
    # 如果目标目录不存在，则创建新目录
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    imageProcess(source_dir)

    