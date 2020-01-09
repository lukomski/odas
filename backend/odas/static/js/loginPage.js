function login() {
	let username = document.getElementById("loginInput").value;
	let password = document.getElementById("passwordInput").value;

	$.ajax({
		url : '/api/authorize',
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
			console.log("OK: " + response.message)
			addMessage(true, response.message)
			window.location = '/'
		} else {
			console.log("ER: " + response.message)
			addMessage(false, response.message)
			//window.location = '/login?fail_message=' + response.message
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

  	mainRow = document.getElementById("mainRow");
  	document.getElementsByClassName("container")[0].insertBefore(newDiv, mainRow)
}