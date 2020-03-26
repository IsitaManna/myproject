const apiBackendBaseUrl = "http://localhost:8000/recommendation-engine";
var num_of_questions=0;
window.onload = function() {
    var url = apiBackendBaseUrl + "/fetch-question-responses";
    var data={};
    var settings = {
      "url": url,
      "method": "GET",
      "headers": {
        "Content-Type": "application/json"
      },
      "data": JSON.stringify(data),
    };
    $.ajax(settings).done(function (response) {
        console.log("response from Api ------",response,response.length) 
        num_of_questions=response.length;
        response.forEach(element => {
            

            // console.log(element.Question,element.answer);
            // document.getElementById("question").innerHTML = element.Question.question;
            // $('#question').attr('id',element.Question.QuesID).append(element.Question.question);
                var htmldivs='<label id="question-'+element.Question.QuesID+'"><b>'+element.Question.question+'</b></label><br>'
                var radio="";
                element.answer.forEach(answer => {
                radio+='<input type="radio" name="radio'+element.Question.QuesID+'" id="answer-'+answer.ResponseID+'" value="'+answer.response+'"><label for="'+answer.response+'">'+answer.response+'</label><br>'
                });
    
            $('#question').append(htmldivs);
            $('#question').append(radio+"<br>");


        });
      });
  };


function submitResponse(){
    var i=0;
    var response=[];
    for(i=1;i<=num_of_questions;i++){
        var radioValue = $("input[name='radio"+i+"']:checked").attr("id");
        if(radioValue == undefined){
            swal({
                title: "Error",
                text: "Please answer all Questions",
                icon: "error",
              });
            
        }
        else{
        var respId=radioValue.split("-")[1];
        response.push({QuesID : i, ResponseID : respId});
        }

    }
    
    console.log("Form Response is---------- ",response);

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
