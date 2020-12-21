$(document).ready(function(){
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.btn-favorite').on('click', function(event){
        event.preventDefault();
        var barcode = event.target.value;
        var fav_url = $('input[name=favorite_true_url]').first().val();
        console.log(fav_url);
        console.log(barcode);
        $.ajax({
            method: "POST",
            url: fav_url,
            contentType: "application/json",
            data: {
                "barcode" : barcode,
                "action": 'post'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                console.log(settings);
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
        // when the data are posted and treated we done the following things
        }).done(function (data) {
            console.log(data);
            $('button[type="submit"][value="'+barcode+'"]').attr("disabled", "disabled");
            $('button[type="submit"][value="'+barcode+'"]').html('<i class="far fa-save fa-2x"></i> Déjà ajouté dans la base de donnée.')
        })
    });
    $('.install-language').on('click', function(event){
        $('#ajax-loader').show();
        var language_code = $(this).val();
        $.ajax({
            method: "POST",
            url: "/search_food/install_language/",
            data: {'language_code': language_code},
            contentType: "application/json",
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                console.log(settings);
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
        }).done(function (data) {
            $('#ajax-loader').hide();
            console.log(data);
        })
    });
})