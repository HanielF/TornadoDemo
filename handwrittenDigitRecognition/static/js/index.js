//========================主页canavs相关的JS======================
//========================自定义变量==============================
var canvas = document.getElementById('canvas');
var outForm = document.getElementById("outForm");
var ctx = canvas.getContext('2d');

var oldx = 0; //起始点x
var oldy = 0; //起始点y
var midx = 0; //中点x
var midy = 0; //中点y
var newx = 0; //最新点x
var newy = 0; //最新点y

var mid_1x = 0; //第一个中点
var mid_1y = 0; //第一个中点
var mid_2x = 0; //第二个中点
var mid_2y = 0; //第二个中点

var onoff = false; //PC端鼠标是否点下标志

var xStart = canvas.clientWidth; //所有点最左边的x坐标
var yStart = canvas.clientHeight; //所有点最上面的y坐标
var xEnd = 0;  //所有点的最右边的x坐标
var yEnd = 0; //所有点的最下面的y坐标

var linew = 15; //线条粗细
var linecolor = 'black';  //线条颜色
var size = document.getElementById('size'); //画笔大小select部件
var outSize = document.getElementById('pixelSize'); //像素大小select部件
size.onchange = function() { linew = size.value; }

//======================================UA检测==========================
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
system.android = ua.indexOf('Android') > -1;

getViewPort();
ctx.fillStyle = "orange"; 
ctx.fillRect(0, 0, canvas.width, canvas.height);

//===================================适配移动端和PC端===============================
if (system.win || system.mac ) {
  canvas.addEventListener('mousedown', down, false); //鼠标点击下去
  canvas.addEventListener('mousemove', draw, false); //鼠标移动
  canvas.addEventListener('mouseup', up, false);     //鼠标弹起取消画图
  var gen_bt = document.getElementById('gen_bt');
} else if (system.android || system.iphone) {
  document.getElementById("outForm").style.marginTop="30px";
  document.getElementById('outForm').style.fontSize="19px";
  document.getElementById('outForm').style.height="130px";
  document.getElementById('clear_bt').style.marginTop="30px";
  document.getElementById('predict_bt').style.marginTop="30px";
  document.getElementById('result_bt').style.marginTop="25px";
  document.getElementById('hint').style.marginTop="25px";

  window.onload = mobLoad();
}


//===================================WebSocket部分=================================
//定义变量
var remoteHref = getRemoteIp();
var ws = new WebSocket("ws://"+remoteHref+"/preNum");
ws.onopen = function(e) {
//  alert("open ws successfully");
}
ws.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var res_bt = document.getElementById("result_bt")
  if(data.result){
     res_bt.value=data.result; 
  }
}



//===========================语句部分结束====函数部分开始====================================
//==================================前端部分函数============================================
//获取视图大小
function getViewPort() {
  var viewHeight = window.innerHeight || document.documentElement.clientHeight;
  var viewWidth = window.innerWidth || document.documentElement.clientWidth;
  console.log(viewHeight, viewWidth);
  if (system.android || system.iphone) {
    document.body.style.width = viewWidth;
    canvas.width = viewWidth;
    canvas.height = viewWidth;              // canvas部分不可以加px
    outForm.style.width = viewWidth + "px"; //不能去掉.style和px
  }
}

//清除幕布
function clearCanvas() {
  // ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
  ctx.fillStyle = "orange";
  ctx.beginPath();
  ctx.fillRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
  ctx.closePath();
}


//=====================================PC端函数======================================
//PC端鼠标按下
function down(event) {
  onoff = true;
  oldx = event.clientX - canvas.offsetLeft;
  oldy = event.clientY - canvas.offsetTop;
  midx = oldx;
  midy = oldy;
};

//PC端鼠标起来
function up() { 
  onoff = false; 
}

//PC端鼠标移动
function draw(event) {
  if (onoff == true) {
    //获取新点和中点
    newx = event.clientX - canvas.offsetLeft;
    newy = event.clientY - canvas.offsetTop;
    mid_1x = 0.5*(oldx+midx);
    mid_1y = 0.5*(oldy+midy);
    mid_2x = 0.5*(newx+midx);
    mid_2y = 0.5*(newy+midy);

    //修改xStart, xEnd, yStart, yEnd
    if(newx<xStart)xStart = newx;
    if(newx>xEnd)xEnd = newx;
    if(newy<yStart)yStart = newy;
    if(newy>yEnd)yEnd = newy;

    //设置粗细和颜色
    ctx.lineWidth = linew;
    ctx.strokeStyle = linecolor;
    ctx.lineCap = 'round';

    //绘制二次贝塞尔
    ctx.moveTo(mid_1x,mid_1y);
    ctx.quadraticCurveTo( midx , midy , mid_2x , mid_2y );
    ctx.stroke();

    //转移新旧坐标
    oldx = midx;
    oldy = midy;
    midx = newx;
    midy = newy;
  };
}


