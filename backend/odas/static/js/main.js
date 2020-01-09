function logout() {
	console.log("Should logout now TODO")

	$.ajax({
		url : '/api/logout',
		method : "post",
        dataType : "json" //oczekujemy odpowiedzi w formacie json
    })
	.done(function(response) {
		console.log(response)
		if (response.success) {
			deleteCookie("session_id")
			window.location = '/login'
		} else {
			window.location = '/login'
		}
	})
	.fail(function() {
		alert('There was an error');
	})
}

function deleteCookie(cname) {
    var d = new Date(); //Create an date object
    d.setTime(d.getTime() - (1000*60*60*24)); //Set the time to the past. 1000 milliseonds = 1 second
    var expires = "expires=" + d.toGMTString(); //Compose the expirartion date
    window.document.cookie = cname+"="+"; "+expires;//Set the cookie with name and the expiration date
}