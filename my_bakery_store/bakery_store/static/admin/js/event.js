function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
$(document).ready(function(){
	$('#event_table').DataTable();
	$('.kichhoat_sk').on('click',function () {
		console.log($(this).id);
		data = {
			id: $(this).attr('id'),
			kichhoat:1
		}
		$.post('event/change',
			data,
			function (data) {
				alert(data['message']);
				location.reload();
			})
	});
	$('.ketthuc_sk').on('click',function () {
		console.log($(this).id);
		data = {
			id: $(this).attr('id'),
			ketthuc:1
		}
		$.post('event/change',
			data,
			function (data) {
				alert(data['message']);
				location.reload();
			})
	});
	$('.xoa_sk').on('click',function () {
		console.log($(this).id);
		data = {
			id: $(this).attr('id'),
			ketthuc:1
		}
		$.post('event/change',
			data,
			function (data) {
				alert(data['message']);
				location.reload();
			});
	});
});
