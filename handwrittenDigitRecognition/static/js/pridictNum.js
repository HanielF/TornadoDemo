var ws = new WebSocket("ws://127.0.0.1:8000/preNum");
ws.onopen = function(e) {
  
}
ws.onmessage = function(e) {
  
}

function sendImage() {
  var data = {
  }
  if(data.img)
    ws.send(JSON.stringify(data));
  else 
    alert("请先生成图片");
}
