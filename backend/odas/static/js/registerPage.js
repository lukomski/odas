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
    console.log(response)
        if (response.success) {
          addMessage(true, response.message) 
        } else {
          addMessage(false, response.message)
        }
  })
  .fail(function() {
      alert('There was an error');
  })
}

function addMessage(success, msg) {
  newDiv = document.createElement("div");
  newDiv.class = "row"
  if (success) {
      newDiv.innerHTML = '<div class="alert alert-success" role="alert">' + msg + '</div>'
    } else {
      newDiv.innerHTML = '<div class="alert alert-danger" role="alert">' + msg + '</div>'
    }

    parent = document.getElementsByClassName("container")[0]
    referenceElement = document.getElementById("registerRow")
    parent.insertBefore(newDiv, referenceElement)
}