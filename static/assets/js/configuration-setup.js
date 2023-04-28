$(document).ready(function() {
    // Handle form submit
    $('#submit').prop('disabled', true);
    $('#alert').hide();
    $("#configuration-tbl-id").submit(function(event) {
      event.preventDefault();

      // Get the form data
      var connectionName = $("#connection-name").val();
      var remoteIpAddress = $("#remote-ip-address").val();
      var username = $("#username").val();
      var password = $("#password").val();
      var port = $("#port").val();
      var max_inputs = $("#max_inputs").val();

      if (connectionName == '' || remoteIpAddress == '' || username == '' || password == '' || port == '' || max_inputs == ''){
        Swal.fire({
            icon: 'error',
            title: 'Please enter IP!',
            showConfirmButton: false,
            timer: 2000
        })
        return false;
    }

      // Send an AJAX request to the server to save the connection
      $.ajax({
        type: "POST",
        url: "/save-connection",
        data: JSON.stringify({
          connection_name: connectionName,
          remote_ip_address: remoteIpAddress,
          username: username,
          password: password,
          port: port,
          max_inputs: max_inputs
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
          // Display the status message
            Swal.fire({
              icon: 'error',
              title: 'Max Inputs reached!',
              text: MaxInputsGlobal,
              showConfirmButton: true,
          })
          console.log(data.msg)
          $("#status").text(data.message);
        },
        error: function(xhr, status, error) {
          // Display the error message
          $("#status").text("Error: " + error);
        }
      });
    });
    $("#button-addon1").click(function(e){
        e.preventDefault();
        var remoteIpAddress = $("#remote-ip-address").val();
        if (remoteIpAddress == ''){
            Swal.fire({
                icon: 'error',
                title: 'Please enter IP!',
                showConfirmButton: false,
                timer: 2000
            })
        }
        
        $.ajax({
            type: "POST",
            url: "/check-ip",
            data: JSON.stringify({
              remote_ip_address: remoteIpAddress,
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function() {
              $('#waitMemodal').waitMe({
                  effect: 'rotateplane',
                  text: 'Please wait...',
                  bg: 'rgba(255,255,255,0.7)',
                  color: '#435ebe',
                  maxSize: '',
                  waitTime: -1,
                  textPos: 'vertical',
                  fontSize: '',
                  source: ''
              });
          },
            success: function(data) {
              // Display the status message
              if (data.checking == 'FALSE'){
                Swal.fire({
                  icon: 'error',
                  title: 'IP INVALID!',
                  showConfirmButton: false,
                  timer: 2000,
                  text: 'please enter valid ip'
                })
                $('#submit').prop('disabled', true);
              }else if (data.checking == null){
                Swal.fire({
                  icon: 'success',
                  title: 'IP INVALID!',
                  showConfirmButton: false,
                  timer: 2000,
                  text: 'please enter valid ip'
                })
                $('#submit').prop('disabled', true);
              }else{
                Swal.fire({
                  icon: 'success',
                  title: 'IP VALID!',
                  showConfirmButton: false,
                  timer: 2000,
                  text: data
                })
                $('#submit').prop('disabled', false);
              }
              console.log(data.checking)
            },
            error: function(xhr, status, error) {
              // Display the error message
            }
          }).done(function() {
            $('#waitMemodal').waitMe('hide');
        });

    });
    $('#add_config_button').click(function(e){
        e.preventDefault();
        $('#inlineForm').modal('show');
        $("#connection-name").val('');
        $("#remote-ip-address").val('');
        $("#username").val('');
        $("#password").val('');
        $("#port").val('');
        $("#max_inputs").val('');

    });
  });




