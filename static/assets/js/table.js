$(document).ready(function () {
  // Define the DataTable

  var table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/machines',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [

      { data: 'id' },
      { data: 'fetched_ip' },
      {
        data: null,
        className: 'text-center',
        render: function (row) {
          return '<button type="button" class="btn btn-outline-info icon icon dripicons dripicons-expand-2 show-btn" data-id="' + row.id + '"></button> ' +
            ' <button type="button" class="btn btn-outline-danger icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
        }
      }
    ],
    "order": [[1, 'asc']]
  });



  $('#machine-table').on('click', '.edit-btn', function () {
    var id = $(this).data('id');
    $.get('/machines/delete/' + id, function (machine) {
      machineIdField.val(machine.id);
      machineNameField.val(machine.name);
      machinePathField.val(machine.path);
      machineModal.modal('show');
    });
  });

  $('#machine-table').on('click', '.show-btn', function () {
    var id = $(this).attr('data-id'); // Get the ID value from the element attribute
    console.log(id)

    $.ajax({
      url: '/get_name',
      method: 'POST',
      data: { id: id }, // Pass the ID in the data payload
      success: function (response) {
        var data = response.result; // Extract the result data from the response

        // Check if data is not empty
        if (data !== null) {
          // Generate HTML for table rows
          var fetchedIp = ''; // Initialize fetchedIp variable
          for (var i = 0; i < data.length; i++) {
            fetchedIp = data[i][1]; // Set fetchedIp to the current value

            // Exit the loop after the first iteration
            break;
          }

          $('#controller_ip').html(fetchedIp); // Set the value of the #controller_ip element to the fetchedIp value

          var html = '';
          for (var i = 0; i < data.length; i++) {
            var id = data[i][0]; // Accessing Name
            var status = data[i][2]; // Accessing status
            var sid = data[i][3]; // Accessing sid
            var port = data[i][4]; // Accessing port
            var machine_name = data[i][5]; // Accessing machine_name

            var inputButton;
            var badgeClass = '';


            if (machine_name === null) {
              if (status == 'CONNECTED') {
                badgeClass = 'badge bg-success"';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
                inputButton = '<div class="input-group mb-3"><input type="text" id="machine_name_var" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="save-btn"><button class="icon dripicons dripicons-plus btn btn-outline-success save-btn" type="button" data-id="' + id + '"></div>'
              } else if (status == 'DISCONNECTED') {
                badgeClass = 'badge bg-danger';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
                inputButton = '<div class="input-group mb-3"><input type="text" id="machine_name_var" class="form-control" placeholder="" aria-label="Example text with button addon" aria-describedby="save-btn" disabled><button class="icon dripicons dripicons-cross btn disabled btn-danger save-btn" type="button" data-id="' + id + '"></div>'
              } else {
                badgeClass = 'badge bg-primary';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
              }
            } else {
              if (status == 'CONNECTED') {
                badgeClass = 'badge bg-success"';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
                inputButton = '<div ><span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span><button class="icon dripicons dripicons-pencil btn btn-outline-success edit-btn" type="button" data-id="' + id + '"></div>'
              } else if (status == 'DISCONNECTED') {
                badgeClass = 'badge bg-danger';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
                inputButton = '<div><span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span><button class="icon dripicons dripicons-pencil btn disabled btn-danger" type="button" data-id="' + id + '"></div>'
              } else {
                badgeClass = 'badge bg-primary';
                badge = '<span class="' + badgeClass + '">' + status + '</span>'
              }

            }
            console.log(i)


            html += '<tr>';
            html += '<td>' + id + '</td>';
            html += '<td>' + badge + '</td>';
            html += '<td>' + sid + '</td>';
            html += '<td>' + port + '</td>';
            html += '<td>' + inputButton + '</td>';
            html += '</tr>';
          }


          // Set the generated HTML as the content of the modal body
          $('#modal-data').html(html);
          // Show the modal
          $('#myModal').modal('show');
        } else {
          // Handle case when data is empty or null
          $('#modal-data').html('<tr><td colspan="4">No data available</td></tr>');
          $('#myModal').modal('show');
        }
      },
      error: function (error) {
        console.log(error);
      }
    });
  });
  $('#machine_result_id tbody').on('click', '.edit-btn', function () {
    console.log('edit')

  });

  $('#machine_result_id tbody').on('click', '.save-btn', function () {
    var id = $(this).attr('data-id');
    var machine_name_var = $('#machine_name_var').val()
    console.log(id, machine_name_var)
    $('#default').modal('show');
    $.ajax({
      url: '/insert_machine_name',
      method: 'POST',
      data: {
        id: id,
        machine_name_var: machine_name_var
      },
      success: function (result) {
        Swal.fire({
          icon: 'success',
          title: 'Saved!',
          showConfirmButton: true,
          text: 'Succesfully Saved!.',
        })
      }
    });
  });

  $('#machine-table').on('click', '.delete-btn', function () {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success'
        )
        var id = $(this).data('id');
        $.ajax({
          url: '/machines/delete',
          method: 'POST',
          data: { id: id },
          success: function (result) {
            table.ajax.reload();
          }
        });
      }
      else
        Swal.fire({
          title: 'Think Again!',
          icon: 'info',
        })
    })

  });


});

















