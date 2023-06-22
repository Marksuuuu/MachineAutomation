var socket = io.connect();

socket.on('result_response', function (data) {

    Swal.fire({
        icon: 'success',
        title: 'Fetched!',
        text: 'Config got!',
    })

});
socket.on('_server_response', function (data) {
    console.log(
        data.operatorIdNum,
        data.photo,
        data.area,
        data.machine_name,
        data.totalProccessQty,
        data.mo,
        data.client_ip
    )


    // Get the table and tbody elements by their IDs
    var table = $('#userPreview');
    var tbody = $('#userTbody');

    // Create a new row
    var row = $('<tr></tr>');

    // Add the columns to the row
    row.append('<td>' + data.operatorIdNum + '</td>');
    row.append('<td><img src="' + data.photo + '" style="width:50px;height:50px; border-radius:50%"></td>');
    row.append('<td>' + data.area + '</td>');
    row.append('<td>' + data.machine_name + '</td>');
    row.append('<td>' + data.totalProccessQty + '</td>');
    row.append('<td>' + data.mo + '</td>');
    row.append('<td>' + data.client_ip + '</td>');

    // Append the row to the tbody
    tbody.append(row);

    // Append the tbody to the table
    table.append(tbody);


})
