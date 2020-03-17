function showLifeStyleImageDetails(clickedImageId){
    $(".lifeStyleImage").remove();
    var clickedImageUrl = '../images/floor-plan/' + clickedImageId + ".png";
    var clickedImage = $('<img src="' + clickedImageUrl + '" alt="" style="width:80%; height:80%;" class="lifeStyleImage">');
    $("#lifestyleCarousel-Inner").append(clickedImage);
}

function showStyleImageDetails(clickedImageId){
    $(".styleImage").remove();
    var clickedImageUrl = '../images/floor-plan/' + clickedImageId + ".png";
    var clickedImage = $('<img src="' + clickedImageUrl + '" alt="" style="width:80%; height:80%;" class="styleImage">');
    $("#styleCarousel-Inner").append(clickedImage);
}