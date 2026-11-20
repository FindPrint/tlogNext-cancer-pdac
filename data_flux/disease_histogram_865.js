//
// disease_histogram.js
//

//Call this function to display the table and plot in the disease.html page.

//This un-named functionis automatically called when the submit button is clicked in the sample.html page.
$(function(){  
    $("#displayButton").click(function(){  
	var p_val=$("#platform").val(),
 	    d_val=$("#disease").val();
	if(p_val.length==0 || d_val.length==0){
		alert("Please select Disease type and Platform type to view the results.");
	}else{
		Display();
	}
    });
});

$(function(){  
    $("#startDownload").click(function(){  
	var p_val=$("#platform").val(),
 	    d_val=$("#disease").val();
	if(p_val.length==0 || d_val.length==0){
		alert("Please select Disease type and Platform type to download the results.");
	}else{
		startDownload();
       }
    });
});

function Display()
  {
	
	 //Note the html file calling this js file must be places in the same folder where the Tables folder is avaliable.
	 //Tables folder has multiple text files each constituting the scores of diseases per platform. These tables were generated using the parse.pl script. 	
	 var disease = document.getElementById('disease').value;
	 var platform = document.getElementById('platform').value;
	 //below the disease and platform variables must match the "values" assigned to each option in the drop down menus in the HTML page.
	 //The commented function calls below are for the missing data. In future if you want to implement more disease types then just follow the file 
	 //naming style and call the functions as below.
	 var filename="tables/"+disease+" "+platform+".txt";
	 var file=filename.replace(/ /g,"_");
		$.ajax({
			url:file,
			type:'HEAD',
				error: function()
				{
					//file not exists
					imageTag();
				},
				success: function()
				{
					//file exists
					genTable(file);
					histogram(disease,platform,file);
				}
		});
	} 

//
//Call imagTag function to to create a image tag in the html page to display missing data in case the data is missing or not avalible.
//The message is presented through the missing.png image. If you want to update the message being presented then please update the missing.png file.
//
function imageTag()
  {
	$("#disease_type").remove(); //removes pre-existing imgage tag. 
	$('#plot').empty();//empty the plot div to refresh the plot to default status
	$('#viz').empty();//empty the plot div to refresh the plot to default status
	$('#plot').append($('<img>', { 
		id  : "disease_type",
		src : "images/missing.png", 
		alt : "histogram for disease type", 
	}));
  }
  
function reScaling()
  {
	if( !!$("#hist:empty").length) {
		var disease = document.getElementById('disease').value;
		var platform = document.getElementById('platform').value;
		//below the disease and platform variables must match the "values" assigned to each option in the drop down menus in the HTML page.
		//In future if you want to implement more disease types then just follow the file 
		//naming style and call the functions as below.
	 
		 var filename="tables/"+disease+" "+platform+".txt";
		 var file=filename.replace(/ /g,"_");
		histogram(disease,platform,file);

	} 
  };

var resizeTimer;
$(window).resize(function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(reScaling, 100);
});
//  
//genTable functoin is called to create a table in viz division in the html page and popullate the table by reading the scores from the text file assigned to the function.
function genTable(file)
  {
        d3.text(file, function(datasetText) {
                document.getElementById("viz").innerHTML='';
                var header=["ID","Stromal_score","Immune_score","ESTIMATE_score"];
                var parsedCSV = d3.tsv.parse(datasetText);
                var sampleHTML = d3.select("#viz")
                        .append("table")
                        .attr("id","table_id")
                        .style("border-collapse", "collapse")
                        .style("border", "2px black solid");
                var thead=sampleHTML.append("thead"),
                    tbody=sampleHTML.append("tbody");

                thead.append("tr")
                     .selectAll("th")
                     .data(header)
                     .enter()
                     .append("th")
                     .style("border", "2px black solid")
                     .style("padding", "5px")
                     .text(function(h){return h;});

                var rows=tbody.selectAll("tr")
                        .data(parsedCSV)
                        .enter().append("tr");

                var cells= rows.selectAll("td")
                        .data(function(row){
                                return header.map(function(h){
                                        return {column: h, value: row[h]};
                                });
                        })
                        .enter().append("td")
                        .style("border", "1px black solid")
                        .style("padding", "5px")
                        .text(function(d){return d.value;})
                        .style("font-size", "12px");
                $('#table_id').dataTable();
                //alert(' ');
        });
}


//
//startDownload function is called when the end-user presses the Download button in the html page. 
function startDownload()
  {
	var disease = document.getElementById('disease').value;
	var platform = document.getElementById('platform').value;
	var filename="tables/"+disease+" "+platform+".txt";
	var url=filename.replace(/ /g,"_");
		$.ajax({
			url:url,
			type:'HEAD',
			error: function()
				{
					//file not exists
					imageTag();
				},
				success: function()
				{
					//file exists
					window.open(url,'Download');
				}
		});
  }
  
