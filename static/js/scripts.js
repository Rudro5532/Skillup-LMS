const nameRegex = /^([A-Za-z]{2,})(\s[A-Za-z]{2,})$/;
const usernameRegex = /^@([a-z0-9_]{3,})$/;
const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}/;


//registration ajax
$(document).ready(function(){
  console.log("LMS dom is ready Teacher")

  $("#register").click(function(event){
    event.preventDefault()
    console.log("We ar inside in ready function")

    const username = $("#username").val()
    const name = $("#name").val()
    const email = $("#email").val()
    const password = $("#password").val()
    const confirm_password = $("#confirm_password").val()
    const subject = $("#subject").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();


    if(!name || !username || !email || !password){
        $("#response").html("<p style='color:red'>All field ar requeried</p>")
        return
    }

    if(subject !== undefined && !subject){
        $("#response").html("<p style='color:red'>Subject is required for teacher registration</p>")
        return
    }

    if(password !== confirm_password){
        $("#response").html("<p style='color:red'>Password and confirm pasword must be same</p>")
        return
    }

    if(!nameRegex.test(name)){
        $("#response").html("<p style='color:red'>Please Enter correct and full name.</p>")
        return
    }

    if(!emailRegex.test(email)){
        $("#response").html("<p style='color:red'>Please enter correct email</p>")
        return
    }

    if(!usernameRegex.test(username)){
        $("#response").html("<p style='color:red'>Start with @ and use one number and always use small letter</p>")
        return
    }

    if(!passwordRegex.test(password)){
        $("#response").html("<p style='color:red'>write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.</p>")
        return
    }

    $.ajax({
        url : subject ? "/account/signup/teacher/" : "/account/signup/student/" ,
        method : "POST",
        data : {
            name : name,
            username : username,
            email : email,
            password : password,
            confirm_password : confirm_password,
            subject : subject,
            csrfmiddlewaretoken: csrf_token

        },
        success : function(response){
            console.log("✅ Server response:", response);
            if(response.success){
                $("#response").text(response.message)
            }else{
                 $("#response").text("Please try again")
            }
        },

        error: function(err){
            console.error("AJAX error:", err);
            $("#response").html("<p style='color:red'>Something went wrong! Please try again.</p>");
        }

    })

  })


})

