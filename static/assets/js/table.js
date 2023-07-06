var ajaxRequestTable;
// var fetchedIp;
var table;

$(document).ready(function () {
  getMachinesNamesApi();

  table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/machines',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [
      { data: 'id' },
      { data: 'fetched_ip' },
      { data: 'controller_name',
        className: 'text-center',
        render: function(row, data){
          return '<span class="badge bg-primary" style="width: auto; height: auto; font-size:20px;">' + row + '</span>';
        },
      },
      {
        data: null,
        className: 'text-center',
        render: function (row) {
          return '<button type="button" class="btn btn-outline-info icon icon dripicons dripicons-expand-2 show-btn" data-id="' + row.id + '"></button> ' +
            ' <button type="button" class="btn btn-outline-danger icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
        }
      }
    ],
    "order": [[1, 'asc']],







        //         var controllerSpanExists = $('#controller_span').children().length > 0;
//         if (!controllerSpanExists) {
//           var span_controller = '<span>Controller name : ' + controller_name + '</span>';
//           var controller_button = '<button type="button" class="btn btn-outline-primary edit-controller-btn" data-id="' + controller_id + '">Edit</button>'
//           var controller_span = $('<div>').attr('id', 'controller_span').append(span_controller);
//           var button_class = $('<div>').attr('id', 'button_class').append(controller_button);
//           $(controller_span).insertAfter("#controller_ip");
//           $(button_class).insertAfter("#controller_span");
//         } else {
//           $('#controller_span').children().text('Controller name : ' + controller_name);
//           var editButton = $('<button>').attr('type', 'button').addClass('btn btn-outline-primary edit-controller-btn').attr('data-id', controller_id).text('Edit');
//           // Check if the button already exists before adding it
//           if ($('#button_class').find('.edit-controller-btn').length === 0) {
//             $('#controller_span').children().text('Controller name: ' + controller_name);
//             var editButton = $('<button>')
//               .attr('type', 'button')
//               .addClass('btn btn-outline-primary edit-controller-btn')
//               .attr('data-id', controller_id)
//               .text('Edit');
//             $('#button_class').append(editButton);
//           }

//         }
//         $('#controller_name').replaceWith('');
//         $('#add-controller-name').replaceWith('');
//       }

    initComplete: function () {
      displayControllerName();
    }
  });

  $('#machine-table').on('click', '.show-btn', function () {
    $('#myModal').modal('show')
    var id = $(this).attr('data-id');
    ajaxRequestShow(id)
  });

  function displayControllerName() {
    var controllerInput = $('#controllerInput');
    var button = $('#controllerBtn');
    var firstRowData = table.row(0).data();
  
    if (firstRowData && firstRowData.controller_name) {
      controllerInput.prop('value', firstRowData.controller_name);
      controllerInput.prop('style', 'pointer-events: none; border:none;');
      controllerInput.prop('readonly', true);
      // button.removeAttr('id')
      button.attr('class', 'btn btn-outline-danger icon dripicons dripicons-pencil edit-btn-test');
      
    } else {
      controllerInput.prop('value', '');
      button.prop('type', 'button');
      button.prop('class', 'btn btn-outline-success icon dripicons dripicons-plus save-btn');
    }

    $('.edit-btn-test').click(function(){
      ajaxChanged(firstRowData)
    })

    $('.save-btn').click(function(){
      controllerSave();
    })
   
  }

  function ajaxChanged(firstRowData) {
    console.log("🚀 ~ file: table.js:106 ~ ajaxChanged ~ firstRowData:", firstRowData.controller_name)
    var controllerInput = $('#controllerInput');
    var button = $('#controllerBtn');
    controllerInput.prop('style', 'pointer-events: auto;');


    controllerInput.attr('value', firstRowData.controller_name);
    controllerInput.attr('readonly', false);
    button.attr('class', 'btn btn-outline-primary icon dripicons dripicons-plus update-btn');

    $('.update-btn').click(function(){
      controllerSave();
    })
  }


  

  function ajaxRequestShow(id) {
    if (ajaxRequestTable) {
      ajaxRequestTable.destroy();
    }

    ajaxRequestTable = $('#machineResultTbl').DataTable({
      processing: true,
      ajax: {
        url: '/get_name',
        method: 'POST',  // Use GET method for retrieving data
        data: { id: id },  // Pass the ID parameter in the query string
      },
      lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
      columns: [
        { data: 'id' },
        { data: 'fetched_ip' },
        {
          data: 'status',
          render: function (data) {
            if (data == 'DISCONNECTED') {
              return '<span class="badge bg-danger">' + data + '</span>';
            } else if (data = 'CONNECTED') {
              return '<span class="badge bg-success">' + data + '</span>';
            } else {
              return '<span class="badge bg-primary">' + data + '</span>';
            }
          }
        },
        { data: 'sid' },
        { data: 'port' },
        { data: 'machine_name'},
        { data: 'area' },
        { data: 'controller_name' },
        {
          data: null,
          className: 'text-center',
          render: function (row) {
            var buttonClass = row.status === 'DISCONNECTED' ? 'btn btn-outline-danger' : 'btn btn-outline-info';
            var buttonIcon = row.status === 'DISCONNECTED' ? 'dripicons-lock' : 'dripicons-pencil';
            var buttonType = row.status === 'DISCONNECTED' ? 'button' : 'button';
            var buttonAttributes = row.status === 'DISCONNECTED' ? 'disabled' : '';

            return '<button type="' + buttonType + '" class="btn ' + buttonClass + ' icon icon dripicons ' + buttonIcon + ' edit-btn" data-id="' + row.id + '"' + buttonAttributes + '></button>';
          },
          createdRow: function (row, data) {
            if (data.status === 'DISCONNECTED') {
              $(row).find('.edit-btn').click(function (e) {
                e.preventDefault();
              });
            }
          }
        }
      ],
      columnDefs: [
        {
          targets: 3, 
          width: '20%',
        }
      ],
      initComplete: function () {
        var firstRowData = table.row(0).data();
        if (firstRowData) {
          var fetchedIp = firstRowData.fetched_ip;
          // console.log("🚀 ~ file: table.js:30 ~ fetchedIp:", fetchedIp)
          $('#spanDataId').attr('data-ip', fetchedIp)
          controller_name = firstRowData.controller_name;
        
        }
      },
      "order": [[1, 'asc']]
      
    });
  }

  function getMachinesNamesApi() {
    $.ajax({
      url: "/getMachinesNamesApi",
      type: "GET",
      success: function(response) {
        var machineNames = response;
        var select = $("#machine_name_var"); 
        select.select2({
          dropdownParent: $('#myModal')
        })
        
        $.each(machineNames, function(index, name) {
          select.append($('<option></option>').val(name).html(name));
        });
      },
      error: function(error) {
        console.log("Error in API request:", error);
      }
    });
  }

  $('#machineResultTbl').on('click', '.edit-btn', function () {
    var row = $(this).closest('tr');
    var id = $(this).attr('data-id');
    var inputMachineNameTd = row.find('td:nth-child(6)');
    var inputAreaTd = row.find('td:nth-child(7)');
    var sessionID = row.find('td:nth-child(3)').text();
    var buttonReplace = row.find('td:nth-child(9)');
    var selectMachineName = $('<select class="form-control" id="machine_name_var"></select>');
    inputMachineNameTd.empty().append(selectMachineName);
    getMachinesNamesApi();

    var inputArea = $('<select class="form-control" id="area_var"></select>');
    
    var areaOptions = ['Die Prep', 'Die Attach', 'Wirebond', 'Mold', 'EOL1', 'EOL2'];
    areaOptions.forEach(function(option) {
      var optionElement = $('<option></option>').text(option);
      inputArea.append(optionElement);
    });
    inputArea.val(inputAreaTd.text());

    inputAreaTd.empty().append(inputArea);
    var saveButton = $('<button type="button" id="edit" class="icon dripicons btn dripicons-plus btn btn-outline-primary save-btn" data-id="' + id + '"></button>');
    buttonReplace.empty().append(saveButton);
  });

  $('#machineResultTbl').on('click', '.save-btn', function () {
    var row = $(this).closest('tr');
    var id = $(this).attr('data-id');
    var inputMachineNameTd = row.find('td:nth-child(6)');
    var inputAreaTd = row.find('td:nth-child(7)');
    var sessionID = row.find('td:nth-child(4)').text();
    var selectMachineName = inputMachineNameTd.find('select').val();
    var selectArea = inputAreaTd.find('select').val();
    sendEmit(sessionID, selectMachineName)
    var formData = new FormData()
    formData.append('id', id);
    formData.append('selectMachineName', selectMachineName);
    formData.append('selectArea', selectArea);

    ajaxRequestUpdate('/insert_machine_name', formData)
  });

  // $('#controllerBtn').click(function () {
  //   controllerSave();
  // });

  function controllerSave() {
    var ip = $('#spanDataId').attr('data-ip');
    var controllerInput = $('#controllerInput').val();
  
    var formData = new FormData();
    formData.append('ip', ip);
    formData.append('controllerInput', controllerInput);
  
    ajaxRequestUpdateController('/insert_controller', formData);
  }

  function ajaxRequestUpdate(url, data) {
    $.ajax({
      url: url,
      data: data,
      method: 'POST',
      processData: false,
      contentType: false,
      beforeSend: function() {
      },
      success: function(data){
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: 'Your work has been saved',
          showConfirmButton: true,
        })
        ajaxRequestTable.ajax.reload();
        table.ajax.reload()
        $('#machine_name_var').replaceWith(data.machine_name);
        $('#area_var').replaceWith(data.area_var);
      }
    }).done(function(){
    });
  }

  function ajaxRequestUpdateController(url, data) {
    $.ajax({
      url: url,
      data: data,
      method: 'POST',
      processData: false,
      contentType: false,
      beforeSend: function() {
      },
      success: function(data){
        location.reload();
        var row = $(this).closest('div').find('input');
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: 'Your work has been saved',
          showConfirmButton: true,


        })
        table.ajax.reload();
        
      }
    }).done(function(){
    });
  }

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

