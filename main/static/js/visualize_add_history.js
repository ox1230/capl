$(document).ready(function () {
    $("#history_category_inputBox").on('change keyup paste', function () { data_inputed() });
    $("#history_price_inputBox").on('keyup paste', function () { data_inputed() });
    $("#history_halbu_week_inputBox").on('change keyup paste', function () { data_inputed() });

    $("#graph").on("shown.bs.collapse", function () {
        // 그래프가 열렸을때
        setUp();
        setUpForAddHistory();
    });

});


var is_all_filled = function () {
    // add_history의 category, price , halbu가 모두 채워져 있으면 true, 아니면 false를 return한다.
    if ($("#history_category_inputBox").val() == "") return false;
    else if ($("#history_price_inputBox").val() == "") return false;
    else if ($("#history_halbu_week_inputBox").val() == "") return false;
    else return true;
}

var data_inputed = function () {
    if (is_all_filled() && !$("#graph").hasClass("in")) {   // 모든 칸이 차있고, 그래프div가 열려있지 않다면
        $("#graph-down-button").trigger("click");
    }
}

var setUp = function () {
    // 처음 그래프가 열렸을 때의 셋업

    $("#graph-canvas").empty(); // 캔버스를 깨끗하게 한다.
    // 캔버스를 세팅한다.
    svg = d3.select("#graph-canvas");
    W = $("#graph-canvas").width();
    H = $("#graph-canvas").height();
    margin = { top: 0, left: 30, right: 0, bottom: 30 };

}

var setUpForAddHistory = function () {
    // 처음 그래프가 열렸을 떄

    if (!is_all_filled()) {
        // 데이터가 다 없을 때
        svg.append("text")
            .text("이 그래프는 나만의 할부를 위한 그래프 입니다. 분류, 가격, 나만의 할부 칸을 모두 채워주세요 ")
            .attr("text-anchor", "middle")
            .attr("x", W / 2 + margin.left - margin.right)
            .attr("y", 20)
            ;
    }
    else {
        //add_history를 위한 셋업
        cate = $("option[value='"+ $("#history_category_inputBox").val() + "']").text();
        price = parseInt( $("#history_price_inputBox").val());
        halbu_week =parseInt($("#history_halbu_week_inputBox").val());
        
        assigned = cate_infos[cate][0];
     
        //resids 변경하기  // resid에서 price/halbu_week만큼빼기
        resids = []
        for(i=0; i< halbu_week; i++){
            resids.push( cate_infos[cate][1][i] - (price/halbu_week));
        }
        for(i=0; i <3 ; i++){
            if(halbu_week + i >= 20) break;
            resids.push(cate_infos[cate][1][i+halbu_week]);
        }

        // 제목 추가
        svg.append("text")
            .text(cate+ "의 주별 남은 돈")
            .attr("text-anchor", "middle")
            .attr("x", W / 2 + margin.left - margin.right)
            .attr("y", 20)
            ;
        //scale 만들기
        // scale생성
        xScale = d3.scaleBand()
            .domain(
                halbu_week > 17 ? d3.range(20) : d3.range(halbu_week+3)
            )
            .rangeRound([margin.left, W - margin.right]);
        
        // 날짜 스케일이 필요하다!!
        // nameScale = d3.scaleBand()
        //     .domain(cate_infos['category'])
        //     .rangeRound([margin.left, W - margin.right]);
        
        minResids = d3.min(resids);  // resids중 0보다 작은게 있으면 resid를 0에 맞춘다.
        yScale = d3.scaleLinear()
            .domain([minResids <0 ? minResids*1.2: 0 , assigned * 1.2])
            .range([H - margin.bottom, margin.top]);

        //축만들기
        xAxis = d3.axisBottom();
        xAxis.scale(xScale)
            .ticks(5);    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.

        yAxis = d3.axisLeft();
        yAxis.scale(yScale)
            .ticks(5);    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + (H - margin.bottom) + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + margin.left + ",0)")
            .call(yAxis);
        

        // line function ( line용 data만들기)
        lineFunction = d3.line()
                        .x(function(d,i){
                             return xScale(i); 
                        })
                        .y(function(d,i){
                             return yScale(d); 
                        })
        ;

        //path 만들기
        svg.append("path")
            .data([resids])
            .attr("class", "cate-resid")
            .attr("d", lineFunction)
           
        ;

        
        
    }
}

var redrawForAddHistory = function(){
    //데이터 다시 받기
    cate = $("option[value='"+ $("#history_category_inputBox").val() + "']").text();
    price = parseInt( $("#history_price_inputBox").val());
    halbu_week =parseInt($("#history_halbu_week_inputBox").val());
    
    assigned = cate_infos[cate][0];
 
    //resids 변경하기  // resid에서 price/halbu_week만큼빼기
    resids = []
    for(i=0; i< halbu_week; i++){
        resids.push( cate_infos[cate][1][i] - (price/halbu_week));
    }
    for(i=0; i <3 ; i++){
        if(halbu_week + i >= 20) break;
        resids.push(cate_infos[cate][1][i+halbu_week]);
    }

    // scale 변경하기.

    xScale.domain(
        halbu_week > 17 ? d3.range(20) : d3.range(halbu_week+3)
    ));
    minResids = d3.min(resids);  // resids중 0보다 작은게 있으면 resid를 0에 맞춘다.
    yScale.domain(
        [minResids <0 ? minResids*1.2: 0 , assigned * 1.2]
    );
      
    //축변경하기
    xAxis.scale(xScale)
    //.ticks(5)
    ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.
    yAxis.scale(yScale)
    //    .ticks(5)
    ;    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (H - margin.bottom) + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(" + margin.left + ",0)")
        .call(yAxis);



}