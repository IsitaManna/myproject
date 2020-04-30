const apiBackendBaseUrl = "http://cf4e9916.ngrok.io/recommendation-engine";
const imageBaseUrl = "http://cf4e9916.ngrok.io/media/";

let imgid =[];

// $(document).ready(function(){

// $('#rating6 span').click(function(){
//     console.log("hiiiii");
//     alert($(this).attr('id'));
// })
// });
// document.addEventListener('DOMContentLoaded', function(){
//     submitRating();
//   });
window.onload = function() {
    console.log(typeof(imgid));

    var name = this.localStorage.getItem("name");

    $(document).ready(function(){
          $("#username").html("Hi "+name);
      });
    // var url = apiBackendBaseUrl + "/fetch-question-responses";
    var url = apiBackendBaseUrl + "/customer-response-recommendation";

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
    // console.log(settings);
    $.ajax(settings).done(function (response) {
       
        console.log("response from Api ------",response,response.length) ;
        var columns='<div class = "row">',count=0;
        response.recommendation.forEach(element => {
            var id=element.id
            imgid.push(id);
            console.log(imgid.length);
            count++;
            if(count>3){
                count =0;
                finalRow='<div class = "row" style="margin-top : 2%" >';
                columns=columns+'</div>'+finalRow;
            }
            var eachcolumn = '<div class="col-md-4 col-lg-4 col-sm-4 col-xs-4">'+
            '<div class="card" >'+
                '<div class="card-body" style="padding-bottom : 1px">'+
                    '<div class ="row">'+
                        '<div class="col-md-12 col-lg-12 col-sm-12 col-xs-12">'+
                            '<img src='+imageBaseUrl+element.img+' alt="Chicago" style="width:300px; height:300px; float : right;">'+
                        '</div>'+
                    '</div>'+
                    '<div class="row">'+
                       ' <div class ="col-xs-12">'+
                       '<select class="rate" id="example-'+element.id+'">'+
                      ' <option value="1">1</option>'+
                       '<option value="2">2</option>'+
                       '<option value="3">3</option>'+
                       '<option value="4">4</option>'+
                       '<option value="5">5</option>'+
                     '</select>'+
                        '</div>'+
                    '</div>'+
               ' </div>'+
            '</div>'+
        '</div>'
        columns=columns+eachcolumn;
          

        });
        var finalhtml=columns+"</div>"
        $('#planimg').append(finalhtml);
        addRating();

      });
     
  };


  function addRating(){
        imgid.forEach(element => {
                       $(function() {
                // $('#example-'+element+'').barrating('set', 0);
                $('#example-'+element+'').barrating({
                theme: 'fontawesome-stars',
                initialRating: null,
                allowEmpty: null
               
                });
            });
        });   
   
  }
  function submitRating(){
      let i=0;
      var ratingresponse=[],allResponseFilled=true;
    
    $.each($(".rate option:selected"), function(){            
        i++;
       let rate=$(this).val();
       let image_id_attr=$(this).parent().attr("id");
        let image_id=image_id_attr.split("-")[1];
       console.log("hiiii...",rate,image_id);
       ratingresponse.push({"id":i,"image_id" : image_id,"rating":rate});

    });

    if(allResponseFilled){
        var token = this.localStorage.getItem("token");

        var url = apiBackendBaseUrl + "/customer-rating";
        var responsedata={
            rating : ratingresponse
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
              console.log("response ---",response);
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

  function logout(){
    localStorage.clear();
    window.location.href = "login-registration.html";

}
function displayTabContent(tabName)
{
    console.log("-------Tab Name-------",tabName);
    var spanTabText = '<span class="sr-only">(current)</span>';
    if(tabName == "homeTab"){
        window.location.href = "index.html";
        // $("#homeTab").append(spanTabText);
    }
    if(tabName == "planTab"){
        // window.location.href = "plan.html";
        $("#planTab").append(spanTabText);
    }
}




 
    
        