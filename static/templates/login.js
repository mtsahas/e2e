function say_hi(){
    console.log("hey")
}
// https://www.freecodecamp.org/news/how-to-submit-a-form-with-javascript/#:~:text=To%20get%20this%20form's%20data,JavaScript%20using%20their%20document%20methods.
let loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let username = document.getElementById("username");
  let password = document.getElementById("password");

  if (username.value == "" || password.value == "") {
    alert("Please provide a value for both fields!");
  } else {
    // perform operation with form input
    //alert("This form has been successfully submitted!");
    console.log(
      `This form has a username of ${username.value} and password of ${password.value}`
    );

    let data = {
      "username": username.value,
      "password": password.value
    };

    // Check user credentials
    fetch("/auth",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
    	if (text=="success") {
        	alert("Successfully logged in!")
        	location.href = "/home";
    	}
      	else if (text=="no account"){
        	alert("Account not found")
    	} else if (text=="incorrect credentials") {
			alert("Incorrect username or password.")
		} else if (text=="error") {
			alert("Error logging in")
		}

	});


    username.value = "";
    password.value = "";
  }
});
// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/group_demo.js?ref_type=heads
// example JS file that creates chat
// steal

// https://gitlab.matrix.org/matrix-org/olm/-/blob/master/javascript/demo/one_to_one_demo.html?ref_type=heads
// one to one demo