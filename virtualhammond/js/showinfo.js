/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/

$(document).ready(function(){
	$("#showinfolist").ready(function(event){
        var parameters = location.search.substring(1).split("&");
		$.post("/listSongFiles",{musicid: parameters[0].split("=")[1]},function (data) {
			$('#showinfolist').append('<ul class="list-group">');
			if (data.message=="unsucess") {
				$('#showinfolist').append('<li class="list-group-item"><span>No information about this version.</span></li>');
			}
			else{
				for (var i=0;; i++)
				{
					var effects=[];
                    var v = parameters[1].split("=")[1];
					if(i > v) break;
                    if(i == v){
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
                        id=data[i].interpid;
                        $('#showinfolist').append('<div id="loading" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"><div class="modal-dialog"><div class="modal-content"><div class="modal-body"> <p>Please wait a few seconds...</p><img src="images/loading.gif" /><br><br><p>Please enable popups in your browser.</p></div></div></div></div>');
					    $('#showinfolist').append('<li class="list-group-item"> <b><span>'+data[i].nome+'	V'+(i+1)+'</span></li></b>   <li class="list-group-item"><div id="graph"></div></li>  <li class="list-group-item"><button type="button" class="btn btn-xs btn-primary" id="getaudio" data-toggle="modal" data-target="#loading">Audio file</button><div id="playerdiv" class="panel"><audio id="musicplayer" autoplay="autoplay" controls="controls"><source id="filesrc" src="" type="audio/wav"></audio></div></li><li class="list-group-item"><span>&nbsp;<b>Register:</b> '+data[i].register+'</span></li>   <li class="list-group-item"><span>&nbsp;<b>Effects: </b>'+effects.join(", ")+'</span></li>	<li class="list-group-item"><span>&nbsp;<b>Votes: </b><span id="tup-span">'+data[i].posvotes+'</span> <img src="images/thumbsup.png" class="thumbsimg" id="tup"/> <span id="tdwn-span">'+data[i].negvotes+'</span> <img src="images/thumbs-down.png" class="thumbsimg" id="tdwn"/></span></li>');
                        $("#tup" ).click(function() {
                            $("#tup-span").text(parseInt($("#tup-span").text()) + 1);
                            var uvote = parseInt($("#tup-span").text());
                            $.post("/updateVotes",{interpretationid: id, pos: uvote, neg: 0},function () {
                            });
                        });		
                        id=data[i].interpid;
                        $("#tdwn" ).click(function() {
                            $("#tdwn-span").text(parseInt($("#tdwn-span").text()) + 1);
                            var dvote = parseInt($("#tdwn-span").text());
                            $.post("/updateVotes",{interpretationid: id, pos: 0, neg: dvote},function () {
                            });
                        });
                        $("#getaudio").click(function(){
                            $.post("/getWaveFile",{interpretationid: id},function(data){
                                var local = data.message + "?version="+id;
                                $("#loading").modal('hide');
                                $("#playerdiv").slideDown("slow");
                                $("#filesrc").attr("src", local);
                                $("#musicplayer").load();
                            });
                        });
                    }
				}
			}
			$('#showinfolist').append('</ul>');
			
		});
	});
    $("#graph").ready(function(event){
        var parameters = location.search.substring(1).split("&");
        $.post("/getWaveForm",{musicid: parameters[0].split("=")[1]},function (data) {
            $('#graph').append('<img class="imgsize" src="images/notes.png">');
        });
    });

});


