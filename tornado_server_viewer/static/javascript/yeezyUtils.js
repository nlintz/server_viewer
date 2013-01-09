function filterByRegex(regex)
{
	$('.file-element').filter(function(){ return ($(this).attr('id') ).match(regex) }).hide()
}