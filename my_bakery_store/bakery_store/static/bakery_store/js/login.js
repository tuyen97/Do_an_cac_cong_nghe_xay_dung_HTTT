$(document).ready(function(){
	$("#submit_btn").click(function(event){
		event.preventDefault();
		var isValid = validLoginForm();
		console.log(isValid);
		
	});
	function validLoginForm(){
		if($("#user_name").val() == ""){
			return false;
		}
		if($("#password").val().trim() == "")
			return false;
		return true;
	}
	function login(){
		//ajax
	}
});