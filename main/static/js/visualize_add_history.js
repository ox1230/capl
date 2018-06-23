$(document).ready(function () {
    $("#history_category_inputBox").on('change keyup paste', function () { data_inputed() });
    $("#history_price_inputBox").on('keyup paste', function () { data_inputed() });
    $("#history_halbu_week_inputBox").on('change keyup paste', function () { data_inputed() });
    $("#history_written_date_inputBox").on('change keyup', function(){ data_inputed() });
   
    $("#graph").on("shown.bs.collapse", function () {
        // 그래프가 열렸을때
        setUp();
        setUpForAddHistory();
    });

});


var is_all_filled = function () {
    // add_history의 category, price , halbu가 모두 채워져 있으면 true, 아니면 false를 return한다.
    if ($("#history_category_inputBox").val() == "") return false;
    else if ($("#history_price_inputBox").val() == "" || $("#history_price_inputBox").val() == 0) return false;
    else if ($("#history_halbu_week_inputBox").val() == "" || $("#history_halbu_week_inputBox").val() < 2) return false;
    else return true;
}

var data_inputed = function () {
    if (is_all_filled() ) {   // 모든 칸이 차있고, 
        if ($("#graph").hasClass("in")) redrawForAddHistory();  //그래프div가 열려있다면
        else $("#graph-down-button").trigger("click"); // 그래프 div가 닫혀 있다면
    }

}

var setUp = function () {
    // 처음 그래프가 열렸을 때의 셋업

    $("#graph-canvas").empty(); // 캔버스를 깨끗하게 한다.
    // 캔버스를 세팅한다.
    svg = d3.select("#graph-canvas");
    W = $("#graph-canvas").width();
    H = $("#graph-canvas").height();
    margin = { top: 30, left: 30, right: 0, bottom: 30 };

}

var getDataFromForm = function(){
    written_date = new Date($("#history_written_date_inputBox").val());
    cate = $("option[value='" + $("#history_category_inputBox").val() + "']").text();
    price = parseInt($("#history_price_inputBox").val());
    halbu_week = parseInt($("#history_halbu_week_inputBox").val());  // 실제 할부 주 
    
    assigned = cate_infos[cate][0];

    //diff_week와 graph_week구하기
    var today = new Date();
    written_date.setDate(written_date.getDate() - written_date.getDay());  //입력주의 첫째날
    today.setDate(today.getDate() - today.getDay());
    diff_week = Math.ceil((written_date.getTime() - today.getTime())/(1000*3600*24*7));  
     //현재 주와 입력 주의 주 차이  (입력주가 빠르면 -,  현재주가 빠르면 +)      getTime(): 기준시점기준 지난밀리초 return 

    graph_week = halbu_week + diff_week;   // 그래프에 표시되는 (할부가 끝나는 주의 수)


    //resids 변경하기  // resid에서 price/halbu_week만큼빼기
    resids = []
    if (graph_week > 19) graph_week = 20;
    // 일단 받아온 값을 채워 넣는다.
    for (i = 0; i < graph_week + 3; i++) {
        if ( i >= 20) break;
        resids.push(cate_infos[cate][1][i]);
    }

    for(i = diff_week; i< graph_week; i++){
        if(i >= 20) break;
        if(i < 0) continue;

        resids[i] -= price/halbu_week;
    }
}

