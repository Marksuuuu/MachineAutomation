function submitForm(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const data = {
    username: username,
    password: password
  };
  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => {
    if (response.ok) {
      window.location.href = '/index?success=true';
    } else {
      response.json().then(data => {
        alert(data.error);
      });
    }
  }).catch(error => {
    alert('An error occurred: ' + error);
  });
}



// $(document).ready(function() {
//   $('#addButton').click(function() {
//     var machine_name = $('input[name="machine_name"]').val();
//     var machine_path = $('input[name="machine_path"]').val();
//     $.ajax({
//       url: '/add-row',
//       type: 'POST',
//       data: {'machine_name': machine_name, 'machine_path': machine_path},
//       success: function(response) {
//         $('#addContainer').append(response);
//         $('input[name="machine_name"]').val('').appendTo('#addContainer');
//         $('input[name="machine_path"]').val('').appendTo('#addContainer');
//       },
//       error: function(error) {
//         console.log(error);
//       }
//     });
//   });
// });