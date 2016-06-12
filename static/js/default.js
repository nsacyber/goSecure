jQuery(document).ready(function() {
    
    /*
        Fullscreen background
    */
    $.backstretch("/static/img/backgrounds/1.jpg");
    
    $('.registration-form fieldset:first-child').fadeIn('slow');
    
    $('.registration-form input[type="text"], .registration-form input[type="password"], .registration-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('a[href="#restart_vpn"]').click(function(){
        $("#message-div").html('Please wait... VPN is restarting.<br><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i><span class="sr-only">Loading...</span>');
    });
    
});