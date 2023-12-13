// who are we talking to currently
var chatter = ""
var author = document.getElementById('username').innerHTML



const log = (text, color) => {
	document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
  };

const socket = new WebSocket('ws://' + location.host + '/echo');
  socket.addEventListener('message', ev => {
	log(ev.data, 'purple');
});

document.getElementById('form').onsubmit = ev => {
	ev.preventDefault();
	if (chatter == ""){
		alert("Who do you want to chat with silly goose?")
		return
	}
	else{
	
		const textField = document.getElementById('text');
		log('me: ' + textField.value, 'blue');

		// should add additional info: send to, from, msg
		let data = {
			"type": "message",
			"to": chatter,
			"from": author,
			"msg": textField.value
		}
		socket.send(JSON.stringify(data));
		textField.value = '';
	}
};



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
			chatter = friend
			alert("Yay!")
			document.getElementById('chat_header').innerHTML = "Chat with "+chatter
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