let loginForm = document.getElementById("loginForm");

// Handle logins
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  let username = document.getElementById("username");

  // Empty username field
  if (username.value == "" ) {
    alert("Please provide a value for the field!");
  } else {

    let data = {
      "username": username.value.toLowerCase(),
    };

    // Check user credentials: does this username already exist?
    fetch("/auth",
      {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
    	if (text=="success") {
          localStorage.setItem("username", data["username"])
        	location.href = "/home";
    	}
      else if (text=="no account"){
        alert("Account not found :(")
		  }

	  });
  }
  
});
