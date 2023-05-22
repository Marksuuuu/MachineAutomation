var socket = io.connect();

socket.on('result_response', function(data){
    
    Swal.fire({
        icon: 'success',
        title: 'Fetched!',
        text: 'Config got!',
      })
    
})