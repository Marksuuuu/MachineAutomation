$(document).ready(function () {
  var table = $('#captured-time-tbl-id').DataTable({
    processing: true,
    responsive: {
      details: false
  },
    ajax: '/card_details_table',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [
      { data: 'id' },
      { data: 'current_path' },
      { data: 'status' },
      { data: 'start_time' },
      { data: 'idle_time' },
      { data: 'pause_time' },
      { data: 'resume_time' },
      { data: 'end_time' },
      { data: 'duration' },
      {
        data: null, render: function (data, type, row) {
          return '<button type="button" class="btn btn-info rounded-pill icon icon dripicons dripicons-plus add-btn" data-id="' + row.id + '"></button> '
        }
      }

    ],
    "order": [[1, 'asc']]
  });
  $('#captured-time-tbl-id').on('click', '.add-btn', function () {
    var id = $(this).data('id')
    console.log(id)
    $('#inlineForm').modal('show');
    $('form').submit(function(event) {
      event.preventDefault();
      var formData = {
        'id': id,
        'duration': $('input[name="duration"]').val(),
      };

      // Send data to Flask route using Ajax
      $.ajax({
        type: 'POST',
        url: '/insert_data',
        data: JSON.stringify(formData, id),
        contentType: 'application/json',
        success: function(response) {
          Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Save it!'
          }).then((result) => {
            if (result.isConfirmed) {
              Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
              )
              table.ajax.reload();
            }
          })
          console.log(response);
          
        },
        error: function(xhr, status, error) {
          Swal.fire({
            icon: 'error',
            title: 'Error!',
            showConfirmButton: false,
            timer: 2000
        })
          console.log(error);
          
        }
      });
    });
    

  });
});
