$(document).ready(function(){
    $('.btn-favorite').on('click', function(event){
        event.preventDefault();
        var barcode = $(this).val();
        $.ajax({
            type: "POST",
            url: "/search_food/add_favorite/",
            data: {"barcode" : barcode},
            dataType: 'json'
    
        // when the data are posted and treated we done the following things
        }).done(function (data) {
            $('button[type="submit"][value="'+barcode+'"]').attr("disabled", "disabled");
            $('button[type="submit"][value="'+barcode+'"]').html('<i class="far fa-save fa-2x"></i> Déjà ajouté dans la base de donnée.')
        })
    });
    
})