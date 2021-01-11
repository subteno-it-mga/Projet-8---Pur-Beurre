$(document).ready(function(){
    $('.modify_text_language').on('click', function(e){
        console.log($(this).parent().find('span'));
        $(this).find('input').attr('type', 'text');
    });
})