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
  init();
	$('.singleSelect').fastselect();
  $('#time_range').on('change',function () {
    /*console.log($(this).val());*/
   /* $('#time_title').text($(this).val());*/
    statiscticsProduct();
  });
  function drawChart(result){
      var i=0;
      var length = result.length;
      var chartData = [];
      for(i = 0; i < length; i++){
        var element = result[i];
        var name = (Object.keys(element))[0];
        var soldProduct = element[name];
                // console.log(soldProduct);
        var temp = {
          y : name,
          a : soldProduct
        };
        chartData.push(temp);
        // console.log(chartData);
      }
      var bar = new Morris.Bar({
        element: 'product-chart',
        resize: true,
        data: chartData,
        barColors: ['#00a65a'],
        xkey: 'y',
        ykeys: ['a'],
        labels: ['Đã bán'],
        hideHover: 'auto'
      });

  }
  function init(){
    statiscticsProduct();

  }
  function statiscticsProduct(){
    data = {
      'range': $('#time_range').val()
    };

    console.log(data);
    $.post('/admin/product/statistics',data,function (data) {

    console.log(data);
    
        $('#product-chart').empty();
        // console.log(data);
        var result = data.static_list;
        drawChart(result);
    });
  }
    
});