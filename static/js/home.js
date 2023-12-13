// who are we talking to currently
var chatter = ""
var author = document.getElementById('username').innerHTML

document.addEventListener("DOMContentLoaded", function() {
	Olm.init()
  
  }, false);
  


const log = (text, color) => {
	document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
  };

const socket = new WebSocket('ws://' + location.host + '/echo');
  socket.addEventListener('message', ev => {
	// have to deal with different kinds of stuff coming back through sock

	let data = ev.data
	let json_data = JSON.parse(data)
	if (json_data["type"]=="message"){
		log(json_data["message"], 'purple');
	}
	if (json_data["type"]=="key_send"){
		//log(json_data["message"], 'purple');
		let user = new Olm.Account()
		let id_key = localStorage.getItem("id_key");
		alert(id_key)
		let user_str = localStorage.getItem("olm_acc")
		alert(user_str)
		user.unpickle(user_str, user.identity_keys) //????
		alert(user)
		alert(JSON.parse(user.identity_keys()))
	}

	
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
			// want to chat w new friend
			intializeChat()
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
function intializeChat(){
	// step 1: ask for keys
	// request to talk to someone (key_query)
	let req = {"type":"key_query", "to": chatter, "from": author, "message":""}
	// sends request to server for keys
	socket.send(JSON.stringify(req))
}