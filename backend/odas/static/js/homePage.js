function uploadPubFile() {
	let file = $("#fileInput")[0].files[0]; 
	if (file == undefined) {
		console.log("ER: Wybierz plik do wysłania") 
		addMessage(false, "Wybierz plik do wysłania")
		return
	}
	username = "jakis randomowy user"

	// get current username needed for upload file
	$.ajax({
		url : '/api/getUserKeyForSessionId',
		method : "post",
        dataType : "json" //oczekujemy odpowiedzi w formacie json
    })
	.done(function(response) {
		console.log(response)
		username = response["username"]
		if (response.success) {
			let form = new FormData()
     		form.append("file", file)
			// upload file
			$.ajax({
				url : '/api/files/' + username + "/pub/" + file.name,
				method : "post",
		        processData: false,
        		contentType: false,
        		data: form,
		    })
			.done(function(response) {
				console.log(response)
				if (response.success) {
					//window.location.reload(false); 
				} else {
					addMessage(false, response.message)
				}
			})
			.fail(function() {
				alert('There was an error');
			})

		} else {

		}
	})
	.fail(function() {
		alert('There was an error');
	})
}

function uploadPrivFile() {
	let file = $("#fileInput")[0].files[0]; 
	if (file == undefined) {
		console.log("ER: Wybierz plik do wysłania") 
		addMessage(false, "Wybierz plik do wysłania")
		return
	}
	username = "jakis randomowy user"

	// get current username needed for upload file
	$.ajax({
		url : '/api/getUserKeyForSessionId',
		method : "post",
        dataType : "json" //oczekujemy odpowiedzi w formacie json
    })
	.done(function(response) {
		console.log(response)
		username = response["username"]
		if (response.success) {
			let form = new FormData()
     		form.append("file", file)
			// upload file
			$.ajax({
				url : '/api/files/' + username + "/priv/" + file.name,
				method : "post",
		        processData: false,
        		contentType: false,
        		data: form,
		    })
			.done(function(response) {
				console.log(response)
				if (response.success) {
					window.location.reload(false); 
					//addMessage(true, response.message)
				} else {
					addMessage(false, response.message)
				}
			})
			.fail(function() {
				alert('There was an error');
			})

		} else {

		}
	})
	.fail(function() {
		alert('There was an error');
	})
}

function deletePubFile(filename) {
	// get current username needed for upload file
	$.ajax({
		url : '/api/getUserKeyForSessionId',
		method : "post",
        dataType : "json" //oczekujemy odpowiedzi w formacie json
    })
	.done(function(response) {
		console.log(response)
		username = response["username"]
		if (response.success) {
			// delete file
			$.ajax({
				url : '/api/files/' + username + "/pub/" + filename,
				method : "delete",
		        processData: false,
        		contentType: false,
		    })
			.done(function(response) {
				console.log(response)
				if (response.success) {
					window.location.reload(false); 
				} else {
					addMessage(false, response.message)
				}
			})
			.fail(function() {
				alert('There was an error');
			})

		} else {

		}
	})
	.fail(function() {
		alert('There was an error');
	})
}

function deletePrivFile(filename) {
	// get current username needed for upload file
	$.ajax({
		url : '/api/getUserKeyForSessionId',
		method : "post",
        dataType : "json" //oczekujemy odpowiedzi w formacie json
    })
	.done(function(response) {
		console.log(response)
		username = response["username"]
		if (response.success) {
			// delete file
			$.ajax({
				url : '/api/files/' + username + "/priv/" + filename,
				method : "delete",
		        processData: false,
        		contentType: false,
		    })
			.done(function(response) {
				console.log(response)
				if (response.success) {
					window.location.reload(false); 
				} else {
					addMessage(false, response.message)
				}
			})
			.fail(function() {
				alert('There was an error');
			})

		} else {

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
  	referenceElement = document.getElementById("title")
  	parent.insertBefore(newDiv, referenceElement)
}