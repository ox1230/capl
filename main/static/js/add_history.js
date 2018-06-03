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

    // 나만의 할부 설명을 위한 html추가
    var explain_title = "'나만의 할부를 적용하면 물건 값을 이번주에 모두 지불한게 아니라 여러 주에 걸쳐 지불한 것으로 처리할 수 있습니다.'";
    var  data_content = "'예를 들어 교통카드에 1만원을 충전해 4주간 사용한다면,\n나만의 할부 4주를 적용해 각 주에 교통비로 2500원을 사용했다고 할 수 있습니다.'";
    $("[for='history_halbu_week_inputBox']").append(
        '<span class="glyphicon glyphicon-question-sign" data-toggle="popover" data-placement="top" title =' +
         explain_title + 'data-content = ' + data_content +'></span>');
});