// JavaScript Document
 

/*------- Menu in mobile set * -----------  */ 

  $(document).ready(function(){
    $('#nav-toggle').click(function(){
		//console.log('hi clcik');
      $('#sidebar').toggleClass('visible');

        $("body").toggleClass('menu_visible');

    });

    $(".menu-wrap").click(function(){
      $('#sidebar').toggleClass('visible');
      $("body").toggleClass('menu_visible');
    });
    $('.menu-wrap').click(function(){$('#um_header .um_mainnav ul.dropnav').hide();});
  });


/*--------  Menu in mobile set --------*/




