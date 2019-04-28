### canvas画笔位置有偏移
- 使用`window.innerHeight || document.documentElement.clientHeight`语句获取视窗高度，同理获得宽度
- 移动端获得视窗的高度和宽度后，根据高视窗的大小设置canvas大小，以及下方按钮文字等大小
- PC端通过canvas的`mousedown、mousemove、mouseup`这三个事件绘图，画笔的起始点和新点用`event.clientX - canvas.offsetLeft`获取x，同理获取y,
- 移动端用`touchstart、touchmove、touchend`这三个事件，画笔的起始点和终点都用`event.targetTouches[0].clientX - canvas.offsetLeft`获取x，`event.targetTouches[0].clientY - canvas.offsetTop`获取y

### canvas用二次贝塞尔曲线绘图
**PC端mousemove事件代码**

```javascript
//PC端鼠标移动
function draw(event) {
  if (onoff == true) {
    //获取新点和中点
    var newx = event.clientX - canvas.offsetLeft;
    var newy = event.clientY - canvas.offsetTop;
    midx = 0.5*(newx+oldx);
    midy = 0.5*(newy+oldy);

    //设置粗细和颜色
    ctx.lineWidth = linew;
    ctx.strokeStyle = linecolor;
    ctx.lineCap = 'round';

    //绘制二次贝塞尔
    ctx.moveTo(oldx,oldy);
    ctx.quadraticCurveTo( midx , midy , newx , newy );
    ctx.stroke();

    //转移新旧坐标
    oldx = newx;
    oldy = newy;
  };
}
```

**mobile端mousemove事件代码**

```javascript
//移动端手指移动
function tMove(event){
  //获取新点和中点
  var touche = event.targetTouches[0];
  var newx = touche.clientX - canvas.offsetLeft;
  var newy = touche.clientY - canvas.offsetTop;
  midx = 0.5*(newx+oldx);
  midy = 0.5*(newy+oldy);

  //设置粗细和颜色
  ctx.lineWidth = linew;
  ctx.strokeStyle = linecolor;
  ctx.lineCap = 'round'

  ctx.beginPath();
  ctx.moveTo(oldx,oldy);
  ctx.quadraticCurveTo(midx,midy,newx,newy);
  ctx.stroke();

  oldx = newx;
  oldy = newy;
}
```

### canvas的imageData像素级缩放
想要获得canvas上的图像并且缩放到28*28，使用scale方法是不行的，必须获取所有的像素RGBA值，然后横向隔一段取一个点，竖向隔几行取一行，一共横向每行取28个像素点，竖向取28行

代码如下：

```javascript
//缩放imageData,scale:倍数,返回:imageData
function scaleImageData(imageData, scale) {
  var scaled =
      ctx.createImageData(imageData.width * scale, imageData.height * scale);
  for (var row = 0; row < imageData.height; row++) {
    for (var col = 0; col < imageData.width; col++) {
      var sourcePixel = [
        imageData.data[(row * imageData.width + col) * 4 + 0],
        imageData.data[(row * imageData.width + col) * 4 + 1],
        imageData.data[(row * imageData.width + col) * 4 + 2],
        imageData.data[(row * imageData.width + col) * 4 + 3]
      ];
      for (var y = 0; y < scale; y++) {
        var destRow = Math.floor(row * scale) + y;
        for (var x = 0; x < scale; x++) {
          var destCol = Math.floor(col * scale) + x;
          for (var i = 0; i < 4; i++) {
            scaled.data[(destRow * scaled.width + destCol) * 4 + i] = sourcePixel[i];
          }
        }
      }
    }
  }
//  alert(scaled.data.length);
  return scaled;
}
```

### 获取服务器的ip
这里取巧了，直接从浏览器显示部分获取
代码如下：

```java
//获取服务器ip，运行时urlPath为https://192.168.137.1:8000/
function getRemoteIp(){
  var urlPath = window.document.location.href;  //浏览器显示地址 http://10.15.5.83:5555/ISV/demo.aspx?a=1&b=2
  // var docPath = window.document.location.pathname; //文件在服务器相对地址 /ISV/demo.aspx
  // var index = urlPath.indexOf(docPath);
  var serverPath = urlPath.substring(7, urlPath.length-1);//服务器ip 192.168.137.1
  return serverPath;
}
```

