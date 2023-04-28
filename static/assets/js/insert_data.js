$(document).ready(function () {
    $('#check-ip-tbl').hide();
    //maximum input boxes allowed
    var InputsWrapper = $("#addContainer"); //Input boxes wrapper ID
    var AddButton = $("#addButton"); //Add button ID
    var x = InputsWrapper.find('div').length; //initial text box count
    var FieldCount = x; //to keep track of text box added
    var ipAddress;
    var MaxInputsGlobal;

    $(AddButton).click(function (e) { //on add input button click
        $.ajax({
            url: "/get-max-inputs", // replace with the URL to your server-side script
            type: "POST",
            datatype: 'json',
            success: function (data) {
                // if (ipAddress == data.data.remote_ip_address){
                // }
                if (x < MaxInputsGlobal) { //max input box allowed
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
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Max Inputs reached!',
                        text: 'expected ' + MaxInputsGlobal,
                        showConfirmButton: true,
                    })
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
        console.log(formData)
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
            beforeSend: function () {
                $('#waitMemodal').waitMe({
                    effect: 'rotateplane',
                    text: 'Please wait...',
                    bg: 'rgba(255,255,255,0.7)',
                    color: '#435ebe',
                    maxSize: '',
                    waitTime: -1,
                    textPos: 'vertical',
                    fontSize: '',
                    source: ''
                });
            },
            success: function (data) {
                var result = data.data;
                MaxInputsGlobal = result[0].max_inputs
                Swal.fire({
                    icon: 'success',
                    title: 'Found!',
                    showConfirmButton: true,
                    text: 'Maximum Inputs ' + MaxInputsGlobal,
                })
                console.log('MaxInputs', MaxInputsGlobal)

                // Handle the result here

            },
            error: function (xhr, status, error) {
                Swal.fire({
                    title: 'SQL Error',
                    text: 'Please contact MIS (Loc 267)!',
                    icon: 'error',
                    allowOutsideClick: false
                });
            }
        }).done(function () {
            $('#waitMemodal').waitMe('hide');
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
