$(document).ready(function(){
    $("#history_category_inputBox").on('change keyup paste', function(){data_inputed()});
    $("#history_price_inputBox").on('change keyup paste', function(){data_inputed()});
    $("#history_halbu_week_inputBox").on('change keyup paste', function(){data_inputed()});
});


var is_all_filled = function(){
    // add_history의 category, price , halbu가 모두 채워져 있으면 true, 아니면 false를 return한다.

    if ($("#history_category_inputBox").val() == "") return false;
    else if ($("#history_price_inputBox").val() == "") return false;
    else if ($("#history_halbu_week_inputBox").val() == "") return false;
    else return true;
}

var data_inputed = function(){
    if( is_all_filled()){
        console.log("나야!");
        $("#graph-down-button").trigger("click");
    }
}