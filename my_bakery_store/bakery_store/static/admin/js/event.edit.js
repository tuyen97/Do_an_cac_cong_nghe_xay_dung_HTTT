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
	$('.multipleSelect').fastselect();
		$("#submit_btn").click(function(){
		/*console.log("id " + $("#event_id").val());
		console.log("name " + $("#name").val());
		console.log("start " + $("#start").val());
		console.log("end " + $("#end").val());
		console.log("sale " + $("#sale").val());
		console.log("products " + $("#products").val());*/
		var isValid = validateForm();
		console.log(isValid);

		console.log(typeof($("#products").val()));
		var products = $("#products").val();
		//array
		console.log(products);
		/*var divParent = document.getElementById("error_notify");
		notifyError(divParent,"Sai kia..");*/
		if(isValid){
			data = {
				event_id : $('#event_id').val(),
				name : $('#name').val(),
				start : $('#start').val(),
				end: $('#end').val(),
				sale : $('#sale').val(),
				products: $('#products').val(),
				id : $('#uuid').val()
			}
			$.post(
				'',
				data,
				function (data) {
					alert(data['message'])
				}
				);
		}


	});
	function validateForm(){
		// if($("#event_id").val() == ""){
		// 	var divParent = document.getElementById("error_notify");
		// 	notifyError(divParent,"Nhập mã sự kiện");
		// 	return false;
		// }
		if($("#name").val() == ""){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Nhập tên sự kiện");
			return false;
		}
		if($("#start").val() == ""){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Nhập ngày bắt đầu sự kiện");
			return false;
		}
		if($("#end").val() == ""){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Nhập ngày kết thúc sự kiện");
			return false;
		}
		if($("#sale").val() == ""){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Nhập số lượng giảm giá");
			return false;
		}
		if(isNaN($("#sale").val())){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Giá trị phải là số");
			return false;
		}
		if($("#sale").val() < 0){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Giá trị phải > 0");
			return false;
		}
		if($("#sale").val() > 100){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Giá trị phải < 100");
			return false;
		}

		if($("#products").val() == ""){
			var divParent = document.getElementById("error_notify");
			notifyError(divParent,"Chọn sản phẩm áp dụng");
			return false;
		}
		return true;
	}
	function notifyError(parent, content){
		var divNode = document.createElement("div");
		var aNode = document.createElement("a");
		var strongNode = document.createElement("strong");
		//&times
		var aContentNode = document.createTextNode("\u00d7")
		var strongContentNode = document.createTextNode("Error");
		var divContentNode = document.createTextNode(content);
		divNode.className = "alert alert-danger alert-dismissible";
		aNode.setAttribute("href","javascript:void(0)");
		aNode.className = "close";
		aNode.setAttribute("data-dismiss", "alert");
		aNode.setAttribute("aria-label", "close");
		aNode.appendChild(aContentNode);
		divNode.appendChild(aNode);
		divNode.appendChild(strongNode);
		divNode.appendChild(divContentNode);
		parent.appendChild(divNode);
	}

});
