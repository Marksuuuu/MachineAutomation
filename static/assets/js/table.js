
$(document).ready(function () {
  // Define the DataTable

  var table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/machines',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [
  
      { data: 'id' },
      { data: 'name' },
      {
        data: null, render: function (data, type, row) {
          return '<button type="button" class="btn btn-info rounded-pill icon icon dripicons dripicons-expand-2 show-btn" data-id="' + row.id + '"></button> '+ 
          ' <button type="button" class="btn btn-danger rounded-pill icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
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

  // $('#machine-table').on('click', '.show-btn', function(){
  //   var id = $(this).attr('data-id'); // Get the ID value from the element attribute
  //   $.ajax({
  //     url: '/get_name',
  //     method: 'POST',
  //     data: {id: id}, // Pass the ID in the data payload
  //     success: function(response) {
        
  //     },
  //     error: function(error) {
  //       console.log(error);
  //     }
  //   });
  // });

  $('#machine-table').on('click', '.show-btn', function(){
    var id = $(this).attr('data-id'); // Get the ID value from the element attribute
  
    // AJAX call to get data
    $.ajax({
      url: '/get_name',
      method: 'POST',
      data: {id: id}, // Pass the ID in the data payload
      success: function(response) {
        var data = response.result; // Extract the result data from the response
        // Check if data is not empty
        if (data !== null) {
          // Generate HTML for table rows
          var html = '';
          for (var i = 0; i < data.length; i++) {
            var id = data[i][0]; // Accessing ID
            var name = data[i][2]; // Accessing Name
            var status = data[i][3]; // Accessing status
            var date_start = data[i][4]; // Accessing date_start
            var date_stop = data[i][5]; // Accessing date_stop
  
            var badgeClass = '';
            if (status == 'running') {
              badgeClass = 'badge bg-success"';
              badge = '<span class="' + badgeClass + '">' + status + '</span>'
            } else if (status == 'stopped') {
              badgeClass = 'badge bg-danger';
              badge = '<span class="' + badgeClass + '">' + status + '</span>'
            } else {
              badgeClass = 'badge bg-secondary';
              badge = '<span class="' + badgeClass + '">' + status + '</span>'
            }
            html += '<tr>';
            html += '<td>' + id + '</td>';
            html += '<td>' + name + '</td>';
            html += '<td>' + badge + '</td>';
            html += '<td>' + date_start + '</td>';
            html += '<td>' + date_stop + '</td>';
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
      error: function(error) {
        console.log(error);
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
  setInterval(function () {
    table.ajax.reload();
    console.log('test');
  }, 100000); // 1 minute interval

});

