function sendEmit(sessionID, machine_name_var) {
  var socket = io.connect();
  console.log("Session ID:", sessionID);
  socket.emit('custom_event', { 'sessionID': sessionID, 'machine_name_var': machine_name_var });


// Client-side code to handle the server's response
socket.on('response', function (data) {
  console.log('Received server response:', data);
  // Process the response data as needed
});

}


  

  
  
  
  
  



//   $('#machine-table').on('click', '.edit-btn', function () {
//     var id = $(this).data('id');
//     $.get('/machines/delete/' + id, function (machine) {
//       machineIdField.val(machine.id);
//       machineNameField.val(machine.name);
//       machinePathField.val(machine.path);
//       machineModal.modal('show');
//     });
//   });


//   function ajaxRequestShow(id) {  
//     $.ajax({
//       url: '/get_name',
//       method: 'POST',
//       data: { id: id }, 
//       success: function (response) {
//         ajaxRequestShowResponse(response)
//       },
//       error: function (error) {
//         console.log(error);
//       }
//     });
//   }

//   function ajaxRequestShowResponse(response){
//     var data = response.result;
//     var addControllerInputGroup = '';
//     if (data !== null) {
//       var fetchedIp = '';
//       for (var i = 0; i < data.length; i++) {
//         fetchedIp = data[i][1];
//         break;
//       }
//       $('#controller_ip').html(fetchedIp);
//       var controller_name = '';
//       var controller_id = '';
//       for (var i = 0; i < data.length; i++) {
//         fetchedIp = data[i][1];
//         controller_id = data[i][0];
//         controller_name = data[i][7]; 
//         break;
//       }
//       if (controller_name == null) {
//         var inputGroupExists = $('#inputGroup').length > 0;
//         if (!inputGroupExists) {
//           var addControllerInputGroup = '<div id="inputGroup">'
//             + '<div class="input-group mb-3">'
//             + '<input type="text" class="form-control" placeholder="" id="controller_name" aria-describedby="add-controller-name">'
//             + '<button class="btn btn-primary add-controller" type="button" id="add-controller-name" data-ip=' + fetchedIp + '>Controller</button>'
//             + '</div></div>';
//           $(addControllerInputGroup).insertAfter("#controller_ip");

