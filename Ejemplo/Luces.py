import wifimgr     # importing the Wi-Fi manager library
from time import sleep     
from machine import Pin

import gc
try:
  import usocket as socket
except:
  import socket
relay = Pin(2, Pin.OUT)
relay1 = Pin(0, Pin.OUT)
wlan = wifimgr.get_connection()        #initializing wlan
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  
print("ESP OK")

def web_page():
  if relay.value() == 1:
    relay_state = ''
  else:
    relay_state = 'checked'
  if relay1.value() == 1:
    relay1_state = ''
  else:
    relay1_state = 'checked'  
 # Empieza el html
  html = """<html>
 <center>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{
  font-family:Arial; 
  text-align: center; 
  margin: 0px auto; 
  padding-top:30px;
} 

.switch{
  position:relative;
  display:inline-block;
  width:120px;
  height:84px;
}
.switch input{
 display:none;
}
.slider{
  position:absolute;
  top:25;
  left:0;
  right:0;
  bottom:0;
  background-color:#ccc;
  border-radius:40px;
} 
.slider:before{
  position:absolute;
  content:"";
  height:50px;
  width:50px;
left:4px;
bottom:4px;
background-color:#fff;
-webkit-transition:.4s;
transition:.4s;
border-radius:24px
} 


input:checked+.slider{
  background-color:#FF3333;
} 
input:checked+.slider:before{
  -webkit-transform:translateX(60px);
  -ms-transform:translateX(60px);
  transform:translateX(60px);
}
 
</style>
<script>function toggleCheckbox1(element) 
{
var xhr = new XMLHttpRequest(); 
if(element.checked)
{
xhr.open("GET", "/?relay=off", true);
} 
else {
xhr.open("GET", "/?relay=on", true);
}




xhr.send();
}
</script>

<script>function toggleCheckbox2(element) 
{
var xhr = new XMLHttpRequest(); 
if(element.checked)
{
xhr.open("GET", "/?relay1=off", true);
} 
else {
xhr.open("GET", "/?relay1=on", true);
}

xhr.send();
}

</script>




</head>

<body>
<h2>Luces de casa </h2>

<h3> lampara 1</h3>
<label class="switch">
<input type="checkbox" onchange="toggleCheckbox1(this)" %s>
<span class="slider Round"></span>
</body>
</label>
<h3>OFF      ON</h3>

<h3>lamapra 2 </h3>
<label class="switch">
<input type="checkbox" onchange="toggleCheckbox2(this)" %s>
<span class="slider Round"></span>
</body>
</label>
<h3>OFF      ON</h3>
</html>""" 
  return html
#Termina el html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))


s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    relay_on = request.find('/?relay=on')
    relay_off = request.find('/?relay=off')
    relay1_on = request.find('/?relay1=on')
    relay1_off = request.find('/?relay1=off')
    if relay_on == 6:
      print('RELAY ON')
      relay.value(0)
    if relay_off == 6:
      print('RELAY OFF')
      relay.value(1)
      ############
    if relay1_on == 6:
      print('RELAY1 ON')
      relay1.value(0)
    if relay1_off == 6:
      print('RELAY1 OFF')
      relay1.value(1)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
