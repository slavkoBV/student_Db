function initJournal() {
	var indicator = $('#ajax-progress-indicator');

	$('.day-box input[type="checkbox"]').click(function(event){
		var box = $(this);
		$.ajax(box.data('url'),{
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data': {
				'pk':box.data('student-id'),
				'date':box.data('date'),
				'present':box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr, settings){
				indicator.show();
			},
			'error': function(xhr, status, error){
				alert('error');
				indicator.hide();
			},
			'success': function(data, status, xhr){
				indicator.hide();
			}
		});
	});
}

function initGroupSelector(){
	$('#group-selector select').change(function(event){
		var group = $(this).val();
		if (group) {
			$.cookie('current_group', group, {'path': '/', 'expires': 365});
		} else {
			$.removeCookie('current_group', {'path': '/'});
		}
		location.reload(true);
		return true;
	});
}

$(document).ready(function(){
	initJournal();
	initGroupSelector();
});