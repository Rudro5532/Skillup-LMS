const nameRegex = /^([A-Za-z]{2,})(\s[A-Za-z]{2,})$/;
const usernameRegex = /^@([a-z0-9_]{3,})$/;
const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}/;

// student registration ajax
$(document).ready(function(){
  console.log("LMS dom is ready student")

  $("#student_register").click(function(event){
    event.preventDefault()
    console.log("We ar inside in ready function")

    const username = $("#username").val()
    const name = $("#name").val()
    const email = $("#email").val()
    const password = $("#password").val()
    const confirm_password = $("#confirm_password").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();

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
        $("#responser").html("<p style='color:red'>write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.</p>")
        return
    }

    $.ajax({
        url : "/account/signup/",
        method : "POST",
        data : {
            name : name,
            username : username,
            email : email,
            password : password,
            confirm_password : confirm_password,
            csrfmiddlewaretoken: csrf_token

        },
        success : function(response){
            if(response.success){
                $("#response").text(response.message)
            }else{
                 $("#response").text("Please try again")
            }
        },

        error : function(err){
            $("#response").err
        }
    })

  })

})

// teacher registration ajax
$(document).ready(function(){
  console.log("LMS dom is ready Teacher")

  $("#teacher_register").click(function(event){
    event.preventDefault()
    console.log("We ar inside in ready function")

    const username = $("#username").val()
    const name = $("#name").val()
    const email = $("#email").val()
    const password = $("#password").val()
    const confirm_password = $("#confirm_password").val()
    const subject = $("#subject").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();


    if(!name || !username || !email || !password || !subject){
        $("#response").html("<p style='color:red'>All field ar requeried</p>")
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
        url : "/account/teacher_signup/",
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
            if(response.success){
                $("#response").text(response.message)
            }else{
                 $("#response").text("Please try again")
            }
        },

        error : function(err){
            $("#response").err
        }
    })

  })


})

