$(document).ready(function() {
           $('form').on('submit', function(event) {
               $('#loader').show();
               $.ajax({
                   data : {
                       machine_name : $('#machine_name').val(),
                       program_path : $('#program_path').val()
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
                      confirmButtonText: 'Cool',
                      timer: 1500
                    })
                   }
                   else {
                     Swal.fire({
                      icon: 'success',
                      title: 'Your work has been saved',
                      showConfirmButton: false,
                      timer: 2000
                    })
                   }
         
               });
               event.preventDefault();
           });
       });

$(document).ready(function() {
    var empDataTable = $('#data_tbl').DataTable({
                'processing': true,
                'serverSide': true,
                'serverMethod': 'post',
                'ajax': {
                    'url':'/ajaxfile'
                },
                'lengthMenu': [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
                searching: true,
                sort: false,
                "serverSide": true,
                'columns': [
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
                    {data : null,
                        "render": function(data, type, row) {
                            return ' <button class="btn btn-danger rounded-pill icon dripicons dripicons-trash" onclick="deleteRow(' + row.id + ')"></button>';
                        },
                    },
                    {data : null,
                        "render": function(data, type, row) {
                            return ' <button class="btn btn-primary rounded-pill icon dripicons dripicons-pencil" onclick="deleteRow(' + row.id + ')"></button>';
                        }
                    }
                ]
            });
});


                     