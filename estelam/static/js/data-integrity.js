
// Empty Error

function isEmpty (id){
    
var userinput = $("#"+id).val();
// var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i ;
var div = $("#"+id).closest("div");

// if( (!pattern.test(userinput)) ){
if( userinput=="" || userinput==null ) {
    
    div.addClass("has-error");
    $("#"+id).addClass("error");
    $("#"+id).attr("data-content",'وارد نمایید');
    $("#"+id).popover('show');
    return false;

}
   
    div.removeClass("has-error");
    $("#"+id).removeClass("error");
    $("#"+id).popover('hide');
    return true;

}

// Email invalid
function email_invalid(id){

var userinput = $("#"+id).val();
var pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i ;
var div = $("#"+id).closest("div");

if( (!pattern.test(userinput)) ){
	
    div.addClass("has-error");
    $("#"+id).addClass("error");

    $("#"+id).attr("data-content",'ایمیل صحیح وارد نشده است');
    $("#"+id).popover('show');
    return false;

}
   
    div.removeClass("has-error");
    $("#"+id).removeClass("error");
    $("#"+id).popover('hide');
    return true;

}


// Password 
function pass_invalid(id){
    
    var val = $("#"+id).val();
    var pattern = /^\b[A-Z0-9]{5,}.+\b$/i;
    var div = $("#"+id).closest("div");

    if(!pattern.test(val)){
        div.addClass("has-error");
        $("#"+id).addClass("error");
        $("#"+id).attr("data-content",'رمز عبور را وارد نمایید');
        // $("#"+id).attr("data-placement",'left');
        $("#"+id).popover('show');
        return false;
    }

        div.removeClass("has-error");
        $("#"+id).removeClass("error");
        $("#"+id).popover('hide');
        return true;        
}


// Date
function date_invalid(id){
    var val = $("#"+id).val();
    var pattern = /^\b[A-Z0-9]{5,}.+\b$/i;
    var div = $("#"+id).closest("div");

    if(!pattern.test(val)){
        div.addClass("has-error");
        $("#"+id).addClass("error");
        $("#"+id).attr("data-content",'تارخ صحیح نیست');
        // $("#"+id).attr("data-placement",'left');
        $("#"+id).popover('show');
        return false;
    }
        div.removeClass("has-error");
        $("#"+id).removeClass("error");
        $("#"+id).popover('hide');
        return true;           
}


// Fax

function fax_invalid(id){
    var val = $("#"+id).val();
    var pattern = /^\b[0-9].+\b$/i;
    var div = $("#"+id).closest("div");

    if(!pattern.test(val)){
        div.addClass("has-error");
        $("#"+id).addClass("error");
        $("#"+id).attr("data-content",'تارخ صحیح نیست');
        $("#"+id).popover('show');
        return false;
    }
        div.removeClass("has-error");
        $("#"+id).removeClass("error");
        $("#"+id).popover('hide');
        return true;       
}


// Phone

function phone_invalid(id){
    var val = $("#"+id).val();
    var pattern = /^\b[0-9].+\b$/i;
    var div = $("#"+id).closest("div");

    if(!pattern.test(val)){
        div.addClass("has-error");
        $("#"+id).addClass("error");
        $("#"+id).attr("data-content",'تارخ صحیح نیست');
        $("#"+id).popover('show');
        return false;
    }
        div.removeClass("has-error");
        $("#"+id).removeClass("error");
        $("#"+id).popover('hide');
        return true;       
}


// Mobile

function mobile_invalid(id){
    var val = $("#"+id).val();
    var pattern = /^\b[0][9][0-9]{11}.+\b$/i;
    var div = $("#"+id).closest("div");

    if(!pattern.test(val)){
        div.addClass("has-error");
        $("#"+id).addClass("error");
        $("#"+id).attr("data-content",'تارخ صحیح نیست');
        $("#"+id).popover('show');
        return false;
    }
        div.removeClass("has-error");
        $("#"+id).removeClass("error");
        $("#"+id).popover('hide');
        return true;       
}