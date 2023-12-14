let loginForm = document.getElementById("loginForm");

// Initialize Olm
document.addEventListener("DOMContentLoaded", function() {
  Olm.init()}, false);

// Handle logins
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let username = document.getElementById("username");

  // Empty username field
  if (username.value == "") {
    alert("Please provide a value for the field!");
  } else {

    let data = {
      "username": username.value.toLowerCase()
    };

    // Checks if username already exists
    fetch("/addcredentials",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
      if (text=="success") {
          localStorage.setItem("username", data["username"])

          // Perform user key setup with Olm
          createOlmAcc();
      }
	  else if (text=="already exists") {
			alert("Sorry, that username already exists. Try another one.")
	  }
      else {
          alert("Error creating new account!")
    }});

  }
});

// Sets up Olm Account and sends public keys to server
function createOlmAcc(){
    window.user= new Olm.Account();
    user.create()
    user.generate_one_time_keys(100)
    id_keys = JSON.parse(user.identity_keys())
    id_key_public = id_keys.curve25519
    one_time_keys = JSON.parse(user.one_time_keys())
    var user_ot_keys = []
    for (key in one_time_keys.curve25519) {
        user_ot_keys.push(one_time_keys.curve25519[key]);
    }

    let data = {"id_key":id_key_public, "one_time_keys":user_ot_keys}
    
    // Sending public keys to be stored on server
    fetch("/receivekeys",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
      if (text=="success") {
          // Store client's Olm account in local storage
          localStorage.setItem("id_keys", user.identity_keys());
          let user_string = user.pickle(user.identity_keys())
          localStorage.setItem("olm_acc", user_string);

          // Redirect to home page
          location.href = "/home";
      }

      else {
          alert("Error sending")
    }});

}