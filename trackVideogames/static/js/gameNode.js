
function deleteReview(id, name) {
    swal({
      title: "Estàs segur?",
      text: "Vols eliminar la review del joc " + name,
      icon: "warning",
      buttons: true,
      dangerMode: true,
    })
    .then(function (willDelete) {
      if (willDelete) {
        swal("OK!", "S'ha eliminat correctament", "success").then(function () {
            window.location.href = "/trackVideogames/video_games/" + id +"/review/delete/?next=" + window.location.pathname;
        });
      } else {
        swal("OK!","No has eliminat la review", "success");
      }
    });
}