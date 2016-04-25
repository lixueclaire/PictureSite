$(window).on("load",function(){
	$('.grid').masonry({
		// options
		itemSelector: '.grid-item',
		columnWidth: 285
	});
});

function mOver(id)
{
	document.getElementById(id).style.visibility='visible'
	
}

function mOut(id)
{
	document.getElementById(id).style.visibility='hidden'
}