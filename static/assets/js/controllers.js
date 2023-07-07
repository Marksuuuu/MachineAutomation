var resTable = null;

$(document).ready(function() {
  select2Options();

  $('#controllerBtn').click(function() {
    var controllerInput = $('#controllerInput').val();
    var formData = new FormData();
    formData.append('controllerInput', controllerInput);
    ajaxRequest('/insertController', formData);
  });

  var table = $('#machine-table').DataTable({
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
    order: [[1, 'asc']],
    initComplete: function () {
      var firstRowData = table.row(0).data();
      if (firstRowData) {
        // Do something with the firstRowData
      }
    }
  });

  $('#machine-table').on('click', '.add-machine', function(){
    var data_id = $(this).attr('data-id');
    $('#dataController').attr('data-controller', data_id);
    $('#inlineForm').modal('show');
    var formData = new FormData();
    formData.append('data_id', JSON.stringify(data_id));
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
        if (response && response.results && Array.isArray(response.results)) {
          var machines = response.results;
          var selectData = machines.map(function(machine) {
            return {
              id: machine.id,
              text: machine.port,
              data: machine
            };
          });
          var selectElement = $('#machine-select');
          selectElement.select2({
            data: selectData,
            dropdownParent: '#inlineForm',
            width: '100%',
            tags: true
          });
          selectElement.on('change', function() {
            var selectedOptions = selectElement.select2('data');
            $('#resTbody').empty();
            selectedDataArray = [];
            selectedOptions.forEach(function(option) {
              var selectedData = option.data;
              appendToTable(selectedData);
              selectedDataArray.push(selectedData);
            });
            saveSelectedData();
            table.ajax.reload()
             
          });
        }
      }
    });
  }

  function appendToTable(machineData) {
    var tbody = $('#resTbody');
    var row = $('<tr>');
    row.append($('<td>').text(machineData.id));
    row.append($('<td>').text(machineData.fetched_ip));
    row.append($('<td>').text(machineData.status));
    row.append($('<td>').text(machineData.sid));
    row.append($('<td>').text(machineData.port));
    row.append($('<td>').text(machineData.machine_name));
    row.append($('<td>').text(machineData.area));
    row.append($('<td>').text(machineData.start_date));
    row.append($('<td>').text(machineData.stop_date));
    tbody.append(row);
  }

  function saveSelectedData() {
    var dataControllerID = $('#dataController').attr('data-controller');
    console.log("dataControllerID:", dataControllerID);
    console.log("selectedDataArray:", selectedDataArray);
    var formData = new FormData();
    formData.append('selectedDataArray', JSON.stringify(selectedDataArray));
    formData.append('dataControllerID', JSON.stringify(dataControllerID));
    ajaxRequestControllerResult('/processSelectedData', formData);
  }

  function ajaxRequest(url, data) {
    $.ajax({
      url: url,
      method: 'POST',
      data: data,
      processData: false,
      contentType: false,
      beforeSend: function() {
        // Code to execute before sending the AJAX request
        $('#resTable').DataTable().destroy()
        $('#resTbody').html('')
      },
      success: function(data) {
        console.log("🚀 ~ file: controllers.js:145 ~ ajaxRequest ~ data:", data)
        var dataResult = data.data
        console.log("🚀 ~ file: controllers.js:152 ~ ajaxRequest ~ dataResult:", dataResult)
        dataResult.forEach(function(row) {
          var newRow = '<tr>' +
            '<td>' + row.ID + '</td>' +
            '<td>' + row.FETCHED_IP + '</td>' +
            '<td>' + row.STATUS + '</td>' +
            '<td>' + row.SID + '</td>' +
            '<td>' + row.PORT + '</td>' +
            '<td>' + row.MACHINE_NAME + '</td>' +
            '<td>' + row.AREA + '</td>' +
            '<td>' + row.START_DATE + '</td>' +
            '<td>' + row.STOP_DATE + '</td>' +
            '<td>' + row.REMARKS + '</td>' +
            '</tr>';
          $('#resTbody').append(newRow);
        });
           $('#resTable').DataTable({
            processing: true,
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
          });
      }
    }).done(function() {
    });
  }

  function ajaxRequestControllerResult(url, data) {
    $.ajax({
      url: url,
      method: 'POST',
      data: data,
      processData: false,
      contentType: false,
      success: function(data) {
        console.log("data:", data);
      },
    }).done(function() {
      // Code to execute after the AJAX request is done
    });
  }
});