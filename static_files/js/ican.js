var perSelect="null";
var prcSelect="null";
var conSelect="null";

function fecthStatement() {
	theurl="http://cs4all.nyc/api/ican";
	var people = [];
	$("#userdata tbody").empty();
	if(perSelect.localeCompare("null")!=0&&prcSelect.localeCompare("null")!=0&&conSelect.localeCompare("null")!=0){
		console.log("All Options Chosen");
		$.getJSON(theurl, function(data) {
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

	var old = $(".old").html();
		// var now = $(".cocon").html();

		$(".an").hover(
			function(){$(".old").html($(".ancon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".co").hover(
			function(){$(".old").html($(".cocon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".pr").hover(
			function(){$(".old").html($(".prcon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".ab").hover(
			function(){$(".old").html($(".abcon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".al").hover(
			function(){$(".old").html($(".alcon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".p").hover(
			function(){$(".old").html($(".pcon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".d").hover(
			function(){$(".old").html($(".dcon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".n").hover(
			function(){$(".old").html($(".ncon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".e").hover(
			function(){$(".old").html($(".econ").html());}, 
			function(){$(".old").html(old);}
			);
		$(".c").hover(
			function(){$(".old").html($(".ccon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".i").hover(
			function(){$(".old").html($(".iicon").html());}, 
			function(){$(".old").html(old);}
			);
		$(".z").hover(
			function(){$(".old").html($(".zcon").html());}, 
			function(){$(".old").html(old);}
			);

		$(".perbtn").hover(
			function(){
				$(".original").css("background-color","#17283e");
				$(".original").css("color","white");
				$(".prcinfo").css("display","none");
				$(".coninfo").css("display","none");
				$(".readMore").css("display","none");

			},
			function(){
				$(".original").css("background-color","lightgrey");
				$(".original").css("color","black");
				$(".prcinfo").css("display","inline");
				$(".coninfo").css("display","inline");
				$(".readMore").css("display","inline");

			}
			);

		$(".prbtn").hover(
			function(){
				$(".original").css("background-color","#2FA351");
				$(".original").css("color","white");
				$(".perinfo").css("display","none");
				$(".coninfo").css("display","none");
				$(".readMore").css("display","none");

			},

			function(){
				$(".original").css("background-color","lightgrey");
				$(".original").css("color","black");
				$(".perinfo").css("display","inline");
				$(".coninfo").css("display","inline");
				$(".readMore").css("display","inline");

			}
			);
		$(".conbtn").hover(
			function(){
				$(".original").css("background-color","#F26922");
				$(".original").css("color","white");
				$(".perinfo").css("display","none");
				$(".prcinfo").css("display","none");
				$(".readMore").css("display","none");

			},
			function(){
				$(".original").css("background-color","lightgrey");
				$(".original").css("color","black");
				$(".perinfo").css("display","inline");
				$(".prcinfo").css("display","inline");
				$(".readMore").css("display","inline");

			}
			);
		//#2FA351

		$(".prbtn").click(function(){
			document.getElementById("practice").innerHTML=($(this).html());
			prcSelect=$(this).attr('class').split(' ')[0];
			var prccon=prcSelect+"con2";
			$(".prcinfo").html($("."+prccon).html());
			$(".practice").addClass("practiceinvert");
			$(".practice").removeClass("practice");
			fecthStatement();
		});

		$(".conbtn").click(function(){
			document.getElementById("concept").innerHTML=($(this).html());
			conSelect=$(this).attr('class').split(' ')[0];
			var concon=conSelect+"con2";
			$(".coninfo").html($("."+concon).html());
			$(".concept").addClass("conceptinvert");
			$(".concept").removeClass("concept");

			fecthStatement();
		});
		$(".perbtn").click(function(){
			document.getElementById("perspective").innerHTML=($(this).html());
			perSelect=$(this).attr('class').split(' ')[0];
			$(".perspective").addClass("perspectiveinvert");
			$(".perspective").removeClass("perspective");
			var percon=perSelect+"con2";
			$(".perinfo").html($("."+percon).html());
			fecthStatement();

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