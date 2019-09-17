from PIL import Image
import os
import tensorflow as tf

# 图片存放路径和目标路径
source_dir = "./static/images/Pansy/"
target_dir = "./static/images/Enhanced-Pansy/"

# 功能：返回目录中所有JPG 图像的文件名列表获取文件名列表
# 参数：dirPath，目录名
def get_imlist(dirPath: str):
    return [os.path.join(dirPath, f) for f in os.listdir(dirPath) if f.endswith('.jpg')]


# 功能：对传入路径的图片进行处理，每张图片进行缩放、上下反转、左右反转、沿对角线反转、亮度饱度和色相随机调整
# 参数：imagePath，图片所在目录名
def imageProcess(Path: str):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    imlist = get_imlist(Path)

    with tf.Session() as sess:
        print("正在处理： "+source_dir)
        for i in range(100):
            image_raw_data = tf.gfile.FastGFile(imlist[i],'rb').read()
            imgData = tf.image.decode_jpeg(image_raw_data)

            # 调整尺寸
            image_resized = tf.image.resize_images(imgData,[299,299],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            encode_resized = tf.image.encode_jpeg(image_resized)
            # 左右翻转
            flipLR = tf.image.flip_left_right(image_resized)
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
            # 如果是0.5的随机调整色相，会比较大，修改为[0, 0.1]
            image_random = tf.image.random_hue(image_random, 0.1)
            # 饱和度在[lower, upper]的范围随机调整
            image_random = tf.image.random_saturation(image_random, 0, 5)
            encode_random=tf.image.encode_jpeg(image_random)

            with tf.gfile.GFile(target_dir+str(i)+"_resized"+".jpg","wb") as f:
                f.write(encode_resized.eval())
            with tf.gfile.GFile(target_dir+str(i)+"_LR"+".jpg","wb") as f:
                f.write(encode_flipLR.eval())
            with tf.gfile.GFile(target_dir+str(i)+"_UD"+".jpg","wb") as f:
                f.write(encode_flipUD.eval())
            with tf.gfile.GFile(target_dir+str(i)+"_X"+".jpg","wb") as f:
                f.write(encode_flipX.eval())
            with tf.gfile.GFile(target_dir+str(i)+"_random"+".jpg","wb") as f:
                f.write(encode_random.eval())

        print("处理结束： "+source_dir)

if __name__=='__main__':
    imageProcess(source_dir)