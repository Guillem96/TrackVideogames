$( document ).ready(function() {
    var id = 0;
    $("#vg-name").autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/trackVideogames/api/video_games/",
                dataType: 'json',
                data : {
                    q: request.term
                },
                success: function( data ) {
                    response( $.map( data, function( item ) {
                            return {
                                label: item.name ,
                                value: item.name,
                                cover: item.cover,
                                id: item.videogame_id
                            }
                    }));
                },
            });
        },
        select: function (a, b) {
            $(".vg-cover").attr("src", b.item.cover);
            id = b.item.id
        },
        minLength:2,
    });

    $(".create-review-button").click(function() {
        var form =  $("form");

        var vg = $("#vg-name").val();
        var comment = $("#comment").val();
        var ttb = $("#time-to-beat").val();
        var ttbRegex = new RegExp("^[0-9]+h [0-9]+min")
        var stars = $('input[name=rating]:checked', form).val()

        if(vg === "" || id === 0) {
            swal("Ouch!", "No has introduït un videojoc!", "error");
            return
        }

        if(comment === "") {
            swal("Ouch!", "No has introduït un comentari!", "error");
            return
        }

        if(ttb === "") {
            swal("Ouch!", "No has introduït una durada!", "error");
            return
        }

        if(!ttbRegex.test(ttb)){
            swal("Ouch!", "La durada ha de ser expressada en format XXh XXmin!", "error");
            return
        }

        swal("Ok!", "Review afegida correctament!", "success")
            .then(function () {
                form.attr("action", "/trackVideogames/video_games/"+ String(id) +"/reviews/create/?vg-name=" +
                            vg + "&rating=" + stars + "&comment=" + comment + "&time-to-beat=" + ttb)
                form.submit();
        });

    });

    $('[data-toggle="tooltip"]').tooltip();

});