const apiBackendBaseUrl = "http://65b09446.ngrok.io/recommendation-engine";
const imageBaseUrl = "http://65b09446.ngrok.io/media/";

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
    var url = apiBackendBaseUrl + "/similar-plan";

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
                        '<a href='+imageBaseUrl+element.img+' target="_blank" >'+
                            '<img title="click to open in new window" src='+imageBaseUrl+element.img+' alt="Chicago" style="width:300px; height:300px; float : right;">'+
                        '</a>'+
                        '</div>'+
                    '</div>'+
                    '<div class="row">'+
                       ' <div class ="col-xs-8">'+
                       '<select class="rate" id="example-'+element.id+'">'+
                      ' <option value="1">1</option>'+
                       '<option value="2">2</option>'+
                       '<option value="3">3</option>'+
                       '<option value="4">4</option>'+
                       '<option value="5">5</option>'+
                     '</select>'+
                        '</div>'+
                        '<div class ="col-xs-4">'+
                          '<a>'+
                          '<i title="Download Image" onclick=forceDownload("'+imageBaseUrl+element.img+'","'+element.img+'") class="fa fa-download" aria-hidden="true" style="font-size: 23px;float: right;color: blue;"></i>'+
                          '</a>'+
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
                }).then( function(){
                  window.location.href = "stylePage.html";
                 
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

function downloadFile(data, fileName, type="octet/stream") {
  // Create an invisible A element
  const a = document.createElement("a");
  a.style.display = "none";
  document.body.appendChild(a);

  // Set the HREF to a Blob representation of the data to be downloaded
  a.href = window.URL.createObjectURL(
    new Blob([data], { type })
  );

  // Use download attribute to set set desired file name
  a.setAttribute("download", fileName);

  // Trigger the download by simulating click
  a.click();

  // Cleanup
  window.URL.revokeObjectURL(a.href);
  document.body.removeChild(a);
}

function forceDownload(url,fileName){
  // var url="http://fc545a71.ngrok.io/media/floor_plans/199.jpg";
  console.log("url is",url);
  // var fileName="test"
  fileName=fileName.split("/")[1];
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.responseType = "blob";
  xhr.onload = function(){
      var urlCreator = window.URL || window.webkitURL;
      var imageUrl = urlCreator.createObjectURL(this.response);
      var tag = document.createElement('a');
      tag.href = imageUrl;
      tag.download = fileName;
      document.body.appendChild(tag);
      tag.click();
      document.body.removeChild(tag);
  }
  xhr.send();
}






 
    
        