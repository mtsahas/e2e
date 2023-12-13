// who are we talking to currently
var chatter = ""
var author = document.getElementById('username').innerHTML
var u_session // can i do this
var user

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
		sender = json_data["from"]
		message = json_data["message"]
		decrypted = u_session.decrypt(message.type, message.body)
		formatted_string = sender+": "+decrypted
		log(formatted_string, 'purple');
	}
	else if (json_data["type"]=="key_send"){
		//log(json_data["message"], 'purple');
		user = new Olm.Account()
		let id_keys = localStorage.getItem("id_keys");
		// alert(id_key)
		let user_str = localStorage.getItem("olm_acc")
		user.unpickle(id_keys, user_str) //????
		id_keys = user.identity_keys()

		// ok now i know who i am!!!! and i have keys !!!!
		// create outbound session
		u_session = new Olm.Session();
		receiver_id_key = json_data["id_key"]
		receiver_ot_key = json_data["ot_key"] // this one is fucked up
		alert(receiver_id_key)
		alert(receiver_ot_key)
		u_session.create_outbound(user, receiver_id_key, receiver_ot_key);
		message1 = u_session.encrypt("SHAWTY");
		log("Created outbound session", 'green');
		let data = {
			"type": "invite",
			"to": chatter,
			"from": author,
			"message": message1
		}
		socket.send(JSON.stringify(data));
	}
	else if (json_data["type"]=="invite"){
		user = new Olm.Account()
		let id_keys = localStorage.getItem("id_keys");
		let user_str = localStorage.getItem("olm_acc")
		user.unpickle(id_keys, user_str)
		id_keys = user.identity_keys()
		message1 = json_data["message"]

		// ok now i know who i am!!!! and i have keys !!!!
		// create outbound session
		u_session = new Olm.Session();
		alert("about to do inbound")
		u_session.create_inbound(user, message1.body);
		plaintext = u_session.decrypt(message1.type, message1.body);
		log(plaintext, 'purple');
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
			"msg": u_session.encrypt(textField.value)
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