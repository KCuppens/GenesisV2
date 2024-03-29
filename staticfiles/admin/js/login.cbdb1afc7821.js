function checkbtn() {
      var x = document.getElementById("password");
      if (x.type === "password") {
        x.type = "text";
      } else {
        x.type = "password";
      }
    }
$("#loginform").submit(function(e){
      e.preventDefault()
      var serveurl=$("#loginform").attr('action');
      var serializedData = $("#loginform").serialize();
      $.ajax({
            url:serveurl,
            type:"POST",
            datatype:"json",
            data: serializedData,
            csrfmiddlewaretoken: '{{ csrf_token }}',
            success: function(data){
                  if(data.url){
                        window.location.href=data.url
                  }else if(data.errorpass){
                        $("#feedback2").slideDown(200).css("display","block");
                        $("#password").addClass("border border-danger rounded");
                        $("#password").keypress(function(){
                              $("#feedback2").removeAttr('style');
                              $("#password").removeClass("border border-danger rounded")
                        });
                        
                  } else if(data.invalup){
                        $("#feedback").slideDown(200).css("display","block");
                        $("#username").addClass("border border-danger rounded");
                        $("#feedback2").slideDown(200).css("display","block");
                        $("#password").addClass("border border-danger rounded");
                        $("#username").keypress(function(){
                              $("#feedback").removeAttr('style');
                              $("#username").removeClass("border border-danger rounded")
                              $("#feedback2").removeAttr('style');
                              $("#password").removeClass("border border-danger rounded")
                        });           
                  }
            }
      });
});
