/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/

$(document).ready(function(){
	$("#showversionsongs").ready(function(event){
        var m = location.search.substring(1).split("=")[1];
		$.post("/listSongFiles",{musicid: m},function (data) {
			$('#showversionsongs').append('<ul class="list-group">');
			if (data.message=="unsucess") {
				$('#showversionsongs').append('<li class="list-group-item"><span>No version for this song yet.</span></li>');
			}
			else{
				for (var i=0;; i++)
				{
					var effects=[];
					if (data[i].effect_echo!="None"){
						effects.push("Echo");
					}
					if (data[i].effect_tremolo!="None"){
						effects.push("Tremolo");
					}
					if (data[i].effect_perc!="None"){
						effects.push("Percussion");
					}
					if (data[i].effect_chorus!="None"){
						effects.push("Chorus");
					}
					if (data[i].effect_dist!="None"){
						effects.push("Distortion");
					}
					if (data[i].effect_texttt!="None"){
						effects.push("Envelope");
					}
					$('#showversionsongs').append('<li class="list-group-item"><div class="pull-right"> <form method="GET" action="/showinfo.html"><input type="hidden" name="musicid"  value="'+m+'"/> <input type="hidden" name="version"  value="'+i+'"/>	<input type="submit" value="Show info" class="btn btn-xs btn-primary" id="ver'+data[i].interpid+'" /></form></div> 	<span>'+data[i].nome+'	V'+(i+1)+'</span>	<i><span>&nbsp;Register: '+data[i].register+'</span>		<span>&nbsp;Effects: '+effects.join(", ")+'</span></i></li>');
				}
			}
			$('#showversionsongs').append('</ul>');
			
		});
	});
});