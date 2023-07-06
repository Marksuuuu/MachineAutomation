var table

$(document).ready(function(){
  select2Options()

  $('#controllerBtn').click(function(){
    var controllerInput = $('#controllerInput').val();

    var formData = new FormData();
    formData.append('controllerInput', controllerInput);

    ajaxRequest('/insertController', formData)
  })


  table = $('#machine-table').DataTable({
    processing: true,
    ajax: '/controllersViewData',
    lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    columns: [
      { data: 'id' },
      {
        data: 'remarks',
        className: 'text-center',
        render: function (data, type, row) {
          if (data == null || data === '') {
            return '<div class="form-group with-title mb-3">' +
              '<textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>' +
              '<label>Your Remarks</label>' +
              '</div>';
          } else {
            return '<span class="badge bg-primary" style="width: auto; height: auto; font-size:20px;">' + data + '</span>';
          }
        },
      },
      {
        data: 'controller_name',
        className: 'text-center',
        render: function (data) {
          return '<span class="badge bg-primary" style="width: auto; height: auto; font-size:20px;">' + data + '</span>';
        },
      },
      {
        data: null,
        className: 'text-center',
        render: function (row) {
          return '<button type="button" class="btn btn-outline-info icon icon dripicons dripicons-plus add-machine" data-id="' + row.id + '"></button> ' +
            ' <button type="button" class="btn btn-outline-danger icon dripicons dripicons-trash delete-btn" data-id="' + row.id + '"></button>';
        },
      },
    ],
    "order": [[1, 'asc']],
    initComplete: function () {
      var firstRowData = table.row(0).data();
      if (firstRowData) {
        var controller_name = firstRowData.id;
        $('#dataController').attr('data-controller', controller_name)
      }
    },
    "order": [[1, 'asc']]
  });

  $('#machine-table').on('click', '.add-machine', function(){
    var id = $(this).attr('data-id');
    $('#inlineForm').modal('show')


    var formData = new FormData();
    formData.append('data_id', JSON.stringify(id))
    ajaxRequest('/viewControllerResult', formData);

  });
  
  $('#machine-table').on('click', '.delete-btn', function(){
    var id = $(this).attr('data-id');
    console.log("Clicked on delete button with id:", id);
  });


  function select2Options() {
    $.ajax({
      url: '/insertMachinesToController',
      method: 'GET',
      success: function(response) {
        console.log('Response:', response);
  
        if (response && response.results && Array.isArray(response.results)) {
          var machines = response.results;
  
          var selectData = machines.map(function(machine) {
            return {
              id: machine.id,
              text: machine.text
            };
          });
  
          var selectElement = $('#machine-select');
          console.log("🚀 ~ file: controllers.js:83 ~ select2Options ~ selectElement:", selectElement);
          selectElement.select2({
            data: selectData,
            dropdownParent: '#inlineForm',
            width: '100%',
            tags: true
          });
          
          $('#submitClick').click(function () {  
            // var inputData = $('#inputData').val()
            // console.log("🚀 ~ file: controllers.js:93 ~ inputData:", inputData)
            var data_id = $('#dataController').attr('data-controller')
            console.log("🚀 ~ file: controllers.js:104 ~ data_id:", data_id)
            var selectedData = selectElement.select2('data');
            
            console.log('Selected Data:', selectedData);
            var formData = new FormData();
            formData.append('selectedData', JSON.stringify(selectedData));
            formData.append('data_id', JSON.stringify(data_id))

            ajaxRequest('/processSelectedData', formData);
  
          })

  
          // selectElement.on('select2:select', function(e) {
          //   var selectedData = selectElement.select2('data');
          //   console.log('Selected Data:', selectedData);
  
          //   var formData = new FormData();
          //   formData.append('selectedData', JSON.stringify(selectedData));
  
          //   ajaxRequest('/processSelectedData', formData);
          // });
        } else {
          console.error('Invalid response data format.');
        }
      },
      error: function() {
        console.error('Failed to fetch machine data.');
      }
    });
  }
  
  
  
  
})

function ajaxRequest(url, data) {
  $.ajax({
    url: url,
    method: 'POST',
    data: data,
    processData: false, // Corrected typo: processData instead of proccessData
    contentType: false,
    beforeSend: function() {
      // Code to execute before sending the AJAX request
    },
    success: function() {
    //   Swal.fire({
    //     icon: 'success',
    //     title: 'Added!',
    // })
    //   table.ajax.reload()
    },
  }).done(function() {
    // Code to execute after the AJAX request is done
  });
}