### UA检测
因为要适配移动端和PC端，所以简单的UA检测还是必要的，这里没有做的很复杂   
主要就是通过检测`navigator.platfowm`中的关键词来判断

代码如下：

```java
var ua = navigator.userAgent; 
var system = {
  win : false,
  mac : false,
  linux : false,
  // mobile
  iphone : false,
  android : false,
};

var p = navigator.platform;
system.win = p.indexOf('Win') == 0;
system.mac = p.indexOf('Mac') == 0;
system.linux = p.indexOf('Linux') == 0;
system.iphone = ua.indexOf('iPhone') > -1;
system.android = ua.indexOf('Android') > -1

if(system.win||system.mac){
    ...
} else if(system.android||system.iphone){
    ...
}
```

### python根据数组生成图片
dtype一定要写的，不写生成错误
imgData就是图片的RGBA数据数组，要转成np数组才可以用PIL的Image.fromarray()

```python
array = np.asarray(imgData, dtype=np.uint8)
image = Image.fromarray(array, 'RGBA') 
image.save(outputImgPath + imgName +'.png')
```

### 将RGBA转换为RGB格式数组
网上看了很多，有用PIL的，还有直接写算法转换的，用opencv的...很多  
这里发现PIL的不好用，读出来还是RGBA的格式，而且没办法用函数在数组上转换

最后解决办法是:
- 从前端传过来的数据是字典类型，先获取values()
- 将dict.vlues这个数组转换为ndarray数组
- 转换完了,再把这个RGBA数组用 PIL 转换为图片
- 用save()方法保存为临时图片
- 用opencv读取临时图片的RGB通道的数据

```java
# 将图片数据转换为ndarray类型
npData = np.array(imageData,dtype=np.uint8).reshape(28,28,4)
# 将RGBA格式数组转换为图片
image = Image.fromarray(npData, 'RGBA') 
# 保存临时图片
image.save('static/images/npimg.png')

# 用opencv读取图片的RGB数据
rgbImage = cv2.imread('static/images/npimg.png', cv2.IMREAD_COLOR) 
```

### cv2.imread(path[, flags])
cv2的imread函数的第二个参数这里说明下:
> 如果不设置，读进来的是BGR格式的数据，值在0-255,flag一共有3个取值
> cv2.IMREAD_COLOR : 读入彩色图片,任何与透明度相关通道的会被忽视,默认以这种方式读入.
> cv2.IMREAD_GRAYSCALE : 以灰度图的形式读入图片
> cv2.IMREAD_UNCHANGED : 保留读取图片原有的颜色通道.

可以简单的用**-1,0,1**来分别表示这3个flag


