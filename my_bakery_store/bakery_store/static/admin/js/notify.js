$(document).ready(function(){
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
	function notifySuccess(parent, content){
		var divNode = document.createElement("div");
		var aNode = document.createElement("a");
		var strongNode = document.createElement("strong");
		//&times
		var aContentNode = document.createTextNode("\u00d7")
		var strongContentNode = document.createTextNode("Error");
		var divContentNode = document.createTextNode(content);
		divNode.className = "alert alert-success alert-dismissible";
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