/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/


//mnewversion.html

$(document).ready(function(){
	$("#newversion").ready(function(event){
        var parameters = location.search.substring(1).split("&");
        $("#addversion").click(function(){
            var reg, check = true, echo, trem, perc, chor, dist, env;
            
            if ( $('#echoinput2').prop('checked') ) {
                echo = "echo";
            } else {
                echo = "None";
            }
            if ( $('#treminput2').prop('checked') ) {
                trem = "tremolo";
            } else {
                trem = "None";
            }
            if ( $('#percinput2').prop('checked') ) {
                perc = "perc";
            } else {
                perc = "None";
            }
            if ( $('#chorusinput2').prop('checked') ) {
                chor = "chorus";
            } else {
                chor = "None";
            }
            if ( $('#distinput2').prop('checked') ) {
                dist = "dist";
            } else {
                dist = "None";
            }
            if ( $('#envinput2').prop('checked') ){
                env = "textttenv" ;
            }else{
                env = "None";
            }
            
            reg = document.getElementById('registerinput2').value;
            if (reg.length != 9 || isNaN(reg)) {
                check = false;
            }
            
            for(var k = 0; k < 8; k++){
                if(reg.charAt(k) == "9") check = false;
            }
            
            if (check == true) {
                $.post("/createInterpretation",
                {
                    musicid: parameters[0].split("=")[1],
                    register: reg,
                    effect_echo: echo,
                    effect_tremolo: trem,
                    effect_perc: perc,
                    effect_chorus: chor,
                    effect_dist: dist,
                    effect_textttenv: env
                },
                function (data) {
                    alert('The new version was created with success!');
                });
            } else {
                alert('Something is wrong! Check what is wrong, change and try again!');
            }
        });
    });    
});


//mshowall.html

function menuPush(){
    if($("#showallsongs").length){
        $.getJSON( "/listSongs",function (data) {
            $('#showallsongs').append('<ul class="table-view" style ="list-style-type: none">')
            for (var i=0;i<data.length; i++)
            {
                $('#showallsongs').append('<li class="table-view-cell" style ="list-style-type: none">'+data[i].nome+'<div><div class="topspace rightspace pull-right"> <button class="btn btn-primary" id="'+data[i].musicid+'">Get Notes</button></div> <div class="topspace rightspace pull-right"> <form method="GET" action="/mnewversion.html"> <input type="hidden" name="musicid"  value="'+data[i].musicid+'"/>	<input type="submit" value="New version" class="btn btn-primary" id="ver'+data[i].musicid+'" /></form> </div> <div class="topspace rightspace pull-right"><form method="GET" action="/mshowversions.html"><input type="hidden" name="musicid"  value="'+data[i].musicid+'"/> <input type="submit" value="Show versions" class="btn btn-primary" id="ver'+data[i].musicid+'"/></form> </div><div id="shownotes'+data[i].musicid+'" class="panel"></div></div></li>');
                m='#'+data[i].musicid.toString();
				$(m).click(function() {
					mid=this.id;
					$.post("/getNotes",{musicid: mid},function (data) {
						str_shownotes = '#shownotes'+mid.toString();
						$(str_shownotes).text(data[0].stave);
						$(str_shownotes).slideToggle("slow");	
					});
				});
            }
            $('#showallsongs').append('</ul>');
        });
    }
}


//mnewmusic.html