//           $('#add-controller-name').click(function () {
//             var ip = $(this).data('ip');
//             console.log("🚀 ~ file: table.js:84 ~ ip:", ip)
//             // var controller_name_var = $('#controller_name').val()
//             // if (controller_name_var == '') {
//             //   Swal.fire({
//             //     icon: 'warning',
//             //     title: 'Error',
//             //     text: 'Enter you must something!.',
//             //     showConfirmButton: true,
//             //   })

//             // } else {
//             //   console.log('Clicked on button with IP:', ip, controller_name_var);
//             //   $.ajax({
//             //     url: '/insert_controller',
//             //     method: 'POST',
//             //     data: {
//             //       ip: ip,
//             //       controller_name_var: controller_name_var
//             //     },
//             //     success: function (response) {
//             //       Swal.fire({
//             //         icon: 'success',
//             //         title: 'Successfully saved!',
//             //         text: 'Controller Inserted!',
//             //         showConfirmButton: true,
//             //       })

//             //       // $('#myModal').modal('hide');
//             //       table.ajax.reload();
//             //     }
//             //   });

//             // }
//           });
//         } else {
//           console.log('Input group already exists.');
//         }
//       } else {
//         // If controller_name is not null, update the existing controller_span element
//         var controllerSpanExists = $('#controller_span').children().length > 0;
//         if (!controllerSpanExists) {
//           var span_controller = '<span>Controller name : ' + controller_name + '</span>';
//           var controller_button = '<button type="button" class="btn btn-outline-primary edit-controller-btn" data-id="' + controller_id + '">Edit</button>'
//           var controller_span = $('<div>').attr('id', 'controller_span').append(span_controller);
//           var button_class = $('<div>').attr('id', 'button_class').append(controller_button);
//           $(controller_span).insertAfter("#controller_ip");
//           $(button_class).insertAfter("#controller_span");
//         } else {
//           $('#controller_span').children().text('Controller name : ' + controller_name);
//           var editButton = $('<button>').attr('type', 'button').addClass('btn btn-outline-primary edit-controller-btn').attr('data-id', controller_id).text('Edit');
//           // Check if the button already exists before adding it
//           if ($('#button_class').find('.edit-controller-btn').length === 0) {
//             $('#controller_span').children().text('Controller name: ' + controller_name);
//             var editButton = $('<button>')
//               .attr('type', 'button')
//               .addClass('btn btn-outline-primary edit-controller-btn')
//               .attr('data-id', controller_id)
//               .text('Edit');
//             $('#button_class').append(editButton);
//           }

