$(document).ready(function(){
    var weekDates = getWeekStartAndEndDate();

    setTextTo("#week_start_and_end_date", getTextFormat(weekDates[0], weekDates[1]) );
});

function getWeekStartAndEndDate(){
    var today = new Date(); //오늘 날짜 
    today.set

    var day = today.getDay(); // 일요일: 0 , 토요일: 6

    var startDate = new Date(today.toDateString());
    startDate.setDate(today.getDate() - today.getDay());

    var endDate = new Date(today.toDateString());
    endDate.setDate(startDate.getDate() + 6 );

    return [startDate, endDate];
};

function getTextFormat(startDate, endDate){
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wendsday','Thursday', 'Friday', 'Saturday'];
    var startStr = startDate.getFullYear() + "-" ;
    
    if(startDate.getMonth() < 10){
        startStr += "0";
    };
    
    startStr = startStr + (startDate.getMonth() +1 )  +"-"+ startDate.getDate() + " " + days[startDate.getDay()]; 


    var endStr = endDate.getFullYear() + "-" ;
    if(endDate.getMonth() < 10){
        endStr += "0";
    }
    endStr += (endDate.getMonth()+1) +"-"+ endDate.getDate() + " " + days[endDate.getDay()]; 

    return startStr + " ~ " + endStr;  
};

function setTextTo(id, string){
    $(id).html(string);
}



