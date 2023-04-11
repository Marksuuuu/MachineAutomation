$(document).ready(function() {
            $('form').on('submit', function(event) {
            var machine_name = $('#machine_name').val()
            var program_path = $('#program_path').val()

            if (program_path == '' && program_path == '') {
                Swal.fire({
                    title: 'Error!',
                    text: 'Please Enter Something',
                    icon: 'error',
                    confirmButtonText: 'Ok'
                })
                event.preventDefault();
            } else {
                $.ajax({
                    data : {
                        machine_name : machine_name,
                        program_path : program_path
                    },
                    type : 'POST',
                    url : '/process'
                })
                .done(function(data) {
                    if (data.error) {
                        Swal.fire({
                            title: 'Error!',
                            text: 'Do you want to continue',
                            icon: 'error',
                            confirmButtonText: 'Ok',
                            timer: 2000
                        })
                    }
                    else {
                        Swal.fire({
                            icon: 'success',
                            title: 'Saved!',
                            showConfirmButton: false,
                            timer: 2000
                        })
                    }
                });
                event.preventDefault();
            }
        });
       });  

$(document).ready(function() {
    var machineTbl = $('#data_tbl').DataTable({
                'processing': true,
                'serverSide': true,
                'serverMethod': 'post',
                'ajax': {
                    'url':'/datatable',
                    
                },

                'lengthMenu': [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
                searching: true,
                sort: true,
                "serverSide": true,
                'columns': [
                    { data: 'id' },
                    { data: 'name' },
                    { data: 'path' },
                    { data: 'status',
	                    render: function(data, type, row, meta) {
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
                    { data: 'date_start'},
                    { data: 'date_stop'},
                    { data: null,
                      "render": function (data, type, row) {
                        var editBtn = '<button id="delete-button" class="btn btn-primary rounded-pill icon dripicons dripicons-document-edit" onclick="editRow()"></button>';
                        var deleteBtn = '<button class="btn btn-danger rounded-pill icon dripicons dripicons-trash" onclick="deleteRow()"></button>';
                          return editBtn + " " + deleteBtn;
                      }
                    }
                ]
            });
    setInterval( function () {
        machineTbl.ajax.reload();
        console.log('test')
    }, 100000 );

});

function editRow(id) {
      Swal.fire({
      title: 'Are you sure?',
      text: "You want to edit?",
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes!'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success'
        )
      }
    })

}

function deleteRow(id) {
    Swal.fire({
          title: 'Are you sure?',
          text: "Are you sure you want to delete this program?",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
          if (result.isConfirmed) {
            $.ajax({
            url: '/delete_program',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'id': id
            }),
            success: function(data) {
                if (data.success) {
                    Swal.fire(
                      'Deleted!',
                      'Your file has been deleted.',
                      'success'
                    )
                    empDataTable.ajax.reload();
                } else {
                    Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Something went wrong!',
                    })
                }
            },
            error: function(error) {
                Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Error, Plase check again.',
                    })
                console.log(error);
            }
        });
          }
        })
}













                     