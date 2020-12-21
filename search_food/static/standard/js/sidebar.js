/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("page-top").style.marginLeft = "250px";
  }
  
  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("page-top").style.marginLeft = "0";
  }
  
  $('#language-sidebar').on('click', function(){
    let sidebar = $('#mySidebar');
    let top = $('#page-top');

    if(sidebar.width() === 0){
      sidebar.width(250);
      top.css("margin-left", "250px");
    }
    else {
      sidebar.width(0);
      top.css("margin-left", "0px");
    }
  })

  $("body").on('focus', function(){
    $('#mySidebar').width(0);
    $('#page-top').css("margin-left", "0px");
  })