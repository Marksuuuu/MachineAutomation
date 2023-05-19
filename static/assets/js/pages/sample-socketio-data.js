var socket = io.connect();
socket.on('server_sample_response', function (data) {
    console.log(data)
    $('span #message').html('<p>'+ data.message +'</p>')
    $('span #from').html('<p>'+ data.filename_var +'</p>')

});

