
apiBackendBaseUrl=environments.apiBackendBaseUrl;
imageBaseUrl=environments.imageBaseUrl;
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
            // ----two images in one row-------
            if(count>2){
                count =0;
                finalRow='<div class = "row" style="margin-top : 2%" >';
                columns=columns+'</div>'+finalRow;
            }
          // ------ dimensions-------------------
            var dimdiv="";
            element.dimension.forEach(dim => {
              console.log(dim);
              dimdiv=dimdiv+'<span><b>'+dim.room+' :</b> '+dim.area_perc
              +'% </span> <br> '
            });
            // -----------------------------------
            // --------each image column-----------
            var eachcolumn = '<div class="col-md-6 col-lg-6 col-sm-6 col-xs-6">'+
            '<div class="card" >'+
                '<div class="card-body" style="padding-bottom : 1px">'+
                    '<div class ="row">'+
                        '<div class="col-md-8 col-lg-8 col-sm-8 col-xs-8" id="download-area">'+
                        '<a href='+imageBaseUrl+element.img+' target="_blank" >'+
                        '<img title="click to open in new window" src='+imageBaseUrl+element.img+' alt="Chicago" style="width:300px; height:300px; float : right;">'+
                        '</a>'+
                        '</div>'+
                        '<div class ="col-xs-4" style="margin-top: 4%;">'+
                      '<span><b style="font-size : 16px">Dimesions :</b><br>'+dimdiv+
                      '</span>'+
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
                          '<a >'+
                          '<i onclick=forceDownload("'+imageBaseUrl+element.img+'","'+element.img+'") title="Download Image" class="fa fa-download" aria-hidden="true" style="font-size: 23px;float: right;color: blue;"></i>'+
                          '</a>'+
                        '</div>'+
                    '</div>'+
                    // '<div class="row">'+
                    //   ' <div class ="col-xs-12">'+
                    //   '<span><b>Dimesions :</b>'+dimdiv
                    //   +' </span>'
                    //   '</div>'+
                    // '</div>'+
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

function downloadPNGImage(linkElement) {
  var myDiv = document.getElementById('download-area');
  var myImage = myDiv.children[0];
  let downloadLink = myImage.src + "&format=jpg";
  linkElement.setAttribute('download', downloadLink);
  linkElement.href = downloadLink;
  linkElement.click();
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



 
    
        