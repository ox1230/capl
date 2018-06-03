$(document).ready(function(){
    //날짜 입력칸을 위한 html 변경
    var $forCalender = $('<div class="form-group"><div class="input-group date" id ="datepicker1"><span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div></div>');
    $("#history_written_date_inputBox").before($forCalender);
    $("#datepicker1").prepend($("#history_written_date_inputBox"));

    //날짜를 위한 datepicker추가
    $(function(){
        $('.input-group.date').datepicker({
            calendarWeeks: false,
            todayHighlight: true,
            autoclose: true,
            format: "yyyy-mm-dd",
            language: "kr"
        });
    });

    //나만의 할부에 있는 기본값제거
    $("#history_halbu_week_inputBox").removeAttr("value");

});