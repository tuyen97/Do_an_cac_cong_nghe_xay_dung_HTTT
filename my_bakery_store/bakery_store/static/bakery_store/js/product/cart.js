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
$(document).ready(function () {
    $('.quantity').on('change',function () {
        var count = $(this).val();
        var price = $(this).attr('name');
        var total = count * price;
        $(this).closest('.product-cart').find('span.tonggia').text(total);

    });
    $('.xoa_sp').on('click',function () {
        var data={
            id:$(this).attr('id')
        };
        console.log(data);
        $.post(
            'delete_product_on_cart', data,function (data,status) {
                alert(data['message']);
                location.reload();

            }
        )
        ;
    })
})