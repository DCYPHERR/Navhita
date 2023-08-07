const passwordField = document.getElementById("password");
const togglePasswordVisibility = document.getElementById("togglePasswordVisibility");

togglePasswordVisibility.addEventListener("change", function() {
  if (this.checked) {
    passwordField.type = "text";
  } else {
    passwordField.type = "password";
  }
});

const loginButton = document.getElementById("loginButton");

loginButton.addEventListener("click", function(e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = passwordField.value;

  if (email === "" || password === "") {
    alert("Please fill in all fields.");
  } else {
    // Perform login validation here
    console.log("Email: " + email + ", Password: " + password);
  }
});
