let loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let username = document.getElementById("username");
  let password = document.getElementById("password");

  if (username.value == "" || password.value == "") {
    alert("Please provide a value for both fields!");
  } else {

    let data = {
      "username": username.value,
      "password": password.value
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
          location.href = "/home";
      }
	  else if (text=="already exists") {
			alert("Sorry, that username already exists. Try another one.")
	  }
      else {
          alert("Error creating new account!")
    }});


    username.value = "";
    password.value = "";
  }
});
// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/group_demo.js?ref_type=heads
// example JS file that creates chat
// steal

// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/one_to_one_demo.html?ref_type=heads
// one to one demo