var setUpForAddHistory = function () {
    // 처음 그래프가 열렸을 떄

    if (!is_all_filled()) {
        // 데이터가 다 없을 때
        svg.append("text")
            .text("이 그래프는 나만의 할부를 위한 그래프 입니다.\n분류, 가격, 나만의 할부 칸을 모두 채워주세요\n(나만의 할부를 2주 이상으로 설정해주세요) ")
            .attr("text-anchor", "middle")
            .attr("x", W / 2 + margin.left - margin.right)
            .attr("y", 20)
            ;
    }
    else {
        //add_history를 위한 셋업
       
        getDataFromForm();

        // 제목 추가
        title = svg.append("text")
            .text(cate + "의 주별 남은 돈")
            .attr("text-anchor", "middle")
            .attr("x", W / 2 + margin.left - margin.right)
            .attr("y", 15)
            ;
        //scale 만들기
        // scale생성
        xScale = d3.scaleBand()
            .domain(
                graph_week > 17 ? d3.range(20) : d3.range(graph_week + 3)
            )
            .rangeRound([margin.left, W - margin.right]);

        //날짜 스케일이 필요하다!!
        var today = new Date();
        today.setDate(today.getDate() - today.getDay());
        startDates = ["this\nweek"];

        for (i = 1; i < graph_week + 3; i++) {
            if ( i >= 20) break;
            var forStringDate = new Date();
            forStringDate.setDate(today.getDate() + (7 * i));
            str = "";

            if (forStringDate.getMonth() + 1 < 10) str += "0";
            str += forStringDate.getMonth() + 1;
            str += "/";
            if (forStringDate.getDate() < 10) str += "0";
            str += forStringDate.getDate();
            str += "~";

            startDates.push(str);
        }

        xAxisScale = d3.scaleBand()
            .domain(startDates)
            .rangeRound([margin.left, W - margin.right]);


        yScale = d3.scaleLinear()
            .domain([d3.min(resids) - 2000, assigned * 1.1])
            .range([H - margin.bottom, margin.top]);

        //축만들기
        xAxis = d3.axisBottom();
        xAxis.scale(xAxisScale)
            // .ticks(5)
            ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.

        yAxis = d3.axisLeft();
        yAxis.scale(yScale)
            //  .ticks(5)
            ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.

        xAxisLine = svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + (H - margin.bottom) + ")")
            .call(xAxis);

        yAxisLine = svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + margin.left + ",0)")
            .call(yAxis);

        //assigned-line 만들기
        svg.append("line")
            .attr("x1", margin.left)
            .attr("x2", W - margin.right)
            .attr("y1", yScale(assigned))
            .attr("y2", yScale(assigned))
            .attr("class", "assigned-line")
        ;
        // line function ( line용 data만들기)
        lineFunction = d3.line()
            .curve(d3.curveStepAfter)
            .x(function (d, i) {
                return xScale(i);
            })
            .y(function (d, i) {
                return yScale(d);
            })
            ;

        // //path 만들기
        // pathLine = svg.append("path")
        //     .data([resids])
        //     .attr("class", "cate-resid")
        //     .attr("d", lineFunction)
        //     ;
        // path가 짧다 ㅠㅠ 늘려주자.

        svg.selectAll(".cate-horizontal-resid")
            .data(resids)
            .enter()
            .append("line")
            .attr("class", "cate-resid cate-horizontal-resid")
            .attr("x1", function(d,i){
                return xScale(i);
            })
            .attr("y1", function(d,i){
                return yScale(d)
            })
            .attr("x2", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                return yScale(d)
            })
        ;
        
        svg.selectAll(".cate-vertical-resid")
            .data(resids)
            .enter()
            .append("line")
            .attr("class", "cate-resid cate-vertical-resid")
            .attr("x1", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y1", function(d,i){
                return yScale(d);
            })
            .attr("x2", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                if (i < resids.length-1 ) return yScale(resids[i+1]);
                else return  yScale(d);     // 마지막 데이터는 세로선을 그릴 필요가 없다.
            })
        ;


        //포인트표시
        svg.selectAll("circle")
            .data(resids)
            .enter()
            .append("circle")
            .attr("class", "cate-resid-point")
            .attr("r", 3)
            .attr("cx", function (d, i) {
                return xScale(i) + xScale.bandwidth() / 2;    //우로 차이만큼 이동
            })
            .attr("cy", function (d, i) {
                return yScale(d);
            })
            ;


        //금액표시
        svg.selectAll(".cate-resid-text")
            .data(resids)
            .enter()
            .append("text")
            .attr("class", "cate-resid-text")
            .text(function (d) {
                return Math.round(d);
            })
            .attr("text-anchor", "middle")
            .attr("x", function (d, i) {
                return xScale(i) + xScale.bandwidth() / 2;    //우로 차이만큼 이동
            })
            .attr("y", function (d, i) {
                return yScale(d) + 15;
            })
            ;
    }
}