//         }
//         $('#controller_name').replaceWith('');
//         $('#add-controller-name').replaceWith('');
//       }

//       $('.edit-controller-btn').click(function () {
//         $("#controller_span").html('');

//         var saveEdittedController = $('<div id="inputGroup">')
//           .append($('<div class="input-group mb-3">')
//             .append($('<input type="text" class="form-control" placeholder="" id="controller_name" aria-describedby="add-controller-name">'))
//             .append($('<button class="btn btn-primary add-controller" type="button" id="add-controller-name">Controller</button>').data('ip', fetchedIp)));

//         $('#controller_span').append(saveEdittedController);
//         $('#button_class').html('');

//         $('#add-controller-name').click(function () {
//           var ip = $(this).data('ip');
//           var controller_name_var = $('#controller_name').val();

//           if (controller_name_var === '') {
//             Swal.fire({
//               icon: 'warning',
//               title: 'Error',
//               text: 'You must enter something!',
//               showConfirmButton: true,
//             });
//           } else {
//             console.log('Clicked on button with IP:', ip, controller_name_var);
//             $.ajax({
//               url: '/insert_controller',
//               method: 'POST',
//               data: {
//                 ip: ip,
//                 controller_name_var: controller_name_var
//               },
//               success: function (response) {
//                 Swal.fire({
//                   icon: 'success',
//                   title: 'Successfully saved!',
//                   text: 'Controller Updated!',
//                   showConfirmButton: true,
//                 });

