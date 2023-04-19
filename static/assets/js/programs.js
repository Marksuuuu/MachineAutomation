$(document).ready(function () {
    // Define the DataTable
  
    var table = $('#programs-table').DataTable({
      processing: true,
      ajax: '/programs',
      lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
      columns: [
        {data: 'id'},
        { data: 'path' },
        {
            data: 'status',
                render: function (data, type, row) {
                    // Check the value of 'status' and return a badge with appropriate color
                    if (data === 'running') {
                        return '<span class="badge bg-success status'+row.id+'">' + data + '</span>';
                    } else if (data === 'stopped') {
                        return '<span class="badge bg-danger">' + data + '</span>';
                    } else {
                        return data;
                    }
                }
            },
        { data: 'date_start' },
        { data: 'date_stop' },
        {
          data: 'status', 
          render: function (data, type, row) {
            if (data === 'running') {
                return '<button type="button" class="btn btn-danger rounded-pill icon icon icon dripicons dripicons-media-stop stop-btn" data-id="' + row.id + '"></button> ';
            } else if (data === 'stopped') {
                return '<button type="button" class="btn btn-success rounded-pill icon icon icon dripicons dripicons-media-play start-btn" data-id="' + row.id + '"></button> '
            } else {
                return data;
            }
            
          }
        }
      ],
      "order": [[1, 'asc']]
    });

    $('#programs-table').on('click', '.stop-btn', function(){
        var id = $(this).attr('data-id'); // Get the ID value from the element attribute
        console.log('stop',id)
        $(this).hide()
        $(this).closest('tr').find('td:eq(2)').html('<span class="badge bg-danger">stopped</span>')
        $(this).closest('td').append('<button type="button" class="btn btn-success rounded-pill icon icon icon dripicons dripicons-media-play start-btn" data-id="' +id + '"></button>')
        $.ajax({
            url: '/stop_execute',
            type: 'POST',
            success: function(response) {
                console.log(response);  // Log the response from the server
            },
            error: function(error) {
                console.log(error);  // Log any errors
            }
        });
    });
    $('#programs-table').on('click', '.start-btn', function(){
        var id = $(this).attr('data-id'); // Get the ID value from the element attribute
        $(this).hide()
        $(this).closest('tr').find('td:eq(2)').html('<span class="badge bg-success">running</span>')
        $(this).closest('td').append('<button type="button" class="btn btn-danger rounded-pill icon icon icon dripicons dripicons-media-stop stop-btn" data-id="' +id + '"></button>')
        // AJAX call to get data
        $.ajax({
          url: '/execute',
          method: 'POST',
          data: {id: id}, // Pass the ID in the data payload
          success: function(response) {
            var data = response.msg; // Extract the result data from the response
            // Check if data is not empty
            console.log(data)
          },
          error: function(error) {
            console.log(error);
          }
        });
      });
      
});