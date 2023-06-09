var socket = io.connect();
var machine_name = '';
// Declare the variable globally
socket.on('server_response', function (data) {
    var machine_name = data.machine_name
    console.log("🚀 ~ file: socket-io-data.js:11 ~ data:", machine_name)
    var fetched_ip = data.client_ip;
    console.log("🚀 ~ file: socket-io-data.js:5 ~ fetched_ip:", fetched_ip)
    var status = data.message;
    console.log("🚀 ~ file: socket-io-data.js:7 ~ status:", status)
    var fetched_sid = data.sid;
    console.log("🚀 ~ file: socket-io-data.js:8 ~ fetched_sid:", fetched_sid)
    var get_start_date = data.get_start_date
    console.log("🚀 ~ file: socket-io-data.js:14 ~ get_start_date:", get_start_date)

    $.ajax({
        url: "/insert_ip_data",
        type: "POST",
        data: JSON.stringify({
            machine_name: machine_name,
            fetched_ip: fetched_ip,
            status: status,
            fetched_sid: fetched_sid,
            get_start_date: get_start_date

        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log('data here', data);
        },
        error: function (xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });
    var data_var = data.status;
    if (data_var === 'CONNECTED') {
        $('.tbody-var').append('<tr><td class="text-bold-500 text-center">' + data.ip + '</td><td class="text-bold-500 text-center"><span class="badge bg-success">' + data.status + '</span></td></tr>');
    } else {
        return data_var;
    }
});
// socket.on('client_connected', function (data) {
//     console.log("🚀 ~ file: socket-io-data.js:11 ~ data:", machine_name)
//     var fetched_ip = data.client_ip;
//     console.log("🚀 ~ file: socket-io-data.js:5 ~ fetched_ip:", fetched_ip)
//     var status = data.message;
//     console.log("🚀 ~ file: socket-io-data.js:7 ~ status:", status)
//     var fetched_sid = data.sid;
//     console.log("🚀 ~ file: socket-io-data.js:8 ~ fetched_sid:", fetched_sid)
//     $.ajax({
//         url: "/insert_ip_data",
//         type: "POST",
//         data: JSON.stringify({
//             machine_name: machine_name,
//             fetched_ip: fetched_ip,
//             status: status,
//             fetched_sid: fetched_sid
//         }),
//         contentType: "application/json; charset=utf-8",
//         dataType: "json",
//         success: function (data) {
//             console.log('data here', data);
//         },
//         error: function (xhr, status, error) {
//             console.log("An error occurred: " + error);
//         }
//     });
//     var data_var = data.status;
//     if (data_var === 'CONNECTED') {
//         $('.tbody-var').append('<tr><td class="text-bold-500 text-center">' + data.ip + '</td><td class="text-bold-500 text-center"><span class="badge bg-success">' + data.status + '</span></td></tr>');
//     } else {
//         return data_var;
//     }
// });
socket.on('client_disconnected', function (data) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        width: '580px',
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'warning',
        html: '<div>IP Address: <strong>' + data.client_ip + '</strong><br>SESSION ID: <strong>' + data.sid + '</strong><br> are Disconnected!. Please Check!</div>'
    })

    var message = data.message;
    var sid = data.sid;
    var client_ip = data.client_ip;
    var stop_date = data.stop_date;
    console.log("🚀 ~ file: socket-io-data.js:99 ~ stop_date:", stop_date)



    $.ajax({
        url: '/update_ip_data',
        method: 'POST',
        data: JSON.stringify({
            message: message,
            sid: sid,
            client_ip: client_ip,
            stop_date: stop_date,

        }),
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        success: function () {
            console.log('SAKSESS')
        },
        error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 0) {
            } else if (jqXHR.status === 404) {
                console.log("🚀 ~ file: socket-io-data.js:125 ~ makeAjaxRequest ~ jqXHR:", jqXHR)
            } else if (jqXHR.status === 500) {
                console.log("🚀 ~ file: socket-io-data.js:127 ~ makeAjaxRequest ~ jqXHR:", jqXHR)
            } else if (textStatus === 'parsererror') {
                console.log("🚀 ~ file: socket-io-data.js:129 ~ makeAjaxRequest ~ textStatus:", textStatus)
            } else if (textStatus === 'timeout') {
                console.log("🚀 ~ file: socket-io-data.js:131 ~ makeAjaxRequest ~ textStatus:", textStatus)
            } else if (textStatus === 'abort') {
                console.log("🚀 ~ file: socket-io-data.js:133 ~ makeAjaxRequest ~ textStatus:", textStatus)
            } else {
            }
        }.bind(this) // Bind the error function to preserve context
    });

});