//====================================移动端函数========================================
//移动端加载函数
function mobLoad() {
  canvas.addEventListener('touchstart',
    function(event) {
      //触摸点按下事件
      if (event.targetTouches.length == 1) {
        var touche = event.targetTouches[0];
        oldx = touche.clientX - canvas.offsetLeft;
        oldy = touche.clientY - canvas.offsetTop;
        midx = oldx;
        midy = oldy;
        canvas.addEventListener('touchmove',tMove,false);
        canvas.addEventListener('touchend',tEnd,false);
      }
    },
    false);
}

//移动端手指移动
function tMove(event){
  //获取新点和中点
  var touche = event.targetTouches[0];
  newx = touche.clientX - canvas.offsetLeft;
  newy = touche.clientY - canvas.offsetTop;
  mid_1x = 0.5*(oldx+midx);
  mid_1y = 0.5*(oldy+midy);
  mid_2x = 0.5*(newx+midx);
  mid_2y = 0.5*(newy+midy);

  //修改xStart, xEnd, yStart, yEnd
  if(newx<xStart)xStart = newx;
  else if(newx>xEnd)xEnd = newx;
  if(newy<yStart)yStart = newy;
  else if(newy>yEnd)yEnd = newy;
    
  //设置粗细和颜色
  ctx.lineWidth = linew;
  ctx.strokeStyle = linecolor;
  ctx.lineCap = 'round'

  ctx.beginPath();
  ctx.moveTo(mid_1x,mid_1y);
  ctx.quadraticCurveTo( midx , midy , mid_2x , mid_2y );
  ctx.stroke();

  oldx = midx;
  oldy = midy;
  midx = newx;
  midy = newy;
}

//移动端手指离开
function tEnd(event) {
  //手机离开屏幕的事件
  ctx.closePath();
}


//====================================WebSocket部分函数=======================================
//发送消息函数
function sendMessage(uData) {
  var data = {
    number: uData,
  }
  if(data.number)
    ws.send(JSON.stringify(data));
  else 
    alert("RGBA数据为空!");
    return false;
}

//获取服务器ip
function getRemoteIp(){
  var urlPath = window.document.location.href;  //浏览器显示地址 http://10.15.5.83:5555/ISV/demo.aspx?a=1&b=2
  // var docPath = window.document.location.pathname; //文件在服务器相对地址 /ISV/demo.aspx
  // var index = urlPath.indexOf(docPath);
  var serverPath = urlPath.substring(7, urlPath.length-1);//服务器ip 192.168.137.1
  return serverPath;
}


//====================================识别数字部分===============================================
//识别函数
function recognizeNum(){
  var uData =  genImg();
  sendMessage(uData);
}


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

//生成输出的Data,返回RGBA四个通道像素数组
function genImg() {
  var tmpWidth = xEnd - xStart;
  var tmpHeight = yEnd - yStart;
  var maxtmp;

  //使矩形变成正方形
  if(tmpWidth>tmpHeight){   //宽度比较大
    maxtmp = tmpWidth;
    var diff = (tmpWidth - tmpHeight)/2;
    //如果超过了上边界
    if(diff>yStart){
      yStart = 0;
      yEnd = tmpWidth;
    //如果超过了下边界
    }else if(diff>canvas.clientHeight-yEnd){
      yEnd = canvas.clientHeight;
      yStart = canvas.clientHeight-tmpWidth;
    }else{
      yStart = Math.floor(yStart - diff);
      yEnd = yStart+tmpWidth;
    }
  }else{                  //长度比较大
    maxtmp = tmpHeight;
    var diff = (tmpHeight - tmpWidth)/2;
    //如果超过了左边界
    if(diff>xStart){
      xStart = 0;
      xEnd = tmpHeight;
    //如果超过了右边界
    }else if(diff>canvas.clientWidth-xEnd){
      xEnd = canvas.clientWidth;
      xStart = canvas.clientWidth-tmpHeight;
    }else{
      xStart = Math.floor(xStart -diff);
      xEnd = xStart+tmpHeight;
    }
  }

  //对这个正方形上下左右都扩大一点，防止数字太贴边
  var minStart = Math.min(xStart,yStart);
  var minEnd = Math.min(canvas.clientWidth-xEnd,canvas.clientHeight-yEnd);
  var minLength = Math.min(minStart,minEnd);
  minLength = Math.min(60,minLength);

  xStart = xStart - minLength;
  yStart = yStart - minLength;
  xEnd = xEnd + minLength;
  yEnd = yEnd + minLength;

//  var bt = document.getElementById("clear_bt");
//  var bt2 = document.getElementById("predict_bt");
//  bt.value=xStart+' '+xEnd;
//  bt2.value = yStart +' '+yEnd;

  //对绘图的一部分进行截取并获取imageData
  var imgData = ctx.getImageData(xStart,yStart,maxtmp+2*minLength, maxtmp+2*minLength);
  var scale = outSize.value/imgData.width;
  var outImgData = scaleImageData(imgData,scale);
  //outCtx.putImageData(outImgData,(outCanvas.width-outSize.value)/2,(outCanvas.width-outSize.value)/2);
  return outImgData.data;
}