### Python图像处理
#### 图片的读写方式总结
找到一个很全的博客，推荐一下：[Python各类图像库的图片读写方式总结](https://www.jb51.net/article/135307.htm)

#### opencv的基本操作
推荐看看这篇文章：[点击跳转](https://www.jianshu.com/p/ed00179ede34)

#### tensorflow简单的图像处理
推荐链接：[使用TensorFlow进行简单的图像处理](https://blog.csdn.net/jia20003/article/details/79118769)

#### PIL格式转换
推荐链接：[Python图像处理库PIL中图像格式转换（一）](https://blog.csdn.net/icamera0/article/details/50843172)

### 对图片灰度化
如果只是灰度的话可以用PIL的convert函数，很方便，但是这里要用tensorflow，所以得用`tf.image_to_grayscale(imageData)`这个函数。注意事先要先将数据格式转换为`tf.float32`类型的

```python
# 将rgb图片转换为float32格式
rgbImage = tf.image.convert_image_dtype(rgbImage, tf.float32)
# 将图片灰度化得到(28,28,1)格式的tensor
rgbImage = tf.image.rgb_to_grayscale(rgbImage
```

### 后端改变图片的背景和画笔颜色数据
出于美观，前端并不是黑底白字，但是模型训练的是黑底白字的，虽然后面测试用了灰度数据，还是会不准确，所以在数据处理前，对imageData中的部分像素进行修改，将橙色变为黑色，黑色画笔变为白色

```python
# 将橙色的背景转换为黑色,将画笔的黑色转为白色
# input: RGBA格式图片数据
# output: 修改过的RGBA格式图片数据
def reveBlack(imageData):
    for i in range(0,len(imageData),4):
        # 如果画笔为白色
        if imageData[i]==0 and imageData[i+1]==0 and imageData[i+2]==0:
            imageData[i]=imageData[i+1]=imageData[i+2]=255
        # 如果背景为橙色
        if imageData[i]==255 and imageData[i+1]==165 and imageData[i+2]==0:
            imageData[i]=imageData[i+1]=imageData[i+2]=0
    return imageDat
```

### tensor和numpy数组转换
#### tensor转ndarray
由于项目里面是模型恢复，所以没有初始化这步
有两种方法：

```python
# 将tensor转换为ndarray
init = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init)
    # 第一种
    ndName = tensorName1.eval(session=sess)
    #第二种
    ndName = sess.run(tensorName2)
```


### ndarray转tensor

```python
# 将ndarray转换为tensor
tensorName =  tf.convert_to_tensor(ndName, dtype = tf.float32)
```


### 使用训练好的模型
**参考链接：**[言初见的CSDN博客](https://blog.csdn.net/yanchujian88/article/details/80559936)

训练用的算法是Lenet-5，下面的代码是部分调用模型代码，因为只有一张图片的数据，并不是用整个测试集，所以有些地方会有点不一样

主要还是通过恢复模型，传入图片数据来获得预测结果

注意点：
1. x占位符的shape，要注意个train的一致，第一个shape要是1，因为只有一个图片
2. 使用tf.argmax(y,1)函数获得最大预测的下标,这里就是结果了，因为是0-9正好对应了下标
3. 输入的feed_dict测试数据必须是ndarray，不可以是tensor，因此要转换以下

代码如下：

```python
# 定义输入格式(1,28,28,1)
x = tf.placeholder(tf.float32, [1, 
                                mnist_inference.IMAGE_SIZE, 
                                mnist_inference.IMAGE_SIZE, 
                                mnist_inference.NUM_CHANNEL], 
                                name='x-input')
#直接通过调用封装好的函数来计算前向传播的结果 
y = mnist_inference.interence(x,None, None)

#使用tf.argmax(y, 1)就可以得到输入样例的预测类别 
prediction = tf.argmax(y, 1)

# 通过变量重命名的方式来加载模型
# 所有滑动平均的值组成的字典,处在/ExponentialMovingAverage下的值  
# 为了方便加载时重命名滑动平均量，tf.train.ExponentialMovingAverage类  
# 提供了variables_to_store函数来生成tf.train.Saver类所需要的变量  
# 这些值要从模型中提取
variable_averages = tf.train.ExponentialMovingAverage(mnist_train.MOVING_AVERAGE_DECAY)
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
        rgbNpData = tf.reshape(rgbImage,[1,
                                            mnist_inference.IMAGE_SIZE, 
                                            mnist_inference.IMAGE_SIZE, 
                                            mnist_inference.NUM_CHANNEL])
        # 将tensor转换为ndarray
        reshaped_data = rgbNpData.eval()
        # 将输入的测试数据格式调整为一个四维矩阵
        validate_feed = {x: reshaped_data}

        # 获得预测的结果数组
        predictionNum = sess.run(prediction, feed_dict = validate_feed)
        print("Number is %d" %(predictionNum[0]))

tf.reset_default_graph()
```

### 报错：Error: the tensor's graph is different from the session's graph
这是因为session里面的图和使用的图不一样导致的，刚开始不清楚，把参考的博客上面的那句： with tf.Graph().as_default() as g:写上去了，导致默认图被设置成了g，但是用的又是恢复的图，所以不一样了

解决办法炒鸡简单...但是debug的过程里就一直没意识到就是了...就是把那句话去掉就行了哇

### 报错：List of Tensors when single Tensor expected
使用tf.constant()函数的时候可能会报这个错误

看看这个函数的定义：
> def constant(value, dtype=None, shape=None, name="Const", verify_shape=False)
> value: A constant value (or list) of output type dtype.
> Returns: A Constant Tensor.

问题也应该清楚了，constant要求输入的是list，用的时候如果传入了tensor类型的，当然就不可以了