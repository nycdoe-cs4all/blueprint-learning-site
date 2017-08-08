var perSelect="null";
var prcSelect="null";
var conSelect="null";

function fetchStatement() {
	theurl="http://cs4all.nyc/api/ican";
	var people = [];
	$("#userdata tbody").empty();
	if(perSelect.localeCompare("null")!=0&&prcSelect.localeCompare("null")!=0&&conSelect.localeCompare("null")!=0){
		console.log("All Options Chosen");
		// Load loader circle
		$("#loaderContainer").html("<div class=\"loader\" style=\"margin:auto;\"></div>");
		$.getJSON(theurl, function(data) {
			// get rid of loader once the info has been fetched
			$("#loaderContainer").html("<div></div>");
			$.each(data, function(i, f) {

				var per=f.Perspective;
				var con=f.Subconcept.slice(0,f.Subconcept.indexOf("."));
				var prc=f.Subpractice.slice(0,f.Subpractice.indexOf("."));
				per=per.toLowerCase();
				con=con.toLowerCase();
				prc=prc.toLowerCase();
				if(perSelect.localeCompare(per)==0){
					if(prcSelect.localeCompare(prc)==0){
						if(conSelect.localeCompare(con)==0){
							console.log("Found Match(es)");
							$(".tblinfo").css("display","inline");
							var tblRow = "<tr id=\"userdata\">" +"<td id=\"userdata\">" + f.ICanStatement + "</td>" + "</tr>"
							$(tblRow).appendTo("#userdata tbody");
						}
					}
				}


			});

		});
	}

}

window.onload = function(){


		$(".prbtn").click(function(){
			document.getElementById("practice").innerHTML=($(this).html());
			prcSelect=$(this).attr('class').split(' ')[0];
			var prccon=prcSelect+"con2";
			$(".prcinfo").html($("."+prccon).html());
			$(".practice").addClass("practiceinvert");
			$(".practice").removeClass("practice");
			fetchStatement();
		});

		$(".conbtn").click(function(){
			document.getElementById("concept").innerHTML=($(this).html());
			conSelect=$(this).attr('class').split(' ')[0];
			var concon=conSelect+"con2";
			$(".coninfo").html($("."+concon).html());
			$(".concept").addClass("conceptinvert");
			$(".concept").removeClass("concept");

			fetchStatement();
		});
		$(".perbtn").click(function(){
			document.getElementById("perspective").innerHTML=($(this).html());
			perSelect=$(this).attr('class').split(' ')[0];
			$(".perspective").addClass("perspectiveinvert");
			$(".perspective").removeClass("perspective");
			var percon=perSelect+"con2";
			$(".perinfo").html($("."+percon).html());
			fetchStatement();

		});
	};
	function pracClick(){

	//document.getElementById("practice").innerHTML=$(this).data('value');
}
	/*
}
<a href="#" class="ab">abstractions</a>
			<a href="#" class="al">algorithms</a>
			<a href="#" class="p">programming</a>
			<a href="#" class="d">data</a>
			<a href="#" class="n">networks</a>
	*/
