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
        var count = parseInt($(this).val());
        console.log(count);
        if(count > parseInt($(this).attr('max')) || count < parseInt($(this).attr('min')) || !Number.isInteger(count)){
            alert('Invalid');
        }else {
            count = parseInt(count);
            var price = $(this).attr('name');
            var total = count * price;
            $(this).closest('.product-cart').find('span.tonggia').text(total);
            var id = $(this).closest('div').attr('name');
            var data = {
                id:id,
                count:count
            }
            $.post('change_quantity_on_cart',data,function (data, status) {
                console.log(data['message']);
                var t = data['total'];
                t = t.toLocaleString();
                console.log(t);
                $('#thanh_tien').text(t);
            })
        }
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