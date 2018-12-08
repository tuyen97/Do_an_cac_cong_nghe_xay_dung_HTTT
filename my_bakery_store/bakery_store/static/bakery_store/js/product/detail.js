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
    var rating = 0;
    $('#add_to_cart').on('click',function () {
         var data = {
            id: $(this).attr('name'),
            count: 1
        };
        $.post('add_to_cart',data,function (data,status) {
            alert(data['message']);
        });
        // $.ajax({
        //     url:"add_to_cart",
        //     data:data,
        //     type:"POST",
        //     beforeSend: function(xhr){xhr.setRequestHeader('X-CSRFToken', "{{csrf_token}}");},
        //      success: likeSuccess,
        //     }
        //
        // );
    });
    // using jQuery
    var artaraxRatingStar = $.artaraxRatingStar({
          onClickCallBack: onRatingStar
      });
    function onRatingStar(rate, id) {
      rating = rate;
      $('#rating').val(rate);
    };
    // $("#comment_btn").click(function(){
    //     var cmt = document.getElementById("comment");
    //     var fd = new FormData((cmt));
    //
    //     var reqData = {
    //         'product_id' : $("#product_id").val(),
    //         'customer_id' : $("#customer_id").val(),
    //         'rating': rating,
    //         'text_content' : $("#text_content").val(),
    //
    //     }
    //     console.log(fd);
    //     $.post(
    //         '/add_comment',
    //         fd,
    //         function (data, status) {
    //             alert(data['message']);
    //         }
    //     )
    // })
});