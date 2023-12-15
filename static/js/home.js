// Who are we currently chatting with?
var chatter = ""

// Who are we?
var author = localStorage.getItem("username")

// Olm global variables
var u_session 
var user

// Initialize Olm
document.addEventListener("DOMContentLoaded", function() {
	Olm.init()
  }, false);


// Pretty printing
const log = (text, color) => {
	document.getElementById('log').innerHTML += `<span style="color: ${color}">${text}</span><br>`;
  };
  
// Creating web socket with sever
const socket = new WebSocket('ws://' + location.host + '/handle');

// Handle receiving messages from server through socket
socket.addEventListener('message', ev => {

	let data = ev.data
	let json_data = JSON.parse(data)

	// Receiving normal message from server after olm handshake
	if (json_data["type"]=="message"){
		sender = json_data["from"]
		message = json_data["message"]
		decrypted = u_session.decrypt(message.type, message.body)
		formatted_string = sender+": "+decrypted
		
		// Uncomment to display encrypted message
		// log("Encrypted: "+JSON.stringify(message.body), "red")
		
		log(formatted_string, 'purple');
	}

	// Receiving information about some other user's public keys from server
	else if (json_data["type"]=="key_send"){
		
		// Create an empty olm account to pickle and unpickle our account from local storage
		user = new Olm.Account()
		let id_keys = localStorage.getItem("id_keys");
		let user_str = localStorage.getItem("olm_acc")
		user.unpickle(id_keys, user_str)
		id_keys = user.identity_keys()

		// Create session for client and their desired receiver
		u_session = new Olm.Session();
		receiver_id_key = json_data["id_key"]
		receiver_ot_key = json_data["ot_key"]

		// Create outbound with keys of desired receiver
		u_session.create_outbound(user, receiver_id_key, receiver_ot_key);
		message1 = u_session.encrypt("You are now chatting with " + author + "!");
		log("You are now chatting with " +  chatter + "!", 'black');
		let data = {
			"type": "invite",
			"to": chatter,
			"from": author,
			"message": message1
		}
		socket.send(JSON.stringify(data));
	}
	// Receiving invite to chat from other user
	else if (json_data["type"]=="invite"){
		
		// Unpickle account from local storage
		user = new Olm.Account()
		let id_keys = localStorage.getItem("id_keys");
		let user_str = localStorage.getItem("olm_acc")
		user.unpickle(id_keys, user_str)
		id_keys = user.identity_keys()
		message1 = json_data["message"]

		// Create inbound session
		u_session = new Olm.Session();
		u_session.create_inbound(user, message1.body);
		// Decrypt first message
		plaintext = u_session.decrypt(message1.type, message1.body);
		chatter = json_data["sender"]

		document.getElementById('chat_header').innerHTML = "Chat with "+chatter
		
		log(plaintext, 'black');
	}
	else if (json_data["type"]=="error"){
		alert("Something went wrong. Try reloading or contacting the server administrator.")
	}

});

// Send message to server through socket
document.getElementById('form').onsubmit = ev => {
	ev.preventDefault();
	if (chatter == ""){
		alert("Who do you want to chat with silly goose?")
		return
	}
	else{
		const textField = document.getElementById('text');
		log('me: ' + textField.value, 'blue');

		let data = {
			"type": "message",
			"to": chatter,
			"from": author,
			"msg": u_session.encrypt(textField.value)
		}
		socket.send(JSON.stringify(data));
		textField.value = '';
	}
};

// Invite user to chat through server
function enterUser(){
	let friend = document.getElementById("friend").value;
	document.getElementById("friend").input = friend
	let data = {
		"friend": friend,
	};

	// Verify desired user has an account
	fetch("/checkfriend",
		{method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(data)})
	.then((response) => response.text())
	.then((text) => {
	  if (text=="success") {
			chatter = friend.toLowerCase()
			document.getElementById('chat_header').innerHTML = "Chat with "+chatter

			// Ask server for desired receiver's public keys
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

// Ask server for desired receiver's public keys
function intializeChat(){
	let req = {"type":"key_query", "to": chatter, "from": author, "message":""}
	socket.send(JSON.stringify(req))
}