/*
Daniel Alves e Luís Leira
Laboratórios de Informática, 2015
Projeto 2

Interface Web
*/

$(document).ready(function(){
	$("#showallsongs").ready(function(event){
		$.getJSON( "/listSongs",function (data) {
			$('#showallsongs').append('<ul class="list-group">')
			for (var i=0;i<data.length; i++)
			{
				$('#showallsongs').append('<li class="list-group-item">'+data[i].nome+'<div class="rightspace pull-right"> <button class="btn btn-xs btn-primary" id="'+data[i].musicid+'">Get Notes</button></div> <div class="rightspace pull-right"> <form method="GET" action="/newversion.html"> <input type="hidden" name="musicid"  value="'+data[i].musicid+'"/>	<input type="submit" value="New version" class="btn btn-xs btn-primary" id="ver'+data[i].musicid+'" /></form> </div> <div class="rightspace pull-right"><form method="GET" action="/showversions.html"><input type="hidden" name="musicid"  value="'+data[i].musicid+'"/> <input type="submit" value="Show versions" class="btn btn-xs btn-primary" id="ver'+data[i].musicid+'"/></form> </div><div id="shownotes'+data[i].musicid+'" class="panel"></div></li>');
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
	});
});

