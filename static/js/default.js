jQuery(document).ready(function() {
    
    /*
        Fullscreen background
    */
    $.backstretch("/static/img/backgrounds/1.jpg");
    
    /*
        Form
    */
    $('.registration-form fieldset:first-child').fadeIn('slow');
    
    $('.registration-form input[type="text"], .registration-form input[type="password"], .registration-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
});