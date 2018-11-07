$(document).ready(function(){
	var html5Vars = 'abbr,article,aside,audio,canvas,datalist,details,eventsource,figure,footer,header,hgroup,mark,menu,meter,nav,output,progress,section,time,video';
	var html5Tags = html5Vars.split(',');
	for(var i = 0, len = html5Tags.length ; i < len ; i++ ){var tag = html5Tags[i];	$(tag).addClass(tag);}
});