function menuNew(){
    if($("#newmusic").length){
        var parameters = location.search.substring(1).split("&");
        $("#addsong").click(function(){
            var name, song, reg, check = true, echo, trem, perc, chor, dist, env;

            if ( $('#echoinput').prop('checked') ) {
                echo = "echo";
            } else {
                echo = "None";
            }
            if ( $('#treminput').prop('checked') ) {
                trem = "tremolo";
            } else {
                trem = "None";
            }
            if ( $('#percinput').prop('checked') ) {
                perc = "perc";
            } else {
                perc = "None";
            }
            if ( $('#chorusinput').prop('checked') ) {
                chor = "chorus";
            } else {
                chor = "None";
            }
            if ( $('#distinput').prop('checked') ) {
                dist = "dist";
            } else {
                dist = "None";
            }
            if ( $('#envinput').prop('checked') ){
                env = "textttenv" ;
            }else{
                env = "None";
            }

            name = document.getElementById('nameinput').value;
            song = document.getElementById('songinput').value
            reg = document.getElementById('registerinput').value;
            if (name.length == 0 || song.length == 0 || reg.length != 9 || isNaN(reg)) {
                check = false;
            }

            for(var k = 0; k < 8; k++){
                if(reg.charAt(k) == "9") check = false;
            }

            if (check == true) {
                $.post("/createSong",
                {
                    name: name,
                    notes: song,
                    register: reg,
                    effect_echo: echo,
                    effect_tremolo: trem,
                    effect_perc: perc,
                    effect_chorus: chor,
                    effect_dist: dist,
                    effect_textttenv: env
                },
                function (data) {
                    alert('The song was created with success!');
                });
            } else {
                alert('Something is wrong! Check what is wrong, change and try again!');
            }
        });
    }   
}
window.addEventListener('push', menuPush)
window.addEventListener('push', menuNew)
window.addEventListener('load', menuPush)
window.addEventListener('load', menuNew)


//mshowversions.html

$(document).ready(function(){
        $("#showversionsongs").ready(function(event){
            var m = location.search.substring(1).split("=")[1];
            $.post("/listSongFiles",{musicid: m},function (data) {
                $('#showversionsongs').append('<ul class="table-view" style ="list-style-type: none">');
                if (data.message=="unsucess") {
                    $('#showversionsongs').append('<li class="table-view-cell"><span>No version for this song yet.</span></li>');
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
                        $('#showversionsongs').append('<li class="table-view-cell" style ="list-style-type: none"><div class="pull-right"> <form method="GET" action="/mshowinfo.html"><input type="hidden" name="musicid"  value="'+m+'"/> <input type="hidden" name="version"  value="'+i+'"/>	<input type="submit" value="Show info" class="btn btn-primary" id="ver'+data[i].interpid+'" /></form></div> 	<span>'+data[i].nome+'	V'+(i+1)+'</span>	<i><span>&nbsp;Register: '+data[i].register+'</span>		<span>&nbsp;Effects: '+effects.join(", ")+'</span></i></li>');
                    }
                }
                $('#showversionsongs').append('</ul>');

            });
        });
});


//mshowinfo.html

$(document).ready(function(){
	$("#showinfolist").ready(function(event){
        var parameters = location.search.substring(1).split("&");
		$.post("/listSongFiles",{musicid: parameters[0].split("=")[1]},function (data) {
			$('#showinfolist').append('<ul class="table-view" style ="list-style-type: none">');
			if (data.message=="unsucess") {
				$('#showinfolist').append('<li class="table-view-cell" style ="list-style-type: none"><span>No information about this version.</span></li>');
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
                        
					    $('#showinfolist').append('<li class="table-view-cell" style ="list-style-type: none"> <b><span>'+data[i].nome+'	V'+(i+1)+'</span></li></b>   <li class="table-view-cell" style ="list-style-type: none"><div id="graph"></div></li>   <li class="table-view-cell" style ="list-style-type: none"> <div class="topspace"><button class="btn btn-primary" id="getaudio">Audio file</button> <span id="loading"></span> <div id="playerdiv" class="panel"><audio id="musicplayer" autoplay="autoplay" controls="controls"><source id="filesrc" src="" type="audio/wav"></audio></div></div></li> <li class="table-view-cell" style ="list-style-type: none"><span>&nbsp;<b>Register:</b> '+data[i].register+'</span></li>   <li class="table-view-cell" style ="list-style-type: none"><span>&nbsp;<b>Effects: </b>'+effects.join(", ")+'</span></li>	<li class="table-view-cell" style ="list-style-type: none"><span>&nbsp;<b>Votes: </b><span id="tup-span">'+data[i].posvotes+'</span> <img src="images/thumbsup.png" class="thumbsimg" id="tup"/> <span id="tdwn-span">'+data[i].negvotes+'</span> <img src="images/thumbs-down.png" class="thumbsimg" id="tdwn"/></span></li>');
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
                            $("#loading").text("Loading...");
                            $.post("/getWaveFile",{interpretationid: id},function(data){
                                var local = data.message + "?version="+id;
                                $("#loading").text("");
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