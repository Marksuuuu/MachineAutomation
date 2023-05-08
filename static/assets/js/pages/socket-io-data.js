var socket = io.connect();
socket.on('connect', function () {
    console.log('Connected to server');
});
socket.on('client_connected', function (data) {
    console.log('Client connected:', data.ip);
    fetched_ip = data.ip
    var status = 'CONNECTED'
    console.log('test',fetched_ip, socket.connected);
     $.ajax({
            url: "/insert_ip_data", // replace with the URL to your server-side script
            type: "POST",
            data: JSON.stringify({
                fetched_ip: fetched_ip, 
                status: status
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log('data here',data); 
                data.status
            },
            error: function (xhr, status, error) {
                console.log("An error occurred: " + error);
            }
        });
    data_var = data.status
    if (data_var === 'CONNECTED') {
        $('.tbody-var').append('<tr><td class="text-bold-500 text-center">'+ data.ip +'</td><td class="text-bold-500 text-center"><span class="badge bg-success">'+ data.status +'</span></td></tr>');
        // const Toast = Swal.mixin({
        //     toast: true,
        //     position: 'top-end',
        //     showConfirmButton: false,
        //     timer: 3000,
        //     timerProgressBar: true,
        //     width: '400px',
        //     didOpen: (toast) => {
        //       toast.addEventListener('mouseenter', Swal.stopTimer)
        //       toast.addEventListener('mouseleave', Swal.resumeTimer)
        //     }
        //   })
          
        //   Toast.fire({
        //     icon: 'success',
        //     text: data.ip + ' Connected Successfully'
        //   })
    } else {
        return data_var;
    }
    
    console.log(data.ip)
});
socket.on('client_disconnected', function (data) {
    console.log('Client disconnected:', data.ip);
    fetched_ip = data.ip
    var status = 'DISCONNECTED'
    $('.tbody-var').append('<tr><td class="text-bold-500 text-center">'+ data.ip +'</td><td class="text-bold-500 text-center">'+ data.status +'</td></tr>').remove();
    $.ajax({
        url: "/disconnect_ip_data", // replace with the URL to your server-side script
        type: "POST",
        data: JSON.stringify({
            fetched_ip: fetched_ip, 
            status: status
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log('data here',data); 
        },
        error: function (xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        width: '420px',
        didOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      })
      
      Toast.fire({
        icon: 'info',
        text: data.ip + ' Disconnected!. Please Check!'
      })

});

