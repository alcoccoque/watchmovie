
       $( document ).ready(function() {
          console.log( "ready!" );
          addBinds();
        });
        function addBinds() {
          if($('.film').length == 0)
          {
            $("#mySlider").hide();
            $("#empty").show();
          }
          else
          {
            $("#empty").hide();
            $("#mySlider").show();
          }
          $('.delete').bind('click', function() {
            $.getJSON('/delete/'+this.id,
                function(data) {
            });
          $("#moviesBlock").load('mySlider #film', function() {
             addBinds();
           });

        return false;
      });
}
function addedToCart(val) {
  var successMsg = "<div class='alert alert-success text-center'><strong>Item added to cart!</strong>&nbsp;-&nbsp;<a href='cart'>Click here to see your cart</a></div>";
  var errorMsg = "<div class='alert alert-danger text-center'><strong>Error adding item to cart</strong></div>";
  if(val>0){
    // $('div.itemAdded').stop();
    $('div.top-success').fadeIn(500).delay(1500).fadeOut(500);
  }
  else{
    // $('div.itemAdded').stop();
    $('div.top-danger').fadeIn(500).delay(1500).fadeOut(500);
  }

}