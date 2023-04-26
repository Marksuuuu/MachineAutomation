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

      if (connectionName == '' || remoteIpAddress == '' || username == '' || password == '' || port == ''){
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
          port: port
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {
          // Display the status message
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
            success: function(data) {
              // Display the status message
              if (data.checking == 'FALSE'){
                $('#submit').prop('disabled', true);
              }else if (data.checking == null){
                $('#submit').prop('disabled', true);
              }else{
                $('#submit').prop('disabled', false);
              }
              console.log(data.checking)
            },
            error: function(xhr, status, error) {
              // Display the error message
            }
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

    })
  });