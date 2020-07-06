apiBackendBaseUrl=environments.apiBackendBaseUrl;
imageBaseUrl=environments.imageBaseUrl;

var num_of_questions=0;
window.onload = function() {
    addScrollEvent();
    // createStyleTab()

    // ------- Qualitative and Quantitative Tabs---------------
    var name = this.localStorage.getItem("name");
    if(name == null){
        name = "";
    }
    $(document).ready(function(){
        $("#username").html("Hi "+name);
    });
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
        questions=[]
        num_of_questions=response.length;
        var i=0;
        response.forEach(element => {
            
            i++;
            questions[i]=element.Question.id;
            // console.log(element.Question.id);
            
        });
        // console.log(questions);
        response.forEach(element => {
            
            i++;
            
            console.log(element.Question.question_type);
           

                var htmldivs='<label id="question-'+element.Question.id+'"><b>'+element.Question.question+'</b></label><br>'
                var radio="";
                var i=0;
                element.Answer.forEach(answer => {

                    //---------checkings are kept for demo purpose as placeholders--------
                    //---------to be removed later-----------------
                    i++;
                    if(element.Question.id == 6){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+ element.Question.id +'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;<img src="../images/questions/image'+i+'.jpg" style="width:43%; height : 83%"> &nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;<img src="../images/questions/image'+i+'.jpg" style="width:43%; height : 83%"> &nbsp;'

                    }
                    else if(element.Question.id == 17){
                        //--------- checkings are kept for space issues in UI---------
                       if(answer.id == 86 ){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        
                       }
                       else if (answer.id == 88){
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                         
                       }
                       else{
                        if(answer.id == element.User_Response.answer_id)
                        radio+='<input type="radio" checked="checked" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
                        else
                        radio+='<input type="radio" name="radio'+element.Question.id+'" id="answer-'+answer.id+'" value="'+answer.answer+'">&nbsp;<label style="font-size: 14px;" for="'+answer.answer+'">'+answer.answer+'</label>'+
                        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="../images/house_style/image'+i+'.jpg" style="width:20%; height : 43%">&nbsp;&nbsp;&nbsp;&nbsp;'
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
                var imagediv=''
                // if(element.Question.id == 9){
                //     var imgUrl = imageBaseUrl + element.Question.image_path;
                //     imagediv='<img src="' + imgUrl + '" style="width:100%;">';
                //     // imagediv='<img src="../images/questions/fire.jpeg" style="width:100%;height:100%">'
                // }
                if (element.Question.id == 1){
                    var imgUrl = imageBaseUrl + element.Question.image_path;
                    imagediv='<img src="' + imgUrl + '" style="width:100%;">';
                }
               
                // else if(element.Question.id == 23){
                //     var imgUrl = imageBaseUrl + element.Question.image_path;
                //     imagediv='<img src="' + imgUrl + '" style="width:100%;">';
                // }
                // else if(element.Question.id == 11){
                //     var imgUrl = imageBaseUrl + element.Question.image_path;
                //     imagediv='<img src="' + imgUrl + '" style="width:100%;">';
                // }
                // else if(element.Question.id == 14){
                //     var imgUrl = imageBaseUrl + element.Question.image_path;
                //     imagediv='<img src="' + imgUrl + '" style="width:100%;">';
                // }
                if(element.Question.id == 6 || element.Question.id == 17){
                    var finalHtml='<div class="card" >'+
                '<div id="divid'+i+'" href="divid'+(i+1)+'" class="card-body" style="padding-bottom : 1px">'+
                    ' <div class="row">'+
                        '<div class="col-md-12 col-lg-12 col-sm-12 col-xs-12"> '+htmldivs+''+radio+'</div>'+
                    '</div>'+
                '</div>'+
                '</div><br>'
                }
                else{
                var finalHtml='<div class="card" >'+
                '<div id="divid'+i+'" href="divid'+(i+1)+'" class="card-body" style="padding-bottom : 1px">'+
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
        });

      });
      
  };

// -------Submitting response of qualitative and quantitative questionarre---------
function submitResponse(){
    var token = this.localStorage.getItem("token");
    
    var i=0;
    var responseList=[];
    var allResponseFilled=true;
    for(i=1;i<=num_of_questions;i++){
        qid=questions[i]
        var radioValue = $("input[name='radio"+qid+"']:checked").attr("id");

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
        responseList.push({QuesID : qid, ResponseID : respId});
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

              text: response["message"]+"!",
              icon: "success",
            }).then( function(){
                window.location.href = "plan-recommended.html";

                // createStyleTab();
                // $('#lifestyle').removeClass('active');
                // $('#Qualitativetab').removeClass('active');
                // $('#style').addClass('active show');
                // $('#Styletab').addClass('active');
                // $(this).scrollTop(0);
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
        window.location.href = "plan.html";
        // $("#planTab").append(spanTabText);
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
    '<b> Level 1 : Click on the Images to Select the Floor Plan Outer Structure</b>'+
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
            if(count>3){
                count=0;
                newrow=' <div class="row" style="margin-bottom: 2%;"> ';
                row=row+'</div>'+newrow;
                
            }
            var eachcolumn='<div class="col-md-4 col-lg-4 col-sm-4 col-xs-4" id="img'+element.id+'" onclick="getlevel2Images('+element.id+')">'+
            '<a href="#level2">'+
                '<img id="l1Image-'+element.id+'" src="'+imageBaseUrl+element.image_path+'" style="width: 100%; float : right;">'+
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
                        '<b> Level 2 : Click on the Images to Select the Bedroom Position for the Selected Floor Plan</b>'+
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
    console.log("selected---");
    
    $('.selected').removeClass('selected');
    $("#image-"+id).addClass('selected');
    $("#planButton").removeAttr('disabled');
}

function submitStyleChoice(){
    var element=$('.selected').attr("id");
    var id=element.split("-")[1];
    console.log("Submitted!!!",id);
    var url = apiBackendBaseUrl + "/bedroom-style";

    var data={id:id};
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
    
            // createJwtToken(1200,email);
            swal({
                title: "Success",
                text: response["message"],
                icon: "success"
              }).then( function(){
                    window.location.href = "plan.html";
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


