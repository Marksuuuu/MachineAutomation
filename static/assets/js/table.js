$(document).ready(function () {
  // Define the DataTable

  var table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/machines',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [

      { data: 'id' },
      { data: 'fetched_ip' },
      { data: 'controller_name' },
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
        var addControllerInputGroup = '';


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

          var controller_name = ''; // Initialize controller_name variable
          for (var i = 0; i < data.length; i++) {
            controller_name = data[i][7]; // Set controller_name to the current value
            break;
          }

          if (controller_name == null) {
            // If controller_name is null, add the input group
            var inputGroupExists = $('#inputGroup').length > 0;
            if (!inputGroupExists) {
              var addControllerInputGroup = '<div id="inputGroup">'
                + '<div class="input-group mb-3">'
                + '<input type="text" class="form-control" placeholder="" id="controller_name" aria-describedby="add-controller-name">'
                + '<button class="btn btn-primary add-controller" type="button" id="add-controller-name" data-ip=' + fetchedIp + '>Add Controller</button>'
                + '</div></div>';
              $(addControllerInputGroup).insertAfter("#controller_ip");

              $('#add-controller-name').click(function () {
                var ip = $(this).data('ip');
                var controller_name_var = $('#controller_name').val()
                if (controller_name_var == '') {
                  Swal.fire({
                    icon: 'warning',
                    title: 'Error',
                    text: 'Enter you must something!.',
                    showConfirmButton: true,
                  })

                } else {
                  console.log('Clicked on button with IP:', ip, controller_name_var);
                  $.ajax({
                    url: '/insert_controller',
                    method: 'POST',
                    data: {
                      ip: ip,
                      controller_name_var: controller_name_var
                    },
                    success: function (response) {
                      Swal.fire({
                        icon: 'success',
                        title: 'Successfully saved!',
                        text: 'Controller Inserted!',
                        showConfirmButton: true,
                      })

                      $('#myModal').modal('hide');
                      table.ajax.reload();
                    }
                  });

                }
              });
            } else {
              console.log('Input group already exists.');
            }
          } else {
            // If controller_name is not null, update the existing controller_span element
            var controllerSpanExists = $('#controller_span').children().length > 0;
            if (!controllerSpanExists) {
              var span = $('<h5>').text('Controller name : ' + controller_name);
              var controller_span = $('<div>').attr('id', 'controller_span').append(span);
              $(controller_span).insertAfter("#controller_ip");
            } else {
              $('#controller_span').children().text('Controller name : ' + controller_name);
            }
            $('#controller_name').replaceWith('');
            $('#add-controller-name').replaceWith('');
          }

          console.log("🚀 ~ file: table.js:82 ~ fetched_result:", controller_name)
          var html = '';
          for (var i = 0; i < data.length; i++) {
            var id = data[i][0]; // Accessing Name
            var status = data[i][2]; // Accessing status
            var sid = data[i][3]; // Accessing sid
            var port = data[i][4]; // Accessing port
            var machine_name = data[i][5]; // Accessing machine_name
            var area = data[i][6]; // Accessing area
            var controller_name = data[i][7];

            var input_machine_name = '<input type="text" id="machine_name_var" class="form-control" aria-describedby="save-btn">';
            var input_area = '<input type="text" class="form-control" id="area_var" aria-describedby="save-btn">';
            var buttonClass = '';
            var buttonIcon = '';
            var buttonStatus = '';
            var buttonClassName = '';

            if (status === 'CONNECTED') {
              buttonClass = 'btn-outline-success';
              buttonIcon = 'dripicons-pencil';

              buttonStatus = ''
              if (machine_name !== null) {
                input_machine_name = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span>';
                buttonClassName = 'edit-btn'
              } else {
                buttonClass = 'btn-outline-primary';
                buttonIcon = 'dripicons-plus';
                buttonClassName = 'save-btn'
              }
              if (area !== null) {
                input_area = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + area + '</span>';
                buttonClassName = 'edit-btn'
              } else {
                buttonClass = 'btn-outline-primary';
                buttonIcon = 'dripicons-plus';
                buttonClassName = 'save-btn'
              }


            } else if (status === 'DISCONNECTED') {
              buttonClass = 'disabled btn-danger';
              buttonIcon = 'dripicons-warning';
              buttonStatus = 'disabled'
              input_machine_name = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span>';
              input_area = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + area + '</span>';
            } else {
              buttonClass = 'disabled btn-primary';
              buttonIcon = 'dripicons-warning';
            }

            html += '<tr>';
            html += '<td>' + id + '</td>';
            html += '<td><span class="badge ' + (status === 'CONNECTED' ? 'bg-success' : (status === 'DISCONNECTED' ? 'bg-danger' : 'bg-primary')) + '">' + status + '</span></td>';
            html += '<td>' + sid + '</td>';
            html += '<td>' + port + '</td>';
            html += '<td>' + (status === 'CONNECTED' ? input_machine_name : input_machine_name.replace('type="text"', 'type="text" disabled')) + '</td>';
            html += '<td>' + (status === 'CONNECTED' ? input_area : input_area.replace('type="text"', 'type="text" disabled')) + '</td>';
            html += '<td><button class="icon dripicons ' + buttonIcon + ' btn ' + buttonClass + ' ' + buttonStatus + ' ' + buttonClassName + '" type="button" data-id="' + id + '"></button></td>';
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
    var row = $(this).closest('tr');
    var id = $(this).attr('data-id');
    console.log(id)
    var inputMachineNameTd = row.find('td:nth-child(5)');
    var inputAreaTd = row.find('td:nth-child(6)');
    var buttonReplace = row.find('td:nth-child(7)');
    inputMachineNameTd.html('<input type="text" class="form-control" id="machine_name_var" value="' + inputMachineNameTd.text() + '">');
    inputAreaTd.html('<input type="text" class="form-control" id="area_var" value="' + inputAreaTd.text() + '">');
    buttonReplace.html('<button type="button" class="icon dripicons btn dripicons-plus btn btn-outline-primary save-btn" data-id="' + id + '">');
  });

  $('#machine_result_id tbody').on('click', '.save-btn', function () {
    var id = $(this).attr('data-id');
    var machine_name_var = $('#machine_name_var').val()
    var area_var = $('#area_var').val()
    console.log(id, machine_name_var, area_var)
    $('#default').modal('show');
    if (machine_name_var == '' && area_var == '') {
      Swal.fire({
        icon: 'warning',
        title: 'Error!',
        showConfirmButton: true,
        text: 'You must have enter something!.',
      })
    } else {
      $.ajax({
        url: '/insert_machine_name',
        method: 'POST',
        data: {
          id: id,
          machine_name_var: machine_name_var,
          area_var: area_var
        },
        success: function (data) {
          Swal.fire({
            icon: 'success',
            title: 'Saved!',
            text: 'Succesfully Saved!.',
          })
          $('#default').modal('hide');
          $('#myModal').modal('hide');
        }
      });
    }
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

