//                 // $('#myModal').modal('hide');
//                 table.ajax.reload();
//               }
//             });
//           }
//         });
//       });


//       console.log("🚀 ~ file: table.js:82 ~ fetched_result:", controller_name)
//       var html = '';
//       for (var i = 0; i < data.length; i++) {
//         var id = data[i][0]; // Accessing Name
//         var status = data[i][2]; // Accessing status
//         var sid = data[i][3]; // Accessing sid
//         var port = data[i][4]; // Accessing port
//         var machine_name = data[i][5]; // Accessing machine_name
//         var area = data[i][6]; // Accessing area
//         var controller_name = data[i][7]; // Accessing controller_name


//         var input_machine_name = '<select id="machine_name_var" class="form-control" aria-describedby="save-btn"></select>';
//         var input_area = '<input type="text" class="form-control" id="area_var" aria-describedby="save-btn">';
//         var buttonClass = '';
//         var buttonIcon = '';
//         var buttonStatus = '';
//         var buttonClassName = '';


//         if (status === 'CONNECTED') {
//           buttonClass = 'btn-outline-success';
//           buttonIcon = 'dripicons-pencil';

//           buttonStatus = ''
//           if (machine_name !== null) {
//             input_machine_name = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span>';
//             buttonClassName = 'edit-btn'
//           } else {
//             buttonClass = 'btn-outline-primary';
//             buttonIcon = 'dripicons-plus';
//             buttonClassName = 'save-btn'
//           }
//           if (area !== null) {
//             input_area = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + area + '</span>';
//             buttonClassName = 'edit-btn'
//           } else {
//             buttonClass = 'btn-outline-primary';
//             buttonIcon = 'dripicons-plus';
//             buttonClassName = 'save-btn'
//           }


//         } else if (status === 'DISCONNECTED') {
//           buttonClass = 'disabled btn-danger';
//           buttonIcon = 'dripicons-warning';
//           buttonStatus = 'disabled'
//           input_machine_name = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + machine_name + '</span>';
//           input_area = '<span style="border:none; margin-right:50px;" aria-describedby="save-btn">' + area + '</span>';
//         } else {
//           buttonClass = 'disabled btn-primary';
//           buttonIcon = 'dripicons-warning';
//         }

//         html += '<tr>';
//         html += '<td>' + id + '</td>';
//         html += '<td><span class="badge ' + (status === 'CONNECTED' ? 'bg-success' : (status === 'DISCONNECTED' ? 'bg-danger' : 'bg-primary')) + '">' + status + '</span></td>';
//         html += '<td>' + sid + '</td>';
//         html += '<td>' + port + '</td>';
//         html += '<td>' + (status === 'CONNECTED' ? input_machine_name : input_machine_name.replace('type="text"', 'type="text" disabled')) + '</td>';
//         html += '<td>' + (status === 'CONNECTED' ? input_area : input_area.replace('type="text"', 'type="text" disabled')) + '</td>';
//         html += '<td><button class="icon dripicons ' + buttonIcon + ' btn ' + buttonClass + ' ' + buttonStatus + ' ' + buttonClassName + '" type="button" data-id="' + id + '"></button></td>';
//         html += '</tr>';

//       }

//       // Set the generated HTML as the content of the modal body
//       $('#modal-data').html(html);
//       // Show the modal
//       $('#myModal').modal('show');
//     } else {
//       // Handle case when data is empty or null
//       $('#modal-data').html('<tr><td colspan="4">No data available</td></tr>');
//       $('#myModal').modal('show');
//     }
//   }

