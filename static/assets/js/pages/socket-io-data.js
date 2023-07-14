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
    
    data =  JSON.stringify({
        machine_name: machine_name,
        fetched_ip: fetched_ip,
        status: status,
        fetched_sid: fetched_sid,
        get_start_date: get_start_date

    })
    

    ajaxRequest('/insert_ip_data', data)
    
    var data_var = data.status;
    if (data_var === 'CONNECTED') {
        $('.tbody-var').append('<tr><td class="text-bold-500 text-center">' + data.ip + '</td><td class="text-bold-500 text-center"><span class="badge bg-success">' + data.status + '</span></td></tr>');
    } else {
        return data_var;
    }
});
socket.on('server_response_dc', function (data) {
    console.log("🚀 ~ file: socket-io-data.js:44 ~ data:", data)
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
    var machine_name = data.machine_name
    console.log("🚀 ~ file: socket-io-data.js:62 ~ machine_name:", machine_name)
    var message = data.message;
    var sid = data.sid;
    var client_ip = data.client_ip;
    var stop_date = data.stop_date;
    console.log("🚀 ~ file: socket-io-data.js:99 ~ stop_date:", stop_date)

    data = JSON.stringify({
        machine_name: machine_name,
        client_ip: client_ip,
        message: message,
        sid: sid,
        stop_date: stop_date
    }),

    ajaxRequest('/stop_update', data)

});

socket.on('client_idle', function (data) {
    console.log("🚀 ~ file: socket-io-data.js:109 ~ data:", data)
    var machine_name = data.machine_name
    console.log("🚀 ~ file: socket-io-data.js:110 ~ machine_name:", machine_name)
    var status = data.message
    var uid = data.uid
    console.log("🚀 ~ file: socket-io-data.js:107 ~ uid:", uid)
    var client_ip = data.client_ip;
    console.log("🚀 ~ file: socket-io-data.js:47 ~ client_ip:", client_ip)
    var sid = data.sid;
    var idle_date = data.idle_date
    console.log("🚀 ~ file: socket-io-data.js:49 ~ idle_date:", idle_date)

    data = JSON.stringify({
        machine_name: machine_name,
        status: status,
        uid: uid,
        sid: sid,
        client_ip: client_ip,
        idle_date: idle_date,

    })

    ajaxRequest('/idle_update', data)
   
});

socket.on('stop_date', function (data) {
    console.log("🚀 ~ file: socket-io-data.js:169 ~ socket.on ~ data:", data)
    var status = data.status
    var uid = data.uid
    var client_ip = data.client_ip
    var stop_date = data.stop_date

    data = JSON.stringify({
        status: status,
        uid: uid,
        client_ip: client_ip,
        stop_date: stop_date,

    })

    ajaxRequest('/stop_update_data', data)
})

socket.on('pause_date', function (data) {
    console.log("🚀 ~ file: socket-io-data.js:169 ~ socket.on ~ data:", data)
    var status = data.status
    var uid = data.uid
    var client_ip = data.client_ip
    var get_pause_date = data.get_pause_date

    data = JSON.stringify({
        status: status,
        uid: uid,
        client_ip: client_ip,
        get_pause_date: get_pause_date,

    })

    ajaxRequest('/pause_update_data', data)
})

socket.on('resume_date', function (data) {
    var status = data.status
    var uid = data.uid
    var client_ip = data.client_ip
    var get_resume_date = data.get_resume_date
    console.log("🚀 ~ file: socket-io-data.js:169 ~ get_resume_date:", get_resume_date)

    data = JSON.stringify({
        status: status,
        uid: uid,
        client_ip: client_ip,
        get_resume_date: get_resume_date,

    })

    ajaxRequest('/resume_update_data', data)
})

socket.on('wakeup_date', function (data) {
    var machine_name = data.machine_name
    console.log("🚀 ~ file: socket-io-data.js:169 ~ socket.on ~ data:", data)
    var sid = data.sid
    console.log("🚀 ~ file: socket-io-data.js:185 ~ sid:", sid)
    var status = data.status
    var uid = data.uid
    var client_ip = data.client_ip
    var get_wakeup_date = data.get_wakeup_date
    console.log("🚀 ~ file: socket-io-data.js:188 ~ get_wakeup_date:", get_wakeup_date)

    data = JSON.stringify({
        machine_name: machine_name,
        status: status,
        uid: uid,
        client_ip: client_ip,
        sid: sid,
        get_wakeup_date: get_wakeup_date,

    })

    ajaxRequest('/wakeup_update_data', data)
})


function ajaxRequest(url, data){
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
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

}

