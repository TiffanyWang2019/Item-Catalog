function message(status, shake=false, id="") {
  if (shake) {
    $("#"+id).effect("shake", {direction: "right", times: 2, distance: 8}, 250);
  } 
  document.getElementById("feedback").innerHTML = status;
  $("#feedback").show().delay(2000).fadeOut();
}

function error(type) {
  $("."+type).css("border-color", "#E14448");
}

var login = function() {
  $.post({
    type: "POST",
    url: "/",
    data: {"username": $("#login-user").val(), 
           "password": $("#login-pass").val()},
    success(response){
      var status = JSON.parse(response)["status"];
      if (status === "Login successful") { location.reload(); }
      else { error("login-input"); }
    }
  });
};

$(document).ready(function() {
  
  $(document).on("click", "#login-button", login);
  $(document).keypress(function(e) {if(e.which === 13) {login();}});
  
  $(document).on("click", "#signup-button", function() {
    $.post({
      type: "POST",
      url: "/signup",
      data: {"username": $("#signup-user").val(), 
             "password": $("#signup-pass").val(), 
             "email": $("#signup-mail").val()},
      success(response) {
        var status = JSON.parse(response)["status"];
        if (status === "Signup successful") { location.reload(); }
        else { message(status, true, "signup-box"); }
      }
    });
  });

  $(document).on("click", "#save", function() {
    $.post({
      type: "POST",
      url: "/settings",
      data: {"username": $("#settings-user").val(), 
             "password": $("#settings-pass").val(), 
             "email": $("#settings-mail").val()},
      success(response){
        message(JSON.parse(response)["status"]);
      }
    });
  });


  $( ".catalog a" ).click(function() {    
    var $this = $(this);
    $("a").not(this).removeClass("active");
    $this.toggleClass("active");
    // alert($this.attr("category_id"))
    $.post({
      type: "POST",
      url: "/showcatalogs",
      data: {"id": $this.attr("category_id"), 
            },
      success(response){
        $("#categoryname").text($this.text() + " (Empty)"); 
        var json = JSON.parse(response)["ret"]
        $(".item-group").empty();
        var len = json.length ;
        for(var i = 0; i < json.length; i++) {
          var obj = json[i];      
          // alert(obj.id);
          $(".item-group").append("<a href=/showitem/" + obj.id + " " + "class=list-group-item" + " " + "item_id=" + obj.catalog_name + ">" + obj.item_name + "(" + obj.catalog_name + ")" + "</a>")
          $("#categoryname").text(obj.catalog_name + "(" + len + " item" + ")"); 
        }
      }
    });
  });

  var selected = -1 
  $(".dropdown-menu li a").click(function(){    
    $(".btn:first-child").text($(this).text());
    $(".btn:first-child").val($(this).text());
    var id = $(this).attr("data-value");
    selected = id ;
    $(".categoryindex").attr("value",id)
  });

  $( ".edit" ).click(function() {    
      $(".itemname").attr("readonly", false);
      $(".descriptioncontent").attr("readonly", false);            
  });
  
  $('#delete_btn').click(function(){
    /* when the submit button in the modal is clicked, submit the form */      
    $('#formfield').submit();
}); 
$("#formfield").submit( function(eventObj) {  
  $("<input />").attr("type", "hidden")
      .attr("name", "action")
      .attr("value", "delete")
      .appendTo("#formfield");
  return true;
});

$('#warnng_message').hide()

$('#additembutton').on("click",function(e) {
    var name = $("#itemname").val()
    var content = $("#descriptioncontent").val()    
    if (name.length == 0 || content.length == 0 || selected == -1) {            
      e.preventDefault();  
      $('#warnng_message').show()    
      setTimeout(function() { $("#warnng_message").hide(); }, 3000);
    } else {
       $("additemform").submit();
    }
}); 




});

// Open or Close mobile & tablet menu
// https://github.com/jgthms/bulma/issues/856
$("#navbar-burger-id").click(function () {
  if($("#navbar-burger-id").hasClass("is-active")){
    $("#navbar-burger-id").removeClass("is-active");
    $("#navbar-menu-id").removeClass("is-active");
  }else {
    $("#navbar-burger-id").addClass("is-active");
    $("#navbar-menu-id").addClass("is-active");
  }
});