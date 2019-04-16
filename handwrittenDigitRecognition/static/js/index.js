var canvas = document.getElementById('canvas');
var outForm = document.getElementById("outForm");
var ctx = canvas.getContext('2d');
var oldx = 0; //起始点x
var oldy = 0; //起始点y
var midx = 0; //中点x
var midy = 0; //中点y
var onoff = false;

var outCanvas = document.getElementById("outCanvas");
var outCtx = outCanvas.getContext('2d');

//检测UA
var ua = navigator.userAgent;
console.log(ua);
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

var linew = 15;
var linecolor = 'black';
var size = document.getElementById('size');
var outSize = document.getElementById('pixelSize');

// canvas框
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
outCtx.fillStyle = "white";
outCtx.fillRect(0, 0, outCanvas.width, outCanvas.height);

//判断移动端还是PC
if (system.win || system.mac || system.linux) {
  //画笔大小选择
  size.onchange = function() { 
    linew = size.value; 
  }
  canvas.addEventListener('mousedown', down, false); //鼠标点击下去
  canvas.addEventListener('mousemove', draw, false); //鼠标移动
  canvas.addEventListener('mouseup', up, false);     //鼠标弹起取消画图
  var gen_bt = document.getElementById('gen_bt');
} else if (system.android || system.iphone) {
  window.onload = mobLoad();
}

function mobLoad() {
  canvas.addEventListener('touchstart',
     function(event) {
       //触摸点按下事件
       if (event.targetTouches.length == 1) {
         var touch = event.targetTouches[0];
         oldx = touch.clientX - canvas.offsetLeft;
         oldy = touch.clientY - canvas.offsetTop;
         canvas.addEventListener('touchmove',tMove,false);
         canvas.addEventListener('touchend',tEnd,false);
       }
     },
     false);
}

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

function genImg() {
  var imgData = ctx.getImageData(0,0,512,512);
  var scale = outSize.value/imgData.width;
  var outImgData = scaleImageData(imgData,scale);
  outCtx.putImageData(outImgData,(outCanvas.width-outSize.value)/2,(outCanvas.width-outSize.value)/2);
}

function scaleImageData(imageData, scale) {
  var scaled =
      outCtx.createImageData(imageData.width * scale, imageData.height * scale);
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

function down(event) {
  onoff = true;
  oldx = event.clientX - canvas.offsetLeft;
  oldy = event.clientY - canvas.offsetTop;
};

function up() { onoff = false; }

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

function clearCanvas() {
  // ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.fillRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);
  ctx.closePath();

  // outCtx.clearRect(0, 0, outCanvas.clientWidth, outCanvas.clientHeight);
  outCtx.fillStyle = "white";
  outCtx.beginPath();
  outCtx.fillRect(0, 0, outCanvas.offsetWidth, outCanvas.offsetHeight);
  outCtx.closePath();
}

function tMove(event){
  //获取新点和中点
  var touche = event.targetTouches[0];
  var newx = touche.clientX - canvas.offsetLeft;
  var newy = touche.clientY - canvas.offsetTop;
  midx = 0.5*(newx+oldx);
  midy = 0.5*(newy+oldy);

  ctx.beginPath();
  ctx.moveTo(oldx,oldy);
  ctx.quadraticCurveTo(midx,midy,newx,newy);
  ctx.stroke();

  oldx = newx;
  oldy = newy;
}

function tEnd(event) {
  //手机离开屏幕的事件
  ctx.closePath();
}
