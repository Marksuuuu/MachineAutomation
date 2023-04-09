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