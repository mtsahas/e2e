const log = (text, color) => {
	document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
  };

  const socket = new WebSocket('ws://' + location.host + '/shawty');
  const socket2 = new WebSocket('ws://' + location.host + '/echo');
  socket2.addEventListener('message', ev => {
	log('<<< ' + ev.data, 'blue');
  });

  document.getElementById('form').onsubmit = ev => {
	ev.preventDefault();
	const textField = document.getElementById('text');
	log('>>> ' + textField.value, 'red');

	// should add additional info: send to, from, msg
	socket2.send(textField.value);
	socket.send(textField.value)
	textField.value = '';
  };




document.addEventListener('DOMContentLoaded', function(){


/*
		const websocketClient = new WebSocket("ws://localhost:5003");

	const messageContainer = document.querySelector("#message_container");
	const messageInput = document.querySelector("[name=message_input]");
	const sendMessageButton = document.querySelector("[name=send_message_button]");

	websocketClient.onopen = function(){
		console.log("Client connected!");

		sendMessageButton.onclick = function(){
			websocketClient.send(messageInput.value)
		};

		websocketClient.onmessage = function(message){
			console.log(message)
			const newMessage = document.createElement("div");
			newMessage.innerHTML = message.data;
			messageContainer.appendChild(newMessage)
		}
	}
	*/

});








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