
 $(document).ready(function(){
    var table = $('#configuration-tbl').DataTable({
        processing: true,
        ajax: '/config-datatable',
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        columns: [
          { data: 'remote_ip_address' },
          { data: 'username' },
          { data: 'port' },
          {
            data: null, render: function (row) {
              return '<button type="button" class="btn btn-info rounded-pill icon icon dripicons dripicons-pencil show-btn" data-id="' + row.id + '"></button> '+ 
              ' <button type="button" class="btn btn-danger rounded-pill icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
            }
          }
        ],
        "order": [[1, 'asc']]
      });
      $('#configuration-tbl').on('click', '.show-btn', function (){
        var id = $(this).attr('data-id');
        Swal.fire({
            title: 'Button Clicked',
            text: "TEST "+ id,
            icon: 'warning',
        })
        console.log(id)
      })
      $('#configuration-tbl').on('click', '.delete-btn', function (){
        var id = $(this).attr('data-id');
        Swal.fire({
            title: 'Button Clicked',
            text: "TEST "+ id,
            icon: 'warning',
        })
        console.log(id)
      })
})
 
