$(document).ready(function () {
    var MaxInputs = 8; //maximum input boxes allowed
    var InputsWrapper = $("#addContainer"); //Input boxes wrapper ID
    var AddButton = $("#addButton"); //Add button ID

    var x = InputsWrapper.find('div').length; //initial text box count
    var FieldCount = x; //to keep track of text box added

    $(AddButton).click(function (e) { //on add input button click
        if (x < MaxInputs) { //max input box allowed
            FieldCount++; //text box added increment
            //add input box
            $(InputsWrapper).append('<div class="input-group mb-3"><input type="file" name="addMachine[]" class="form-control addMachineClass" placeholder="Machine Name" id="field_' + FieldCount + '" aria-label="Example text with button addon" aria-describedby="button-addon1"/><button href="#" type="button" class="btn btn-danger removeclass">×</button></div>');
            x++; //text box increment
        }
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
                    timer: 2000
                })
                $('#resultbox').html(data);
            }
        });
    });
});



