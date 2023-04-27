$(document).ready(function () {
    $('#check-ip-tbl').hide();
    //maximum input boxes allowed
    var InputsWrapper = $("#addContainer"); //Input boxes wrapper ID
    var AddButton = $("#addButton"); //Add button ID
    var x = InputsWrapper.find('div').length; //initial text box count
    var FieldCount = x; //to keep track of text box added

    $(AddButton).click(function (e) { //on add input button click
        $.ajax({
            url: "/get-max-inputs", // replace with the URL to your server-side script
            type: "POST",
            datatype: 'json',
            success: function (data) {
                var MaxInputs = data.data[0].max_inputs;
                console.log(MaxInputs)
                if (x < MaxInputs) { //max input box allowed
                    FieldCount++; //text box added increment
                    //add input box
                    var display = '<div class="input-group mb-3">'
                        + '<input type="file" name="addMachine[]"'
                        + 'class="form-control addMachineClass"'
                        + 'placeholder="Machine Name"'
                        + 'id="field_' + FieldCount + '"'
                        + 'aria-label="Example text with button addon"'
                        + 'aria-describedby="button-addon1"/>'
                        + '<button href="#" type="button" class="btn btn-danger removeclass">×</button>'
                        + "</div>";
                    $(InputsWrapper).append(display);
                    x++; //text box increment
                }
                console.log(data); // handle the server response here
            },
            error: function (xhr, status, error) {
                console.log("An error occurred: " + error);
            }
        });
        return false;
    });



    $("body").on("click", ".removeclass", function (e) { //user click on remove text
        if (x > 1) {
            $(this).parent('div').remove(); //remove text box
            x--; //decrement textbox
        }
        return false;
    })

    $('#submit').click(function () {
        var form = $('#add-machine')[0];
        var formData = new FormData(form);
        formData.append('controllerInput', formData.get('controllerInput'));
        formData.append('controllerIp', formData.get('controllerIp'));
        $.ajax({
            url: "/addMachines",
            method: "POST",
            data: formData,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function (data) {
                Swal.fire({
                    icon: 'success',
                    title: 'Saved!',
                    showConfirmButton: false,
                    timer: 2000,
                    text: data.msg
                })
                $('#resultbox').html(data);
            }
        });
    });
    $("#button-addon1").click(function (e) {
        e.preventDefault();
        var form = $('#add-machine')[0];
        var formData = new FormData(form);
        var tbody = $('#check-ip-tbl-tbody')
        formData.append('controllerIp', formData.get('controllerIp'));
        $.ajax({
            url: "/check-ip-addcontroller",
            method: "POST",
            data: formData,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,
            success: function (data) {
                var result = data.data;
                if (result != null) {
                    console.log(data, result.length);
                    $('#check-ip-tbl').show();
                    var var_tbody = '';
                    for (var x = 0; x < result.length; x++) {
                        var fileName = result[x].file_name;
                        if (fileName) {
                            var_tbody += '<tr>'
                                + '<td>' + fileName + '</td>'
                                + '<td><button class="btn btn-info" type="button" id="button-addon1">CHECK IP</button></td>'
                                + '</tr>';
                        } else {
                            console.log('File name is empty');
                        }
                    }
                    tbody.html(var_tbody);
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'No Data Found!',
                        showConfirmButton: false,
                        timer: 2000,
                        text: data
                    })

                }


            },
            // error: function (xhr, status, error) {
            //     Swal.fire({
            //         title: 'SQL Error',
            //         text: 'Please contact MIS (Loc 267)!',
            //         icon: 'error',
            //         allowOutsideClick: false
            //     });
            // }
        });
    });
    $("#openBtn").click(function (e) {
        $('#inlineForm').modal('show');
    })
});


// Swal.fire({
//     icon: 'success',
//     title: 'Saved!',
//     showConfirmButton: false,
//     timer: 2000,
//     text: data
// })