var redrawForAddHistory = function () {
    if (!is_all_filled() || $("line").length == 0) {
        // 데이터가 다 없거나, 그래프가 그려지지 않았을떄
        setUp();
        setUpForAddHistory();
    }

    else {
        var DURATION_TIME = 500;
        
        getDataFromForm();

        title.text(cate + "의 주별 남은 돈");

        //xAxisScale 다시 만들기
        var today = new Date();
        today.setDate(today.getDate() - today.getDay());
        startDates = ["this\nweek"];

        for (var i = 1; i < graph_week + 3; i++) {
            if ( i >= 20) break;
            var forStringDate = new Date();
            forStringDate.setDate(today.getDate() + (7 * i));
            var str = "";

            if (forStringDate.getMonth() + 1 < 10) str += "0";
            str += forStringDate.getMonth() + 1;
            str += "/";
            if (forStringDate.getDate() < 10) str += "0";
            str += forStringDate.getDate();
            str += "~";

            startDates.push(str);
        }

     
        //scale 변경하기
        xAxisScale.domain(
            startDates
        );
        xScale.domain(
            graph_week > 17 ? d3.range(20) : d3.range(graph_week + 3)
        );
        yScale.domain(
            [d3.min(resids) - 2000, assigned * 1.1]
        );

        //축변경하기
        xAxis.scale(xAxisScale)
            //.ticks(5)
            ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.
        yAxis.scale(yScale)
            //    .ticks(5)
            ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.
        
        xAxisLine.transition()
            .duration(DURATION_TIME)
            .call(xAxis);
        ;
        yAxisLine.transition()
            .duration(DURATION_TIME)
            .call(yAxis);

        //assigned-line 변경하기
        svg.select(".assigned-line")
            .transition()
            .duration(DURATION_TIME)
            .attr("x2", W - margin.right)
            .attr("y1", yScale(assigned))
            .attr("y2", yScale(assigned))
        ;

        // 그래프 변경하기 
        horizontalLine = svg.selectAll(".cate-horizontal-resid");

        horizontalLine.data(resids)
            .exit()
            .transition()
            .duration(DURATION_TIME)
            .attr("x1", W)
            .attr("x2", W + xScale.bandwidth() )
            .remove()
        ;

        horizontalLine.data(resids)
            .enter()
            .append("line")
            .attr("class", "cate-resid cate-horizontal-resid")
            .attr("x1", function(d,i){
                return W;
            })
            .attr("y1", function(d,i){
                return yScale(d)
            })
            .attr("x2", function(d,i){
                return  W + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                return yScale(d)
            })
            .merge(horizontalLine)
            .transition()
            .duration(DURATION_TIME)
            .attr("x1", function(d,i){
                return xScale(i);
            })
            .attr("y1", function(d,i){
                return yScale(d)
            })
            .attr("x2", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                return yScale(d)
            })
        ;
         
        verticalLine = svg.selectAll(".cate-vertical-resid");

        verticalLine.data(resids)
            .exit()
            .transition()
            .duration(DURATION_TIME)
            .attr("x1", W+ xScale.bandwidth())
            .attr("x2", W+ xScale.bandwidth())
            .remove()
        ;

        verticalLine.data(resids)
            .enter()
            .append("line")
            .attr("class", "cate-resid cate-vertical-resid")
            .attr("x1", function(d,i){
                return W + xScale.bandwidth();
            })
            .attr("y1", function(d,i){
                return yScale(d);
            })
            .attr("x2", function(d,i){
                return W + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                if (i < resids.length-1 ) return yScale(resids[i+1]);
                else return  yScale(d);     // 마지막 데이터는 세로선을 그릴 필요가 없다.
            })
            .merge(verticalLine)
            .transition()
            .duration(DURATION_TIME)
            .attr("x1", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y1", function(d,i){
                return yScale(d);
            })
            .attr("x2", function(d,i){
                return xScale(i) + xScale.bandwidth();
            })
            .attr("y2", function(d,i){
                if (i < resids.length-1 ) return yScale(resids[i+1]);
                else return  yScale(d);     // 마지막 데이터는 세로선을 그릴 필요가 없다.
            })
        ;
            

        // 포인트 변경
        circles = svg.selectAll(".cate-resid-point");

        circles.data(resids)
            .exit()
            .transition()
            .duration(DURATION_TIME)
            .attr("cx", W+ xScale.bandwidth()/2)
            .remove()
            ;

        circles.data(resids)
            .enter()
            .append("circle")
            .attr("class", "cate-resid-point")
            .attr("r", 3)
            .attr("cx", function (d, i) {
                return W + xScale.bandwidth() / 2;    //밖에서 등장
            })
            .attr("cy", function (d, i) {
                return yScale(d);
            })
            .merge(circles)    // enter + update objects
            .transition()
            .duration(DURATION_TIME)

            .attr("cx", function (d, i) {
                return xScale(i) + xScale.bandwidth() / 2;    //우로 차이만큼 이동
            })
            .attr("cy", function (d, i) {
                return yScale(d);
            })
        ;
        //텍스트 변경

        texts = svg.selectAll(".cate-resid-text");

        texts.data(resids)
            .exit()
            .remove()
            .transition()
            .duration(DURATION_TIME)
            .attr("cx", W+ xScale.bandwidth()/2)
            .remove()
        ;

        texts.data(resids)
            .enter()
            .append("text")
            .attr("class", "cate-resid-text")
            .text(function (d) {
                return Math.round(d);
            })
            .attr("text-anchor", "middle")
            .attr("x", function (d, i) {
                return W + xScale.bandwidth() / 2;    //밖에서 등장
            })
            .attr("y", function (d, i) {
                return yScale(d) - 5;
            })
            .merge(texts)
            .transition()
            .duration(DURATION_TIME)
            .text(function (d) {
                return Math.round(d);
            })
            .attr("x", function (d, i) {
                return xScale(i) + xScale.bandwidth() / 2;    //우로 차이만큼 이동
            })
            .attr("y", function (d, i) {
                return yScale(d) + 15;
            })
            ;
    }
}