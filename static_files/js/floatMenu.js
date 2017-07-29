window.onload = function(){
  $(function() {

      function moveFloatMenu() {
          var menuOffset
          var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
          //set offset using windowWidth rules
          if(w>991){
            menuOffset = 10 + $(this).scrollTop() + "px";
          } else {
            menuOffset = 10 + "px";
          }
          $('#floatMenu').animate({
              top: menuOffset
          }, {
              duration: 500,
              queue: false
          });
      }

      // menuYloc = $('#floatMenu').offset();
      $(window).scroll(moveFloatMenu);
      $(window).resize(moveFloatMenu);

      //get the window dimensions
      // var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      // console.log(w);
      //if width is less than one of the breakpoints, don't call this function.

      moveFloatMenu();
  });
}
