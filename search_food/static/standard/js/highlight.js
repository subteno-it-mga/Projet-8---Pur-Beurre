// This file allow to search a term in the modify translation page
$(document).ready(function(){
    $("#input_search_translation").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#table_translation tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
});
