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
	,"pr":"Prototype"
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
	$('#userdata tbody').empty();
	$('#i-can-results').addClass('hidden');
	
	//Dont fetch data until user has chosen all options
	if(perSelect.localeCompare("null")!=0&&prcSelect.localeCompare("null")!=0&&conSelect.localeCompare("null")!=0){
		
		var tableData = '';
		
		// Load loader circle
		$("#loaderContainer").html("<div class=\"loader\" style=\"margin:auto;\"></div>");
		
		$.getJSON(theurl, function(data) {
		
			// get rid of loader once the info has been fetched
			$('#loaderContainer').html('');
			
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
				if( ( perSelect == per ) && ( prcSelect == prc ) && ( conSelect == con ) ){
							
					//if objects's matches ref then append the i-can statement to the table data
					if (f.Subconcept.localeCompare(ref)==0) {
						tableData += '<li>' + f.ICanStatement  + '</li>';
						
					//otherwise add a header + i-can statement
					} else {
//						console.log(f.Subconcept);
						
						if (tableData) {
							tableData +='</ul></td></tr>';
						}
						
						//grab full subconcept name from key:value pairs
						tableData += '<tr>' + '<th>' + subcons[f.Subconcept] + '</th>';
						tableData += '<td><ul><li>' + f.ICanStatement  + '</li>';
												
						//set the new reference
						ref=f.Subconcept;
					}

				}
			});
			
			tableData += '</ul></td></tr>';
			
			$('#userdata tbody').html(tableData);
			$('#userdata caption').html( 'I can statements: ' + options[perSelect] + 's ' + options[prcSelect] + ' ' + options[conSelect]);
			
			//unhide table
			$("#i-can-results").removeClass('hidden');
			
//			alert(tableData);
		});
		
	}
}

window.onload = function(){

	$('.dropdown a.box').click(function() {
		$(this).closest('.dropdown').toggleClass('active');
	});

	$(".prbtn").click(function(){
	
		//change main button name to selected option and change appearance
		$( '#practice' ).addClass( 'selected' ).children( '.box-content' ).html( $(this).html() );
		$( this ).closest('.dropdown').removeClass('active');
		
		//grab the first class of the selected dropdown option
		prcSelect = $(this).attr('data-value');

		//do this for every button for when user changes selection
		fetchStatement();
	});
	
	$(".conbtn").click(function(){
	
		//change button name to selected option
		$( '#concept' ).addClass( 'selected' ).children( '.box-content' ).html( $(this).html() );
		$( this ).closest('.dropdown').removeClass('active');
		
		//grab the first class of the selected dropdown option
		conSelect = $(this).attr('data-value');
		
		//do this for every button for when user changes selection
		fetchStatement();
	});
	
	$(".perbtn").click(function(){
	
		//change button name to selected option
		$( '#perspective' ).addClass( 'selected' ).children( '.box-content' ).html( $(this).html() );
		$( this ).closest('.dropdown').removeClass('active');
		
		//grab the first class of the selected dropdown option
		perSelect = $(this).attr('data-value');
		
		//do this for every button for when user changes selection
		fetchStatement();
	});
};