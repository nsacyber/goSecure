
jQuery(document).ready(function() {
    
    if( $("#ssid").val().substr($("#ssid").length-4) == "off" ){
            $("#psk").val("key_mgmt_none");
            $("#psk").attr("readonly", true);
            $("#wifi_pass_div").html("<b>This WiFi network does not require a password, please proceed.</b>");
    }

    
    // submit
    $("#wifiform").on('submit', function(e) {
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

    $("#ssid").change(function() {
        if( $(this).val().substr($(this).length-4) == "off" ){
            $("#psk").val("key_mgmt_none");
            $("#psk").attr("readonly", true);
            $("#wifi_pass_div").html("<b>This WiFi network does not require a password, please proceed.</b>");
        }
        else{
            $("#psk").attr("readonly", false);
            $("#psk").val("");
            $("#wifi_pass_div").html("");
        }
    });
    
});