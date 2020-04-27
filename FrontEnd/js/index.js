const apiBackendBaseUrl = "http://f12a4c33.ngrok.io/recommendation-engine";
var num_of_questions=0;
window.onload = function() {
    var name = this.localStorage.getItem("name");

    $(document).ready(function(){
          $("#username").html("Hi "+name);
      });
    // var url = apiBackendBaseUrl + "/fetch-question-responses";
    var url = apiBackendBaseUrl + "/question-response";

    var data={};
    var token = this.localStorage.getItem("token");
    var settings = {
      "url": url,
      "method": "GET",
      "headers": {
        "Content-Type": "application/json",
        "Authorization" : token
          },
      "data": JSON.stringify(data),
    };
    $.ajax(settings).done(function (response) {
        console.log("response from Api ------",response,response.length) ;
        num_of_questions=response.length;
        response.forEach(element => {
           

            console.log(element.Question.question_type);
            // document.getElementById("question").innerHTML = element.Question.question;
            // $('#question').attr('id',element.Question.id).append(element.Question.question);
            // var div="<div class='card'><div class='card-body'>";
                var htmldivs='<label id="question-'+element.Question.id+'"><b>'+element.Question.question+'</b></label><br>'
                var radio="";
                var i=0;
                element.Answer.forEach(answer => {
                    //---------checkings are kept for demo purpose as placeholders--------
                    //---------to be removed later-----------------
                    i++;
                    if(element.Question.id == 6){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;<img src="../images/questions/image'+i+'.jpg" alt="Chicago" style="width:43%; height : 83%"> &nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;<img src="../images/questions/image'+i+'.jpg" alt="Chicago" style="width:43%; height : 83%"> &nbsp;'


                    }
                    else if(element.Question.id == 17){
                        //--------- checkings are kept for space issues in UI---------
                       if(answer.id == 86 ){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        
                       }
                       else if (answer.id == 88){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                         
                       }
                       else{
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" alt="Chicago" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                       }
                       if ( i==3 ){
                            radio+="<br><br>"
                        }

                    }
                    else{
                    if(answer.id == element.User_Response.answer_id)
                    radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label><br>'
                    else 
                    radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label><br>'

                    }
                });
                //-----------checkings to add demo images manually-------
                //to be removed later
                var imagediv=''
                if(element.Question.id == 9){
                    imagediv='<img src="../images/questions/fire.jpeg" alt="Chicago" style="width:100%;height:100%">'
                }
                else if (element.Question.id == 1){
                    var imagediv='<img src="../images/image1.jpg" alt="Chicago" style="width:100%;">'

                }
               
                else if(element.Question.id == 23){
                    imagediv='<img src="../images/questions/roof.jpeg" alt="Chicago" style="width:100%;height:100%">'

                }
                else if(element.Question.id == 11){
                    imagediv='<img src="../images/questions/office.jpg" alt="Chicago" style="width:100%;height:100%">'

                }
                else if(element.Question.id == 14){
                    imagediv='<img src="../images/questions/sunroom.webp" alt="Chicago" style="width:100%;height:100%">'

                }
                if(element.Question.id == 6 || element.Question.id == 17){
                    var finalHtml='<div class="card" >'+
                '<div class="card-body" style="padding-bottom : 1px">'+
                    ' <div class="row">'+
                        '<div class="col-md-12 col-lg-12 col-sm-12 col-xs-12"> '+htmldivs+''+radio+'</div>'+
                    '</div>'+
                '</div>'+
                '</div><br>'
                }
                else{
                var finalHtml='<div class="card" >'+
                '<div class="card-body" style="padding-bottom : 1px">'+
                    ' <div class="row">'+
                        '<div class="col-md-6 col-lg-6 col-sm-12 col-xs-12"> '+htmldivs+''+radio+'</div>'+
                        '<div class="col-md-6 col-lg-6 col-sm-12 col-xs-12">'+imagediv+'</div>'+
                    '</div>'+
                '</div>'+
                '</div><br>'
                }
            // $('#question').append(div);
            if (element.Question.question_type == "Quantitative"){
                // if(element.Question.id == 8){
                   
                //     var finaldiv='<div class="card" >'+
                //     '<div class="card-body" style="padding-bottom : 1px">'+
                //         ' <div class="row">'+
                //             '<div class="col-md-6 col-lg-6 col-sm-12 col-xs-12"> '+htmldivs+
                //             ''
                //             '</div>'+
                //             '<div class="col-md-6 col-lg-6 col-sm-12 col-xs-12">'+imagediv+'</div>'+
                //         '</div>'+
                //     '</div>'+
                //     '</div><br>'
                // }
            $('#question').append(finalHtml);}
            else {
            $('#qualitative').append(finalHtml);
            }
            // $('#question').append('<img src="../images/image1.jpg" alt="Chicago" style="width:100%;">');
            // $('#question').append(radio+"<br></div></div>");


        });
      });
  };


function submitResponse(){
    var token = this.localStorage.getItem("token");

    var i=0;
    var responseList=[];
    var allResponseFilled=true;
    for(i=1;i<=num_of_questions;i++){
        var radioValue = $("input[name='radio"+i+"']:checked").attr("id");
        if(radioValue == undefined){
            allResponseFilled=false;
            swal({
                title: "Error",
                text: "Please answer all Questions",
                icon: "error",
              });
            
        }
        else{
        var respId=radioValue.split("-")[1];
        responseList.push({QuesID : i, ResponseID : respId});
        }

    }
    if(allResponseFilled){
    var url = apiBackendBaseUrl + "/create-customer-response";
    var responsedata={
        answers : responseList
    }
    var reqdata = {
        "url": url,
        "method": "POST",
        "headers": {
          "Content-Type": "application/json",
          "Authorization" : token

            },
        "data": JSON.stringify(responsedata),
      };
      console.log(reqdata);
      $.ajax(reqdata).done(function (response) {
          if(response["status"] == 201){

            // createJwtToken(1200,email);
            swal({
              title: "Success",
              text: response["message"],
              icon: "success",
            });
        }
        else{
            swal({
              title: "Error",
              text: response["message"],
              icon: "error",
            });
          }
          
        });

    }

}

function displayTabContent(tabName)
{
    console.log("-------Tab Name-------",tabName);
    var spanTabText = '<span class="sr-only">(current)</span>';
    if(tabName == "homeTab"){
        $("#homeTab").append(spanTabText);
    }
    if(tabName == "planTab"){
        $("#planTab").append(spanTabText);
    }
}

function logout(){
    localStorage.clear();
    window.location.href = "login-registration.html";

}

function nextTab(){
    console.log("-------------next -------------")
    $('#Quantitativetab').removeClass('active');
    $('#size').removeClass('active');
    $('#lifestyle').addClass('active show');
    $('#Qualitativetab').addClass('active');
    $(this).scrollTop(0);

    
   


    
}
