var perSelect="null";
var prcSelect="null";
var conSelect="null";
var options={
	"e":"Explorer"
	,"c":"Creator"
	,"i":"Innovator"
	,"z":"Citizen"
	,"an":"Analyze"
	,"co":"Communicate"
	,"pr":"Practice"
	,"ab":"Abstraction"
	,"al":"Algorithms"
	,"p":"Programming"
	,"d":"Data"
	,"n":"Networks"
}
//subconcept definitions
//API INCORRECTLY REFERENCES DATA SUBCONCEPT sensor and datasets AS D.SS INSTEAD OF THE CORRECT D.SD
var subcons={
	"AB.D":"Decomposition"
	,"AB.PR":"Pattern Recognition"
	,"AB.GDR": "Generalization and Detail Removal"
	,"AB.M":"Modularity"
	,"AB.I":"Interfaces"
	,"AL.AD":"Algorithm Design"
	,"AL.CF":"Control Flow"
	,"AL.IVO":"Inputs,  Variables and Outputs"
	,"AL.A":"Application"
	,"P.L":"Languages"
	,"P.S":"Syntax"
	,"P.DE":"Development Environments"
	,"P.C":"Collaboration"
	,"D.SS":"Sensors and Datasets"
	,"D.DAS":"Data Abstraction and Storage"
	,"D.TV":"Transformation and Visualization"
	,"D.FLA":"Feedback Loops and Automation"
	,"N.T":"Trust"
	,"N.PRO":"Protocols"
	,"N.PI":"Physical Internet"
	,"N.M":"Markup"
};	
var	theurl="http://cs4all.nyc/api/ican";
function fetchStatement() {
	//Empty table before we append to it
	$("#userdata tbody").empty();
	//Dont fetch data until user has chosen all options
	if(perSelect.localeCompare("null")!=0&&prcSelect.localeCompare("null")!=0&&conSelect.localeCompare("null")!=0){
		// Load loader circle
		$("#loaderContainer").html("<div class=\"loader\" style=\"margin:auto;\"></div>");
		$.getJSON(theurl, function(data) {
			// get rid of loader once the info has been fetched
			$("#loaderContainer").html("<div></div>");
			//reference variable to see if a new subconcept header is needed
			var ref="";
			//loop through JSON, f==object
			$.each(data, function(i, f) {
				//format codification for each json object to compare to the selected options
				var per=f.Perspective;
				var con=f.Subconcept.slice(0,f.Subconcept.indexOf("."));
				var prc=f.Subpractice.slice(0,f.Subpractice.indexOf("."));
				per=per.toLowerCase();
				con=con.toLowerCase();
				prc=prc.toLowerCase();
				//if object matches Perspective, Practive and Concept
				if(perSelect.localeCompare(per)==0){
					if(prcSelect.localeCompare(prc)==0){
						if(conSelect.localeCompare(con)==0){
							$(".tblinfo").html("These are the I can statements for your selection of "+options[perSelect]+", "+options[prcSelect]+" and "+options[conSelect]);
							//unhide table
							$(".tblinfo").css("display","inline");
							//if objects's matches ref then append the ican statement to the table
							if(f.Subconcept.localeCompare(ref)==0){
								var tblRow = "<tr id=\"userdata\">" +"<td id=\"userdata\">" + f.ICanStatement  + "</td>" + "</tr>"
								$(tblRow).appendTo("#userdata tbody");
							//otherwise add a header and then ican statement
						} else { 
								console.log(f.Subconcept);
								//grab full subconcept name from key:value pairs
								var sectionHeader= "<tr id=\"userdata\" style=\"background-color:#F26922;color:white;\">" +"<td id=\"userdata\"style=\"color:white;\">"  + subcons[f.Subconcept] + "</td>" + "</tr>"
								var tblRow = "<tr id=\"userdata\">" +"<td id=\"userdata\">" + f.ICanStatement  + "</td>" + "</tr>"
								$(sectionHeader).appendTo("#userdata tbody");
								$(tblRow).appendTo("#userdata tbody");
								//set the new reference
								ref=f.Subconcept;
							}
						}
					}
				}
			});
		});
	}
}
window.onload = function(){
	$(".prbtn").click(function(){
			//change main button name to selected option
			document.getElementById("practice").innerHTML=($(this).html());
			//grab the first class of the selected dropdown option
			prcSelect=$(this).attr('class').split(' ')[0];
			//invert button apperance
			$(".practice").addClass("practiceinvert");
			$(".practice").removeClass("practice");
			//do this for every button for when user changes selection
			fetchStatement(); 
		});
	$(".conbtn").click(function(){
			//change button name to selected option
			document.getElementById("concept").innerHTML=($(this).html());
			//grab the first class of the selected dropdown option
			conSelect=$(this).attr('class').split(' ')[0];
			//invert button apperance
			$(".concept").addClass("conceptinvert");
			$(".concept").removeClass("concept");
			//do this for every button for when user changes selection
			fetchStatement();
		});
	$(".perbtn").click(function(){
			//change button name to selected option
			document.getElementById("perspective").innerHTML=($(this).html());
			//grab the first class of the selected dropdown option
			perSelect=$(this).attr('class').split(' ')[0];
			//invert button apperance
			$(".perspective").addClass("perspectiveinvert");
			$(".perspective").removeClass("perspective");
			//do this for every button for when user changes selection
			fetchStatement();
		});
	};