// const apiBackendBaseUrl = "http://192.168.1.13:8000/recommendation-engine";
const apiBackendBaseUrl = "http://localhost:8000/recommendation-engine";


$(document).ready(function(){
    $("#signIn").click(function(event){
        event.preventDefault();
        var email = document.login.username.value;
        var password = document.login.password.value;
        var loginData = {
          email : email,
          password : password
        }
        console.log(loginData);
        var emailValidationCheck = validateEmail(email);
          if(emailValidationCheck){
            var url = apiBackendBaseUrl + "/login-customer";
            var settings = {
              "url": url,
              "method": "POST",
              "headers": {
                "Content-Type": "application/json"
              },
              "data": JSON.stringify(loginData),
            };
            
            $.ajax(settings).done(function (response) {
              if(response["status"] == 404){
                swal({
                  title: "Error",
                  text: response["message"],
                  icon: "error",
                });
              }
              if(response["status"] == 200){
                swal({
                  title: "Success",
                  text: response["message"],
                  icon: "success",
                });
                window.location.href = "index.html";
              }
            });
          }
          else{
            swal({
              title: "Error",
              text: "Please provide valid username",
              icon: "error",
            });
          }
       
    })
})

function registerUser(){
    var firstName = document.registration.firstName.value;
    var lastName = document.registration.lastName.value;
    var email = document.registration.email.value;
    var password = document.registration.password.value;
    var contactNo = document.registration.contactNo.value;
    var country = document.registration.country.value;
    var city = document.registration.city.value;

    if(firstName != "" && lastName != "" && email != "" && password != "" && contactNo != "" && country != "" && city != ""){
      var emailValidationCheck = validateEmail(email);
      if(emailValidationCheck){
        if(contactNo.toString().length < 10){
          swal({
            title: "Warning",
            text: "Please put 10 digit phone number",
            icon: "warning",
          });
        }
    
        else{
          var registrationData ={
            email : email,
            fName : firstName,
            lName : lastName,
            password : password,
            contactNo : contactNo,
            city : city,
            country : country
          }
          var registrationUrl = apiBackendBaseUrl + "/register-customer";
          var settings = {
              "url": registrationUrl,
              "method": "POST",
              "timeout": 0,
              "crossDomain": true,
              "headers": {
                "Content-Type": "application/json"
              },
              "data": JSON.stringify(registrationData),
          };
            
          $.ajax(settings)
            .done(function (response) {
              if(response["status"] == 200){
                swal({
                  title: "Success",
                  text: response["message"],
                  icon: "success",
                });
                window.location.href = "feedback.html";
              }
              if(response["status"] == 409){
                swal({
                  title: "Warning",
                  text: response["message"],
                  icon: "warning",
                });
              }
            });
    
          $.ajax(settings).fail(function (response) {
            swal({
              title: "Error",
              text: "Error occured",
              icon: "error",
            });
          }); 
        }
      }
      else{
        swal({
          title: "Error",
          text: "Please provide a valid email",
          icon: "error",
        });
      }
    }
    else{
      swal({
        title: "Error",
        text: "Please fill up all mandatory fields",
        icon: "error",
      });
    }

    
    

}

function validateEmail(email){
  var mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if(email.match(mailFormat)){
    return true;
  }
  else{
    return false;
  }
}


