apiBackendBaseUrl=environments.apiBackendBaseUrl;
imageBaseUrl=environments.imageBaseUrl;
var num_of_questions=0;
window.onload = function() {
    addScrollEvent();
    

    // ------- Qualitative and Quantitative Tabs---------------
    var name = this.localStorage.getItem("name");
    if(name == null){
        name = "";
        window.location.replace("login-registration.html");
    }
    $(document).ready(function(){
        $("#username").html("Hi "+name);
    });
    createStyleTab();
  };

// -------Submitting response of qualitative and quantitative questionarre---------

function displayTabContent(tabName)
{
    console.log("-------Tab Name-------",tabName);
    var spanTabText = '<span class="sr-only">(current)</span>';
    if(tabName == "homeTab"){
        window.location.href = "index.html";
    }
    if(tabName == "planTab"){
        window.location.href = "plan.html";
        // $("#planTab").append(spanTabText);
    }
}

function logout(){
    localStorage.clear();
    window.location.href = "login-registration.html";

}


function addScrollEvent(){
    $('a[href^="#"]').on('click', function(event) {

        var target = $(this.getAttribute('href'));
    
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top
            }, 1000);
        }
    
    });
}
function createStyleTab(){
    $('#styleLevel1').empty();
    $('#styleLevel2').empty();



    var firstRow = '<div class ="row" style="margin-bottom: 2%;">'+
    '<div id="level1" class="col-md-12 col-lg-12 col-sm-12 col-xs-12">'+
    '<h4 style="color : #6D7377;text-align: center;"> Select a basic shape for your home. This will help our AI engine be more efficient</h4>'+
    '</div>'+
    '</div>'
    $('#styleLevel1').append(firstRow);

    var url = apiBackendBaseUrl + "/plan-style";

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

        console.log("response for style tab ------",response,response.length) ;
        var row = ' <div class="row" style="margin-bottom: 2%;"> ';
        var count=0;
        response.forEach(element => {
            count++;
            if(count>12){
                count=1;
                newrow=' <div class="row" style="margin-bottom: 2%;"> ';
                row=row+'</div>'+newrow;
                
            }
            var eachcolumn='<div class="col-md-1 col-lg-1 col-sm-1 col-xs-1" id="img'+element.id+'"  onclick="selectImage('+element.id+')">'+
            '<a href="#level2">'+
                '<img id="l1Image-'+element.id+'" src="'+imageBaseUrl+element.image_path+'" style="width: 100%; height:70%; border:1px solid; float : right;">'+
            ' </a>'+
            '</div>'
            row=row+eachcolumn;
        });
        var finalhtml=row+"</div>";
        $('#styleLevel1').append(finalhtml);

    });
    

}

function getlevel2Images(imageId){
    $("#planButton").attr('disabled','disabled');
    $('.selectedImg').removeClass('selectedImg');
    $("#l1Image-"+imageId).addClass('selectedImg');
    $('#styleLevel2').empty();
    var firstRow='<div class ="row"  style="margin-bottom: 2%;">'+
                    '<div id= "level2" class="col-md-8 col-lg-8 col-sm-8 col-xs-8">' +
                        '<h4 style="color : #6D7377;"> Click on the Images to Select the Bedroom Position for the Selected Floor Plan</h4>'+
                    '</div>'+
                    '<div id= "level2" class="col-md-4 col-lg-4 col-sm-12 col-xs-12">' +
                        '<a href="#level1" style="float: right; font-size: 14px;" >'+
                            '<i class="fa fa-angle-double-up" aria-hidden="true"></i> Go back to Level 1</a>'+
                    '</div>'+
                '</div>'
    $('#styleLevel2').append(firstRow);

    var url = apiBackendBaseUrl + "/plan-style";

    var data={id:imageId};
    var token = this.localStorage.getItem("token");
    var settings = {
      "url": url,
      "method": "POST",
      "headers": {
        "Content-Type": "application/json",
        "Authorization" : token
          },
      "data": JSON.stringify(data),
    };
    $.ajax(settings).done(function (response) {
        console.log("response is------",response);
        var row = ' <div class="row" style="margin-bottom: 2%;"> ';
        var count=0;
        response.forEach(element => {
            count++;
            if(count>3){
                count=0;
                newrow=' <div class="row" style="margin-bottom: 2%;"> ';
                row=row+'</div>'+newrow;
                
            }
            var eachcolumn='<div class="col-md-4 col-lg-4 col-sm-4 col-xs-4" alt="" id="img'+element.id+'">'+
            '<a href="#planButton">'+
                '<img id="image-'+element.id+'" src="'+imageBaseUrl+element.image_path+'" style="height: 300px;width: 300px; float : right;" onclick="selectImage('+element.id+')">'+
            '</a>'+

            '</div>'
            row=row+eachcolumn;
        });
        var finalhtml=row+"</div>";
        $('#styleLevel2').append(finalhtml);
        // $('img').click(function(){
        //     console.log("selected---",this);
        //     $('.selected').removeClass('selected');
        //     $(this).addClass('selected');
        // });
    });

}
function selectImage(id){
    console.log("selected---",id);
    $('.selectedImg').removeClass('selectedImg');
    $("#l1Image-"+id).addClass('selectedImg');
    $("#planButton").removeAttr('disabled');

    // $('.selected').removeClass('selected');
    // $("#img-"+id).addClass('selected');
    // $("#planButton").removeAttr('disabled');
}

function submitStyleChoice(){
    var element=$('.selectedImg').attr("id");
    console.log("selected-->>",element);
    var id=element.split("-")[1];
    $('#overlay').fadeIn();
    console.log("Submitted!!!",id);
    var url = apiBackendBaseUrl + "/bedroom-style";

    var data={id:id};
    console.log("---",data);
    var token = this.localStorage.getItem("token");
    var settings = {
      "url": url,
      "method": "POST",
      "headers": {
        "Content-Type": "application/json",
        "Authorization" : token
          },
      "data": JSON.stringify(data),
    };
    $.ajax(settings).done(function (response) {
        console.log("response in submission---",response);
        if(response["status"] == 201){
            $('#overlay').fadeOut();

    
            // createJwtToken(1200,email);
            // swal({
            //     title: "Success",
            //     text: "Processed Successfully!",
            //     icon: "success"
            //   }).then( function(){
                    window.location.href = "plan.html";
            //   });
        }
        else{
            swal({
              title: "Error",
              text: "Processing Unsuccessful!",
              icon: "error",
            });
          }
    });
    

}

