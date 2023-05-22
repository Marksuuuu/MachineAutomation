$(document).ready(function(){
    $('#getConfig').click(function(){
        $('#requestConfig').modal('show');
        $('#getConfigInput').val('');
    })
     
    $('#submitData').click(function(){
        var getInput = $('#getConfigInput').val();
        if(getInput == ''){
            Swal.fire({
                icon: 'warning',
                title: 'Error!',
                text: 'Please Enter Something!',
            });
        }
        console.log(getInput)
        $.ajax({
            'url':'/request_data',
            'type':'POST',
            data: JSON.stringify(getInput),
            contentType: 'application/json',
            success: function(data){
                console.log(data)
    
            }
    
        });
    })
    


});