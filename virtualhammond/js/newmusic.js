/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/

$(document).ready(function(){
	$("#newmusic").ready(function(event){
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
                    alert(data.message);
                });
            } else {
                alert('Something is wrong! Check what is wrong, change and try again!');
            }
        });
    });
});