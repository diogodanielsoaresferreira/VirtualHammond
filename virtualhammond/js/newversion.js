/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/

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