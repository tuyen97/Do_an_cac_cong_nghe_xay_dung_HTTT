
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

// function getCookie(name)
// {
//     var cookieValue = null;
//     if (document.cookie && document.cookie != '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// $.ajaxSetup({
//      beforeSend: function(xhr, settings) {
//          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
//              // Only send the token to relative URLs i.e. locally.
//              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//          }
//      }
// });
// $(document).ready(function(){
// 	$('.singleSelect').fastselect();
//
// 	 //-------------
//     //- BAR CHART -
//     //-------------
//     //Data
//   $('#time_range').on('change',function () {
//         console.log($(this).val());
//         data = {
//           'range': $(this).val()
//         };
//         $.post(
//             '',
//             data,
//             function (data) {
//               console.log(data)
//             }
//         )
//     });
//     var areaChartData = {
//       labels  : ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
//       datasets: [
//         {
//           label               : 'Electronics',
//           fillColor           : 'rgba(210, 214, 222, 1)',
//           strokeColor         : 'rgba(210, 214, 222, 1)',
//           pointColor          : 'rgba(210, 214, 222, 1)',
//           pointStrokeColor    : '#c1c7d1',
//           pointHighlightFill  : '#fff',
//           pointHighlightStroke: 'rgba(220,220,220,1)',
//           data                : [65, 59, 80, 81, 56, 55, 40]
//         },
//         {
//           label               : 'Digital Goods',
//           fillColor           : 'rgba(60,141,188,0.9)',
//           strokeColor         : 'rgba(60,141,188,0.8)',
//           pointColor          : '#3b8bba',
//           pointStrokeColor    : 'rgba(60,141,188,1)',
//           pointHighlightFill  : '#fff',
//           pointHighlightStroke: 'rgba(60,141,188,1)',
//           data                : [28, 48, 40, 19, 86, 27, 90]
//         },
//         {
//           label               : 'Jewllery',
//           fillColor           : '#bd1616',
//           strokeColor         : '#bd1616',
//           pointColor          : '#bd1616',
//           pointStrokeColor    : '#bd1616',
//           pointHighlightFill  : '#fff',
//           pointHighlightStroke: '#bd1616',
//           data                : [22, 28, 41, 15, 26, 37, 70]
//
//         }
//     }
//     return cookieValue;
// }
//
// $.ajaxSetup({
//      beforeSend: function(xhr, settings) {
//          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
//              // Only send the token to relative URLs i.e. locally.
//              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//          }
//      }
// });

$(document).ready(function(){
  init();
  $('.singleSelect').fastselect();
  $('#time_range').on('change',function () {
    /*console.log($(this).val());*/
   /* $('#time_title').text($(this).val());*/
    statiscticsRevenue();
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
        element: 'revenue-chart',
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
    statiscticsRevenue();

  }
  function statiscticsRevenue(){
    data1 = {
      'range': $('#time_range').val()
    };

    console.log(data1);
    $.post('',data1,function (data) {
        console.log("aaa");
        console.log(data);
        $('#revenue-chart').empty();
        /*console.log(data);*/
        var result = data.static_list;
        drawChart(result);
    });
  }
    
});