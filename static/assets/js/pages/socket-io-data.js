var socket = io.connect();
socket.on('connect', function () {
    console.log('Connected to server');
});
socket.on('client_connected', function (data) {
    console.log('Client connected:', data.ip);
    data_var = data.status
    if (data_var === 'CONNECTED') {
        $('.tbody-var').append('<tr><td class="text-bold-500 text-center">'+ data.ip +'</td><td class="text-bold-500 text-center"><span class="badge bg-success">'+ data.status +'</span></td></tr>');
    } else {
        return data_var;
    }
    
    console.log(data.ip)
});
socket.on('client_disconnected', function (data) {
    console.log('Client disconnected:', data.ip);
    $('.tbody-var').append('<tr><td class="text-bold-500 text-center">'+ data.ip +'</td><td class="text-bold-500 text-center">'+ data.status +'</td></tr>').remove();
});