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

    $("#edit_btn").click(function(){
        console.log("edit");
        var reqData = {
            'id': $("#product_id").val(),
            'name': $("#product_name").val(),
            'price': $("#product_price").val(),
            'quantity': $("#product_quantity").val(),
            'image': $("#product_image").val()
        }
        $.post('/admin/product/edit',reqData,function (rs,status) {
            alert(rs.message);
            console.log(rs);
        });
    });
});