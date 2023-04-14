
$(document).ready(function () {
  // Define the DataTable

  var table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/machines',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [
      {
        class: 'details-control',
        orderable: false,
        data: null,
        defaultContent: '',
      },
      { data: 'id' },
      { data: 'name' },
      { data: 'path' },
      {
        data: 'status',
        render: function (data, type, row, meta) {
          var badgeClass = '';
          if (data == 'running') {
            badgeClass = 'badge bg-success"';
          } else if (data == 'stopped') {
            badgeClass = 'badge bg-danger';
          } else {
            badgeClass = 'badge bg-secondary';
          }
          return '<span class="' + badgeClass + '">' + data + '</span>';
        }
      },
      { data: 'date_start' },
      { data: 'date_stop' },
      {
        data: null, render: function (data, type, row) {
          return '<button type="button" class="btn btn-primary rounded-pill icon dripicons dripicons-document-edit edit-btn" data-id="' + row.id + '"></button> ' +
            '<button type="button" class="btn btn-danger rounded-pill icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
        }
      }
    ],
    "order": [[1, 'asc']]
  });


  var machineModal = $('#editMachine');
  var detailRows = [];


  $('#machine-table tbody').on('click', 'tr td.details-control', function () {
    var tr = $(this).closest('tr');
    var row = table.row(tr);
    var idx = detailRows.indexOf(tr.attr('id'));

    if (row.child.isShown()) {
      tr.removeClass('details');
      row.child.hide();

      // Remove from the 'open' array
      detailRows.splice(idx, 1);
    } else {
      tr.addClass('details');
      row.child(format(row.data())).show();

      // Add to the 'open' array
      if (idx === -1) {
        detailRows.push(tr.attr('id'));
      }
    }
  });

  table.on('draw', function () {
    detailRows.forEach(function (id, i) {
      $('#' + id + ' td.details-control').trigger('click');
    });
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


function format(d) {
  var body = '';
  return (
    body += '<table class="table">'
    + '<thead>'
    + '<tr>'
    + '<th scope="col">#</th>'
    + '<th scope="col">First</th>'
    + '<th scope="col">Last</th>'
    + '<th scope="col">Handle</th>'
    + '</tr >'
    + '</thead >'
    + '<tbody>'
    + '<tr>'
    + '<th scope="row">1</th>'
    + '<td>Mark</td>'
    + '<td>Otto</td>'
    + '<td>@mdo</td>'
    + '</tr>'
    + '<tr>'
    + '<th scope="row">2</th>'
    + '<td>Jacob</td>'
    + '<td>Thornton</td>'
    + '<td>@fat</td>'
    + '</tr>'
    + '<tr>'
    + '<th scope="row">3</th>'
    + '<td>Larry</td>'
    + '<td>the Bird</td>'
    + '<td>@twitter</td>'
    + '</tr>'
    + '</tbody>'
    + '</table >'
  );
}















