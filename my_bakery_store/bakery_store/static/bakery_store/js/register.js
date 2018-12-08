$(document).ready(function(){
	$("#submit_btn").click(function(event){
		event.preventDefault();
		var isValid = validRegisterForm();
		console.log(isValid);
		console.log($("#birth_day").val() + "...");
	});
	function validRegisterForm(){
		if($("#full_name").val() == ""){
			return false;
		}
		if($("#user_name").val() == ""){
			return false;
		}
		if($("#email").val() == ""){
			return false;
		}
		if($("#address").val() == ""){
			return false;
		}
		if($("#gender").val() == "")
			return false;
		if($("#birth_day").val() == "")
			return false;
		if($("#password").val().trim() == "")
			return false;
		if($("#confirmed_password").val().trim() != $("#password").val().trim())
			return false;
		return true;
	}
	function register(){
		//ajax
	}
});