// let newChat = document.getElementById("newchat");

// newChat.addEventListener("submit", (e) => {

//   e.preventDefault();
//   console.log("HELLO")
//   document.getElementById("who_form").hidden = false;

// });


// window.onload = function() {
//   document.getElementById("who_form").hidden = true;
// };

// function startChat(){
// 	document.getElementById("who_form").hidden = false;
// }

function enterUser(){
  let friend = document.getElementById("friend").value;
  document.getElementById("friend").input = friend

  let data = {
	"friend": friend,
  };

  // Start a chat
  fetch("/startchat",
	{method: 'POST',
	headers: {'Content-Type': 'application/json'},
	body: JSON.stringify(data)})
  .then((response) => response.text())
  .then((text) => {
	  if (text=="success") {
		  alert("Creating new chat!")
		  location.href = "/home";
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
// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/group_demo.js?ref_type=heads
// example JS file that creates chat
// steal

// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/one_to_one_demo.html?ref_type=heads
// one to one demo