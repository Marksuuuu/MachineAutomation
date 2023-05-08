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
      { data: 'device_id' },
      {
        data: 'status',
        render: function (data, type, row) {
          // Check the value of 'status' and return a badge with appropriate color
          if (data === 'STARTED') {
            return '<span class="badge bg-success status' + row.id + '">' + data + '</span>';
          } else if (data === 'STOP') {
            return '<span class="badge bg-danger">' + data + '</span>';
          } else {
            return data;
          }
        }
      },
      { data: 'operator' },
      { data: 'assigned_gl' },
      { data: 'operation_code' },
      { data: 'operation' },
      { data: 'area' },

      {
        data: null, render: function (data, type, row) {
          return '<button type="button" class="btn btn-danger rounded-pill icon icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button> '
        }
      }

    ],
    "order": [[1, 'asc']]
  });
  $('#captured-time-tbl-id').on('click', '.delete-btn', function () {
    var id = $(this).data('id');
    console.log(id)
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
          url: '/delete_data',
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
