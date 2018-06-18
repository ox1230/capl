$("#graph").on("shown.bs.collapse",function(){
    setUp();
    setUpForMain();
});



function setUp(){
    $("#temp-text").remove();  // "추가중 글자를 지운다" 
    $("#graph-canvas").empty(); // 캔버스를 깨끗하게 한다.
    // 캔버스를 세팅한다.
    svg = d3.select("#graph-canvas");
    W = $("#graph-canvas").width();
    H = $("#graph-canvas").height();
    margin = {top:0, left:30, right:0, bottom: 30};
    bar_padding = 20;
    
};

function setUpForMain(){
    //main을 위한 셋업
    
    N = cate_infos['category'].length;
    bar_width = 0;
    //scale 만들기
        // scale생성
    xScale = d3.scaleBand()
            .domain(d3.range(N))
            .rangeRound([margin.left, W- margin.right]);

    nameScale = d3.scaleBand()
                .domain(cate_infos['category'])
                .rangeRound([margin.left, W- margin.right]);

    yScale = d3.scaleLinear()
            .domain([0,d3.max(cate_infos['assigned']) * 1.5 ])
            .range([H - margin.bottom ,margin.top]);

    bar_width = xScale.bandwidth()*0.6;
    //축만들기
    xAxis = d3.axisBottom();
    xAxis.scale(nameScale)
        .ticks(5);    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.
    
    yAxis = d3.axisLeft();
    yAxis.scale(yScale)
        .ticks(5);    //구분자를 5개로 지정  --- 권유값, 실제로는 딱떨어지게 알아서 조정된다.
    
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (H -margin.bottom) + ")")
        .call(xAxis);
    
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate("+margin.left+",0)")
        .call(yAxis);
    
    // sum 그래프
    //bar들 그리기
    svg.selectAll(".sum-rect")
        .data(cate_infos['sum'])
        .enter()
        .append("rect")
        .attr("class", "sum-rect")
        .attr("x", function(d,i){
            return xScale(i)+ (xScale.bandwidth()-bar_width)/2;
        })
        .attr("y", function(d){
            return yScale(d);
        })
        .attr("width", bar_width)
        .attr("height", function(d){
            return (H- margin.bottom - margin.top) - yScale(d);
        })
    ;

    

    // resid 그래프 
    //그래프 만들기    ( resid<0이면 덮어써야한다.)
    svg.selectAll(".resid-rect")
        .data(cate_infos['resid'])
        .enter()
        .append("rect")
        .attr("class", function(d){
            if(d<0) return "resid-rect resid-rect-danger"
            else return "resid-rect"
        })
        .attr("width", bar_width)
        .attr("height", function(d,i){
            if (d<0)   return  (H- margin.bottom - margin.top) - yScale(-d);
            else return (H- margin.bottom - margin.top) - yScale(d);
        })
        .attr("x", function(d,i){
            return xScale(i)+ (xScale.bandwidth()-bar_width)/2;
        })
        .attr("y", function(d,i){
            if(d<0) return yScale(cate_infos['sum'][i]);    // sum과 시작위치가 같다.
            else return yScale(cate_infos['sum'][i]) -((H- margin.bottom - margin.top) - yScale(d));   // sum시작위치 - 자신의 길이.
        })
        
    ;
    // assgined표시
    svg.selectAll("assigned-line")
        .data(cate_infos['assigned'])
        .enter()
        .append("line")
        .attr('stroke', 'black')
        .attr('stroke-width', 5)
        .attr("x1",function(d,i){
            return xScale(i) + (xScale.bandwidth()-bar_width)/2;
        })
        .attr("x2", function(d,i){
            return xScale(i) + (xScale.bandwidth()-bar_width)/2 + bar_width ;
        })
        .attr("y1",function(d){
            return yScale(d);
        })
        .attr("y2",function(d){
            return yScale(d);
        })
        
    ;

    //라벨 붙이기
    svg.selectAll("sum-text")
        .data(cate_infos['sum'])
        .enter()
        .append('text')
        .text(function(d){
            return d + "원";
        })
        .attr("class",'sum-text')
        .attr("x", function(d,i){
            return xScale(i) + xScale.bandwidth()/2;
        })
        .attr("y", function(d){
            return H-margin.bottom - 5;
        })
        .attr("text-anchor","middle")
        .attr("fill", "white")
    ;
    svg.selectAll("resid-text")
        .data(cate_infos['resid'])
        .enter()
        .append('text')
        .text(function(d){
            return d + "원";
        })
        .attr("class",'resid-text')
        .attr("x", function(d,i){
            return xScale(i) + xScale.bandwidth()/2;
        })
        .attr("y", function(d,i){
            if(d<0) return yScale(cate_infos['assigned'][i]) -13;
            else return yScale(cate_infos['assigned'][i]) +13;   
        })
        .attr("text-anchor","middle")
        .attr("fill", "white")
    ;
}