//   $('#machine_result_id tbody').on('click', '.edit-btn', function () {
//     var row = $(this).closest('tr');
//     var id = $(this).attr('data-id');
//     console.log(id);
//     var inputMachineNameTd = row.find('td:nth-child(5)');
//     var inputAreaTd = row.find('td:nth-child(6)');
//     var sessionID = row.find('td:nth-child(3)').text(); // Get the text content of the sessionID cell
//     var buttonReplace = row.find('td:nth-child(7)');
  
//     var machineNameOptions = '<select class="form-control" id="machine_name_var">';
//     // Add your options here
//     machineNameOptions += '<option value="value="' + inputMachineNameTd.text() + '"">' + inputMachineNameTd.text() + '</option>';
//     machineNameOptions += '</select>';
  
//     inputMachineNameTd.html(machineNameOptions);
//     inputAreaTd.html('<input type="text" class="form-control" id="area_var" value="' + inputAreaTd.text() + '">');
//     buttonReplace.html('<button type="button" id="edit" class="icon dripicons btn dripicons-plus btn btn-outline-primary save-btn" data-id="' + id + '">');
//     // sendEmit(sessionID, inputMachineNameTd);
//   });

  



//   $('#machine_result_id tbody').on('click', '.save-btn', function () {
//     var row = $(this).closest('tr');
//     var id = $(this).attr('data-id');
//     var machine_name_var = $('#machine_name_var').val()
//     var area_var = $('#area_var').val()
//     var sessionID = row.find('td:nth-child(3)').text(); // Get the text content of the sessionID cell
//     sendEmit(sessionID, machine_name_var);
//     console.log(id, machine_name_var, area_var)
//     $('#default').modal('show');
//     if (machine_name_var == '' && area_var == '') {
//       Swal.fire({
//         icon: 'warning',
//         title: 'Error!',
//         showConfirmButton: true,
//         text: 'You must have enter something!.',
//       })
//     } else {
//       $.ajax({
//         url: '/insert_machine_name',
//         method: 'POST',
//         data: {
//           id: id,
//           machine_name_var: machine_name_var,
//           area_var: area_var
//         },
//         success: function (data) {
//           Swal.fire({
//             icon: 'success',
//             title: 'Saved!',
//             text: 'Succesfully Saved!.',
//           })
//           $('#default').modal('hide');
//           console.log('dataaaaa', data)
//           $('#machine_name_var').replaceWith(machine_name_var);
//           $('#area_var').replaceWith(area_var);
//         }
//       });
//     }
//   });

//   function sendEmit(sessionID, machine_name_var) {
//     var socket = io.connect();
//     console.log("Session ID:", sessionID);
//     socket.emit('custom_event', { 'sessionID': sessionID, 'machine_name_var': machine_name_var });
//   }

//   // Client-side code to handle the server's response
//   socket.on('response', function (data) {
//     console.log('Received server response:', data);
//     // Process the response data as needed
//   });

//   $('#machine-table').on('click', '.delete-btn', function () {
//     Swal.fire({
//       title: 'Are you sure?',
//       text: "You won't be able to revert this!",
//       icon: 'warning',
//       showCancelButton: true,
//       confirmButtonColor: '#3085d6',
//       cancelButtonColor: '#d33',
//       confirmButtonText: 'Yes, delete it!'
//     }).then((result) => {
//       if (result.isConfirmed) {
//         Swal.fire(
//           'Deleted!',
//           'Your file has been deleted.',
//           'success'
//         )
//         var id = $(this).data('id');
//         $.ajax({
//           url: '/machines/delete',
//           method: 'POST',
//           data: { id: id },
//           success: function (result) {
//             table.ajax.reload();
//           }
//         });
//       }
//       else
//         Swal.fire({
//           title: 'Think Again!',
//           icon: 'info',
//         })
//     })

//   });

//   function selectData() {
//     $.ajax({
//       url: "/getMachinesNamesApi",
//       type: "GET",
//       success: function (response) {
//         var machineNames = response;
//         var select = $("#machine_name_var");
//         // Populate select dropdown with machine names
//         $.each(machineNames, function (index, name) {
//           select.append($('<option></option>').val(name).html(name));
//         });
//       }
//     });

//   }


// });





