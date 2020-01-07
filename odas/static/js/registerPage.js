function register() {
  let username = document.getElementById("loginInput").value;
  let password = document.getElementById("passwordInput").value;

  $.ajax({
    url : '/api/adduser',
    method : "post",
      data : {
        username : username,
        password : password
        },
      dataType : "json" //oczekujemy odpowiedzi w formacie json
  })
  .done(function(response) {
    console.log(response);
  })
  .fail(function() {
      alert('There was an error');
  })
}