//
//histogram function is called to generate the histogram dynamically.
//improvements can be made to the plot, the bin size is assigned to make the plots appear good and it does not have any statistical significance.   
function histogram(disease,platform,table)
  {
	$("#disease_type").remove();
	$("#plot").empty();
	////created a temp div to keep check of the resize step and call only the histogram and not other functoins.
	$('#plot').append($('<div>', { 
		id  : "hist",
		class : "plot",
	}));

	/* Read TSV file: first row =>   Breast_cancer_Agilent_G4502A.txt:     ID,Stromal_score,Immune_score,ESTIMATE_score*/
	d3.tsv(table, function(data) { 
        var sampsize = data.length;
		var maxval = 0, minval = 10000;
		var array1 = new Array(),
			array2 = new Array(),
			array3 = new Array(); 
		////Assign each colum in the tsv file to individual array and assing the min and max values of the scores across the table.	
	    for (var i=0; i < sampsize; i++) {
			maxval = Math.max(maxval, parseFloat(data[i].Stromal_score), parseFloat(data[i].Immune_score), parseFloat(data[i].ESTIMATE_score) );
			minval = Math.min(minval, parseFloat(data[i].Stromal_score), parseFloat(data[i].Immune_score), parseFloat(data[i].ESTIMATE_score));
			array1.push(parseFloat(data[i].Stromal_score));
			array2.push(parseFloat(data[i].Immune_score));
			array3.push(parseFloat(data[i].ESTIMATE_score));
			//document.write('<p>' + label_array[i] +  '  ;  ' + parseFloat(data[i].month_return) + '</p>'); 
		}
	 	////Set the dimension of the plots.
		var w_px=$('#plot').css("width"),
			h_px=$('#plot').css("height");
		var h_set=h_px.substring(0,3);
		var w_set=w_px.substring(0,3);
		var margin = {top: (h_set*0.15), right: (w_set*0.05), bottom: (h_set*0.10), left: (w_set*0.10)},
			width = w_set - margin.left - margin.right,
			height = h_set - margin.top - margin.bottom;
		////Creat a SVG to display the graphics as plot.
		var svg = d3.select("#plot").append("svg")
				.attr("class", "histogram")
				.attr("id", "histogram_id")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		////Heading of the plot displaying the disease name and platform type. These values are passed to the function when it is called.	
			svg.append("svg:text")
				.attr("class","heading")
				.attr("x", width/4)
				.attr("y", (((height-(height*0.25))/3)-(height*0.4)))
				.text(disease +" - "+platform);
		////Lable for X-axis 
			svg.append("svg:text")
				.attr("class","heading")
				.attr("x", (width-(width*0.1))/2)
				.attr("y", height+(height*0.1))
				.text("Scores");
		////The bins are defined as below.
		var scalemax=Math.ceil(maxval),
			scalemin=Math.floor(minval),
			bin_n=30;
			//bin_n=(scalemax-scalemin)/200;
			//document.write(bin_n);
		//using d3 histogram function read the array
		var histogram1 = d3.layout.histogram()
					.range([minval, maxval])
					.bins(bin_n)
					.frequency("density")(array1);	
		var histogram2 = d3.layout.histogram()
					.range([minval, maxval])
					.bins(bin_n)
					.frequency("density")(array2);	
		var histogram3 = d3.layout.histogram()
					.range([minval, maxval])
					.bins(bin_n)
					.frequency("density")(array3);	
		//Set uniform height across all the histograms. 			
		var height_array1=d3.max(histogram1, function(d) { return d.y; }),
			height_array2=d3.max(histogram2, function(d) { return d.y; }),
			height_array3=d3.max(histogram3, function(d) { return d.y; });
		var max_height_y=d3.max([height_array1,height_array2,height_array3]); 
		////xaxis info just to make it look uniform, it is independent of the bin size.
		var z = d3.scale.linear()
			.domain([minval,maxval])
			.range([0, width]);
		
		////Scale for histogram 1
		var xScale = d3.scale.ordinal()
            .domain(histogram1.map(function(d) { return d.x; }))
            .rangeRoundBands([0, width]);
		var y = d3.scale.linear()
			.domain([0, max_height_y])
			.range([(height-(height*0.25))/3,0]);	
		
		////histogram 1
		svg.selectAll("rect")
			.data(histogram1)
			.enter()
			.append("rect")
			.attr("transform", function(d) { return "translate(" + 0 + "," + (y(d.y)+((height-(height*0.25))/3)-(2*(height*0.15))) + ")"; })
			.attr("y",  function(d) { return d.y; })
			.attr("x",  function(d) { return xScale(d.x); })
			.attr("width", Math.round(width/bin_n))
			.attr("height", 0)
			.transition()
			.duration(1200)
			.attr("y", 0)
			.attr("height", function(d) { return ((height-(height*0.25))/3)-y(d.y); });
			
		svg.append("svg:text")
			.attr("class","heading_sub")
			.attr("x", width-(width*0.20))
			.attr("y",(((height-(height*0.25))/3)-(height*0.30)))
			.text("Stromal");
			
		//////Scale for histogram 2
		var y2 = d3.scale.linear()
			.domain([0, max_height_y])
			.range([(height-(height*0.25))/3,0]);	
		////histogram 2
		var sub_hist = svg.selectAll("g.rule")
			.data(histogram2)
			.enter().append("svg:g")
			.attr("class", "rule");
						
		sub_hist.append("svg:rect")
			.attr("transform", function(d,i) { return "translate(" + 0 + "," + (y2(histogram2[i].y)+(2*((height-(height*0.25))/3))-(2*(height*0.10))) + ")"; })
			.attr("y",  function(d) { return d.y; })
			.attr("x",  function(d) { return xScale(d.x); })
			.attr("width", Math.round(width/bin_n))
			.attr("height", 0)
			.transition()
			.duration(1200)
			.attr("y", 0)
			.attr("height", function(d,i) { return ((((height)-(height*0.25))/3))-y2(histogram2[i].y); });
		
		svg.append("svg:text")
			.attr("class","heading_sub")
			.attr("x", width-(width*0.20))
			.attr("y", ((2*((height-(height*0.25))/3))-(height*0.20)))
			.text("Immune");
				
		//////Scale for histogram 3
		var y3 = d3.scale.linear()
			.domain([0, max_height_y])
			.range([(height-(height*0.25))/3,0])
		////histogram 3			
		var sub_hist = svg.selectAll("g.rule2")
			.data(histogram3)
			.enter().append("svg:g")
			.attr("class", "rule2");
						
		sub_hist.append("svg:rect")
			.attr("transform", function(d,i) { return "translate(" + 0 + "," + (y3(histogram3[i].y)+(3*(height-(height*0.25))/3)-(2*(height*0.05))) + ")"; })
			.attr("y",  function(d) { return d.y; })
			.attr("x",  function(d) { return xScale(d.x); })
			.attr("width", Math.round(width/bin_n))
			.attr("height", 0)
			.transition()
			.duration(1200)
			.attr("y", 0)
			.attr("height", function(d,i) { return ((height-(height*0.25))/3)-y3(histogram3[i].y); });
		
		svg.append("svg:text")
			.attr("class","heading_sub")
			.attr("x", width-(width*0.20))
			.attr("y", ((3*((height-(height*0.25))/3))-(2*(height*0.05))))
			.text("ESTIMATE");
		
		////svg for the azis of the plots	
		var xAxis = d3.svg.axis()
			.scale(z)
			.tickSize(6,0,0)
            .orient("bottom")




		var yAxis = d3.svg.axis()
			.scale(y)
			.ticks(5)
			.tickSize(6,0,2)
            .orient("left");
		var yAxis2 = d3.svg.axis()
			.scale(y2)
			.ticks(5)
			.tickSize(6,0,2)
            .orient("left");
		var yAxis3 = d3.svg.axis()
			.tickSize(6,0,2)
			.ticks(5)
			.scale(y3)
            .orient("left");
	
		var xaxisz=svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + ((height-(height*0.10))) + ")")
			.call(xAxis);
		//Tilt the x scale values at 45 degrees.
		xaxisz.selectAll("text")
			.attr("transform", function(d) {
				return "rotate(45)translate(" + this.getBBox().width/4 + "," +this.getBBox().height/10 + ")";
			});

		svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + (((height-(height*0.25))/3)-(2*(height*0.15))) + ")")
			.call(yAxis);
	
		svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + ((2*((height-(height*0.25))/3))-(2*(height*0.10))) + ")")
			.call(yAxis2);
	
		svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + ((height-(height*0.25))-(2*(height*0.05))) + ")")
			.call(yAxis3)
		//.attr("transform", "translate(0," + (70 + 3*(height-100)/3) + "),rotate(180) ")
	});

  }
  //get computed style of HTML element
function getStyle(el,styleProp)
 {
	var x = document.getElementById(el);
	var y = document.defaultView.getComputedStyle(x,null).getPropertyValue(styleProp);
	return y;
 }
