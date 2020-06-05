
apiBackendBaseUrl=environments.apiBackendBaseUrl;
imageBaseUrl=environments.imageBaseUrl;



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
              console.log("Response in login ----------",response.status,response);
             
              if(response["status"] == 404){
                swal({
                  title: "Error",
                  text: response["message"],
                  icon: "error",
                });
              }
              if(response["status"] == 200){
                localStorage.setItem("username",response["username"]);
                localStorage.setItem("userid",response["user_id"]);
                localStorage.setItem("token",response["token"]);
                localStorage.setItem("name",response["first_name"]);
                // createJwtToken(1200,email);
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
    var confpassword = document.registration.confpassword.value;
    var contactNo = document.registration.contactNo.value;
    var country = document.registration.country.value;
    var city = document.registration.city.value;

    if(firstName != "" && lastName != "" && email != "" && confpassword !="" && password != "" && contactNo != "" && country != "" && city != ""){
      var emailValidationCheck = validateEmail(email);
      var passwordValidationCheck = validatePassword(password,confpassword);
      if(emailValidationCheck && passwordValidationCheck){

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
              console.log("response in registration--------",response);
              if(response["status"] == 201){
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
    
          // $.ajax(settings).fail(function (response) {
          //   swal({
          //     title: "Error",
          //     text: "Error occured",
          //     icon: "error",
          //   });
          // }); 
        }

      }
      else{
        if(passwordValidationCheck == false){
          swal({
            title: "Error",
            text: "Passwords don't match",
            icon: "error",
          });
        }
        else{
          swal({
            title: "Error",
            text: "Please provide a valid email",
            icon: "error",
          });
        }
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


function validatePassword(password,confpassword){
  if(password == confpassword){
    return true;
  }
  else
  return false;
}


function base64url(source) {
  // Encode in classical base64
  encodedSource = CryptoJS.enc.Base64.stringify(source);

  // Remove padding equal characters
  encodedSource = encodedSource.replace(/=+$/, '');

  // Replace characters according to base64url specifications
  encodedSource = encodedSource.replace(/\+/g, '-');
  encodedSource = encodedSource.replace(/\//g, '_');

  return encodedSource;
}

function createJwtToken(id,username){
  var header = {
    "alg": "HS256",
    "typ": "JWT"
  };
  
  var stringifiedHeader = CryptoJS.enc.Utf8.parse(JSON.stringify(header));
  var encodedHeader = base64url(stringifiedHeader);
  
  var data = {
    "id": id,
    "username": username
  };
  
  var stringifiedData = CryptoJS.enc.Utf8.parse(JSON.stringify(data));
  var encodedData = base64url(stringifiedData);
  
  var token = encodedHeader + "." + encodedData;
  var secret = "My very confidential secret!";

var signature = CryptoJS.HmacSHA256(token, secret);
signature = base64url(signature);

var signedToken = token + "." + signature;

window.localStorage.setItem("token", signedToken);
window.localStorage.setItem("username", username);
return signedToken;


}



