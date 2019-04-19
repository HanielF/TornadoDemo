//========================主页canavs相关的JS======================
//========================自定义变量==============================
var canvas = document.getElementById('canvas');
var outForm = document.getElementById("outForm");
var ctx = canvas.getContext('2d');

var oldx = 0; //起始点x
var oldy = 0; //起始点y
var midx = 0; //中点x
var midy = 0; //中点y
var onoff = false; //PC端鼠标是否点下标志

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

//获得视图窗口大小
getViewPort();

//设置背景为橙色
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
ws.onopen = function(e) { }

//接收到识别的数字后修改结果区域
ws.onmessage = function(e) {
  var data = JSON.parse(e.data);
  var res_bt = document.getElementById("result_bt")
  if(data.result){
     res_bt.value=data.result; 
  }
}


//===========================语句部分结束====函数部分开始====================================
//==================================前端部分函数============================================
//获取视图大小，如果是移动端，还要设置canvas宽度和高度，以及下方文字区域宽度
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
  ctx.fillStyle = "orange";
  ctx.beginPath();
  ctx.fillRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
  ctx.closePath();
}


//=====================================PC端函数======================================
//PC端鼠标按下事件，设置oldx和oldy
function down(event) {
  onoff = true;
  oldx = event.clientX - canvas.offsetLeft;
  oldy = event.clientY - canvas.offsetTop;
};

//PC端鼠标起来
function up() { 
  onoff = false; 
}

//PC端鼠标移动
function draw(event) {
  if (onoff == true) {
    //获取新点和中点
    var newx = event.clientX - canvas.offsetLeft;
    var newy = event.clientY - canvas.offsetTop;
    
    //取中点为二次贝塞尔的控制点
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


//====================================移动端函数========================================
//移动端加载函数，添加touchstart, touchmove, touchend事件
function mobLoad() {
  canvas.addEventListener('touchstart',
    function(event) {
      //触摸点按下事件
      if (event.targetTouches.length == 1) {
        var touche = event.targetTouches[0];
        oldx = touche.clientX - canvas.offsetLeft;
        oldy = touche.clientY - canvas.offsetTop;
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
  var newx = touche.clientX - canvas.offsetLeft;
  var newy = touche.clientY - canvas.offsetTop;
  
  //设置二次贝塞尔曲线的控制点为中点
  midx = 0.5*(newx+oldx);
  midy = 0.5*(newy+oldy);

  //设置粗细和颜色
  ctx.lineWidth = linew;
  ctx.strokeStyle = linecolor;
  ctx.lineCap = 'round'

  //绘图
  ctx.beginPath();
  ctx.moveTo(oldx,oldy);
  ctx.quadraticCurveTo(midx,midy,newx,newy);
  ctx.stroke();

  //转移节点
  oldx = newx;
  oldy = newy;
}


//移动端手指离开事件
function tEnd(event) {
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
  var urlPath = window.document.location.href;  //浏览器显示地址 http://192.168.137.1:8000/
  var serverPath = urlPath.substring(7, urlPath.length-1);//服务器ip 192.168.137.1
  return serverPath;
}


//====================================识别数字部分===============================================
//识别函数
function recognizeNum(){
  var uData =  genImg();
  sendMessage(uData);
}


//缩放imageData函数
//scale:倍数
//返回值:缩放后的imageData
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
  return scaled;
}


//生成输出的Data,返回RGBA四个通道像素数组
function genImg() {
  var imgData = ctx.getImageData(0,0,canvas.clientWidth, canvas.clientHeight);
  var scale = outSize.value/imgData.width;
  var outImgData = scaleImageData(imgData,scale);
  return outImgData.data;
}
