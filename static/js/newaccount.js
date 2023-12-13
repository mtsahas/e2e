let loginForm = document.getElementById("loginForm");

document.addEventListener("DOMContentLoaded", function() {
  Olm.init()

}, false);

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let username = document.getElementById("username");

  if (username.value == "") {
    alert("Please provide a value for the field!");
  } else {

    let data = {
      "username": username.value,
    };

    // Handle announcement
    fetch("/addcredentials",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
      if (text=="success") {
          alert("Successfully logged in!")
          createOlmAcc();
          // call function to create olm accounts, set local storage, send public keys (ot key + id key)
          //location.href = "/home"; // do we need this idk
      }
	  else if (text=="already exists") {
			alert("Sorry, that username already exists. Try another one.")
	  }
      else {
          alert("Error creating new account!")
    }});


    username.value = "";
  }
});

function createOlmAcc(){
    window.user= new Olm.Account();
    user.create()
    user.generate_one_time_keys(5)
    id_keys = JSON.parse(user.identity_keys())
    id_key_private = id_keys.ed25519
    id_key_public = id_keys.curve25519
    one_time_keys = JSON.parse(user.one_time_keys())
    var user_ot_keys = []
    for (key in one_time_keys.curve25519) {
        user_ot_keys.push(one_time_keys.curve25519[key]);
    }
 

    let data = {"id_key":id_key_public, "one_time_keys":user_ot_keys}
    // Handle announcement
    fetch("/receivekeys",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
      if (text=="success") {
          alert("Successfully sent keys!")
          localStorage.setItem("id_keys", user.identity_keys());
      
          // call function to create olm accounts, set local storage, send public keys (ot key + id key)
          //let user_string = user.pickle(user.identity_keys()) // does this work..?
          let user_string = user.pickle(user.identity_keys())
          localStorage.setItem("olm_acc", user_string);

          location.href = "/home";
      }

      else {
          alert("Error sending ")
    }});


    // alert(one_time_keys)
    // alert(id_key_private)
    // alert(id_key_public)
}
// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/group_demo.js?ref_type=heads
// example JS file that creates chat
// steal