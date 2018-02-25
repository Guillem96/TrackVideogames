$( document ).ready(function() {


    $(".add-pendent-button").click(function() {
        var form =  $(".pendent");

        var vg = $("#vg-name-pendent").val();
        var date = $("#date").val();

        if(vg === "" || id === 0) {
            swal("Ouch!", "No has introduït un videojoc!", "error");
            return
        }


        swal("Ok!", "Videojoc pendent afegit!", "success")
            .then(function () {
                form.attr("action", "/trackVideogames/video_games/"+ String(id) +"/pendent/add/?vg-name=" +
                            vg + "&data-pendent=" + date)
                form.submit();
        });

    });


    $(".create-review-button").click(function () {
        var form = $("#review-from-form");
        var vg = $("#vg-name").val();
        var comment = $("#comment").val();
        var ttb = $("#time-to-beat").val();
        var ttbRegex = new RegExp("^[0-9]+h [0-9]+min")
        var stars = $('input[name=rating]:checked', form).val()

        if (vg === "" || id === 0) {
            swal("Ouch!", "No has introduït un videojoc!", "error");
            return
        }

        if (comment === "") {
            swal("Ouch!", "No has introduït un comentari!", "error");
            return
        }

        if (ttb === "") {
            swal("Ouch!", "No has introduït una durada!", "error");
            return
        }

        if (!ttbRegex.test(ttb)) {
            swal("Ouch!", "La durada ha de ser expressada en format XXh XXmin!", "error");
            return
        }

        swal("Ok!", "Review afegida correctament!", "success")
            .then(function () {
                console.log("Hola")
                form.attr("action", "/trackVideogames/video_games/" + String(id) + "/reviews/create/?vg-name=" +
                    vg + "&rating=" + stars + "&comment=" + comment + "&time-to-beat=" + ttb)
                form.submit();
            });

    });

});

var id = 0;

function addToComplete(pk, name) {
    id = pk;
    document.getElementById('review-form').style.display='block';

    // Valors per defecte del formulari
    var nameInput = $("#vg-name");
    nameInput.val(name);
    nameInput.attr('disabled','disabled');

    $.ajax({
        url: "/trackVideogames/api/video_games/",
        dataType: 'json',
        data : {
            q: name
        },
        success: function( data ) {
            console.log(data);
            $(".vg-cover").attr("src", data[0].cover);
        }
    });


}