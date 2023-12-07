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
    alert("Ensure you input a value in both fields!");
  } else {
    // perform operation with form input
    alert("This form has been successfully submitted!");
    console.log(
      `This form has a username of ${username.value} and password of ${password.value}`
    );

    username.value = "";
    password.value = "";
  }
});