function enterUser(){
	let friend = document.getElementById("friend").value;
	document.getElementById("friend").input = friend

	let data = {
		"friend": friend,
	};

	// Verify desired user to chat with
	fetch("/checkfriend",
		{method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(data)})
	.then((response) => response.text())
	.then((text) => {

		// todo: add case for already have a chat with this person!
	  if (text=="success") {
		  createChat(friend)
	  }
		else if (text=="no account"){
		  alert("No account found with this username :( ")
	  } else if (text == "self chat") {
			alert("You can't chat with yourself, silly!")
	  }
	  	else if (text=="error") {
		  alert("Error logging in")
	  }});

}

function createChat(friend){
	let data = {
		"friend": friend,
	};

	// Verify desired user to chat with
	fetch("/createchat",
		{method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(data)})
	.then((response) => response.text())
	.then((text) => {
		if(text == "success") {
		}
	});

}
// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/group_demo.js?ref_type=heads
// example JS file that creates chat
// steal

// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/one_to_one_demo.html?ref_type=heads
// one to one demo