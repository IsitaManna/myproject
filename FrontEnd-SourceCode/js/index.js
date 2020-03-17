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