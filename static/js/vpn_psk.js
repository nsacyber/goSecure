
jQuery(document).ready(function() {
    
    // submit
    $("#vpnpskform").on('submit', function(e) {
        var isValid = true;
    	$(this).find('input[type="text"], input[type="password"]').each(function() {
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
                isValid = false;
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
        if(isValid == true){
            $("#message-div").html('Please wait... you will be connected in less than 30 seconds.<br><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i><span class="sr-only">Loading...</span>');
        }
    });

});