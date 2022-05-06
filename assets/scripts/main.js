function checkchanged(cb){
		
		cb.disabled = true;
		$('#modalCarregando').modal({
    		backdrop: 'static',
    		keyboard: false
		});
		$('#modalCarregando .close').css('display', 'none');
		$('#modalCarregando').modal("show");	

		var xhttp = new XMLHttpRequest();
		  xhttp.onreadystatechange = function() {		  	
		    if (this.readyState == 4 && this.status == 200) {		      
		    	cb.disabled = false;
		      if(this.responseText == 1) {		      	
		      	cb.checked = false;
		      	document.getElementById("spanAberto").innerHTML = "Fechado";		      	
		      	$('#modalFechado').modal("show");		      	
		      }
		      else {
		      	cb.checked = true;
		      	document.getElementById("spanAberto").innerHTML = "Aberto";			      	
		      	$('#modalAberto').modal("show");		      			      	
		      }
		      $('#modalCarregando').modal("hide");
		    }
		  };
		  xhttp.open("POST", "abrirfechar.php", true);
		  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		  xhttp.send("aberto="+(cb.checked ? 1 : 0));
		  xhttp.send();
		  
	}