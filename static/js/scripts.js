const nameRegex = /^([A-Za-z]{2,})(\s[A-Za-z]{2,})$/;
const usernameRegex = /^@([a-z0-9_]{3,})$/;
const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}/;


$(document).ready(function(){
  console.log("LMS dom is ready Teacher")

  //registration ajax
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

  // for manage courses
  $("#blog_submit").click(function(e){
    e.preventDefault();

    const course_name = $("#course_name").val();
    const category = $("#category").val();
    const teacher = $("#teacher").val();
    const slug = $("#slug").val();
    const price = $("#price").val();
    const description = $("#description").val();
    const image = $("#image")[0].files[0];
    const meterial = $("#meterial")[0].files[0];
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    const course_slug = $("#course_slug").val();

    console.log("Image File:", image);
    console.log("Meterial File:", meterial);

    if (!course_name || !category || !teacher || !slug || !price || !description) {
        $("#post_response").html(`<div class="alert alert-danger">All fields are required</div>`);
        return;
    }


    const form_data = new FormData();
    form_data.append("title", course_name);
    form_data.append("category", category);
    form_data.append("teacher", teacher);
    form_data.append("description", description);
    form_data.append("slug", slug);
    form_data.append("price", price);
    if (image && meterial) {
        form_data.append("image", image);
        form_data.append("meterial", meterial);
    }
    $("#loader-overlay").show();

    $.ajax({
        url : course_slug ?  `/account/update_course/${course_slug}/` : "/account/teacher_dashboard/",
        method : "POST",
        data: form_data,
        processData: false, 
        contentType: false,
        headers : {
            "X-CSRFToken": csrf_token
        },
        success : function(response){
            console.log("✅ Success:", response);
            if(response.success){
                $("#post_response").html(`<div class="alert alert-success">${response.message}</div>`);
                setTimeout(() => {
                alert(`${response.message}`)
                console.log(response.message)
                window.location.href = response.redirect_url;
                }, 2000)
              
            } else {
                $("#loader-overlay").hide();
                $("#post_response").html(`<div class="alert alert-success">Please Try again</div>`);
            }
        },
        error: function(err){
            console.error("❌ Error:", err);
            $("#post_response").html(`<div class="alert alert-success">Something went wrong</div>`);
        },
        complete: function(xhr, status) {
            console.log("Complete. Status:", status);
            console.log("Raw Response:", xhr.responseText);
        }
    });


  });

  // manage course video
  $("#video_up").click(function(e){
    e.preventDefault()

    const title = $("#title").val()
    const course = $("#course").val()
    const video_file = $("#video_file")[0].files[0]
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    const video_id = $("#video_id").val();
    $("#loader-overlay").show();

    const fromData = new FormData()

    fromData.append("title", title)
    fromData.append("course_name", course)
    
    if(video_file){
        fromData.append("video_file", video_file)
    }

    $.ajax({
        url : video_id ? `/account/edit_video/${video_id}/` : "/account/course_video/",
        type : "POST",
        data : fromData,
        processData : false,
        contentType : false,
        headers : {
            "X-CSRFToken": csrf_token
        },
        success : function(response){
            if(response.success){
                alert(`${response.message}`)
                setTimeout(() => {
                window.location.href = response.redirect_url;
                $("#message .alert").fadeOut("slow", function(){
                    $(this).remove(); 
                });
                }, 2000)
            }else{
                $("#loader-overlay").hide();
                $("#message").html(`<div class="alert alert-alert">${response.message}</div>`);
                setTimeout(() => {
                $("#message .alert").fadeOut("slow", function(){
                    $(this).remove(); 
                });
                }, 2000)
            }
        },

        error : function(err){
            $("#loader-overlay").hide();
            $("#message").html(`<div class="alert alert-alert">${err}</div>`);
            setTimeout(() => {
                $("#message .alert").fadeOut("slow", function(){
                    $(this).remove(); 
                });
            }, 2000)
           
        }
    })
  })

 // login ajax
 $("#login-btn").click(function(e){
    e.preventDefault()

    const email = $("#email").val()
    const password = $("#password").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $("#loader-overlay").show();
    

    $.ajax({
        url : "/account/user_login/",
        type : "POST",
        data : {
            email : email,
            password : password,
            csrfmiddlewaretoken : csrf_token
        },
       
        success : function(response){
            if(response.success){
                $("#message").html(
                    `<div class="alert alert-success">${response.message}</div>`
                )
                setTimeout(() => {
                alert(`${response.message}`)
                window.location.href = response.redirect_url;
                }, 2000) 
            }
            else{
                $("#loader-overlay").hide();
                $("#message").html(
                        `<div class="alert alert-danger">Credential Invalid</div>`
                )
            }

        },

        error : function(err){
            $("#loader-overlay").hide();
            $("#message").html(
                    `<div class="alert alert-danger">Something went wrong</div>`
            )
        }
    })

})

 // payment gateway
$("#enroll").click(function(e) {
    e.preventDefault();

    const amount = $("#amount").val();
    const course_id = $("#course_id").val();
    if (!amount || amount <= 0) {
        alert('Please enter a valid amount.');
        return;
    }

    $.ajax({
        url: "/payment/course_payment/",
        type: "POST",
        data: {
            amount: amount,
            course_id: course_id,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            console.log("Razorpay Response:", data);
            const options = {
                key: data.key,
                amount: data.amount,
                order_id: data.order_id,
                currency: 'INR',
                name: data.name,
                description: data.description,

                handler: function(response) {
                    alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
                    console.log("Payment Response: ", response);

                    $.ajax({
                        url: "/payment/verify_payment/",
                        type: "POST",
                        data: {
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature,
                            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                        },
                        success: function(verificationResponse) {
                            if (verificationResponse.success) {
                                alert("Payment verified successfully!");
                            } else {
                                alert("Payment verification failed: " + verificationResponse.error);
                            }
                        },
                        error: function(error) {
                            alert("Error verifying payment.");
                            console.error(error);
                        }
                    });
                }
            };

            const razorpay = new Razorpay(options);
            razorpay.open();
        },
        error: function(error) {
            console.error('Order creation error:', error);
            alert('Error creating order.');
        }
    });
});

 // edit profile
$("#editProfile").click(function(e){
    e.preventDefault()
    const username = $("#username").val()
    const fullname = $("#fullname").val()
    const profile_image = $("#profile_image")[0].files[0];
    const csrf_token = $("input[name='csrfmiddlewaretoken']").val();

    const form_data = new FormData()

    form_data.append("username", username)
    form_data.append("fullname", fullname)
    form_data.append("csrf_token", csrf_token)
    if (profile_image) {
        form_data.append("profile_image", profile_image);
    }
    $("#loader-overlay").show();

    $.ajax({
        url : "/account/edit_profile/",
        type : "POST",
        data : form_data,
        processData: false,              
        contentType: false,              
        headers: {
            "X-CSRFToken": csrf_token    
        },
        success : function(response){
            if(response.success){
                $("#post_response").html(`<div class="alert alert-success">${response.message}</div>`);
                setTimeout(() => {
                alert(`${response.message}`)
                console.log(response.message)
                window.location.href = response.redirect_url;
                }, 2000)
            }else{
                $("#loader-overlay").hide();
                $("#message").html(`<div class="alert alert-danger">${response.message}</div>`);

            } 
        },
        error : function(err){
            console.error("❌ Error:", err);
            $("#message").html(`<div class="alert alert-success">Something went wrong</div>`);
        }

    })

})

// change password
$("#updatePassword").click(function(e){
    e.preventDefault

    const currentPassword = $("#currentPassword").val()
    const newPassword = $("#newPassword").val()
    const confirmPassword = $("#confirmPassword").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    
    // if(!passwordRegex.test(newPassword)){
    //     $("#message").html("<p style='color:red'>write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.</p>")
    //     return
    // }
    $("#loader-overlay").show();


    $.ajax({
        url : "/account/change_password/",
        type : "POST",
        data : {
            currentPassword : currentPassword,
            confirmPassword : confirmPassword,
            newPassword : newPassword,
            csrfmiddlewaretoken : csrf_token
        },
        success : function(response){
            if(response.success){
                alert(`${response.message}`)
                setTimeout(()=>{
                    window.location.href = response.redirect_url
                },3000)
            }else{
                $("#loader-overlay").hide();
                $("#message").html(`<div class="alert alert-danger">${response.message}</div>`);
            }
        },
        error : function(err){
            $("#message").html(`<div class="alert alert-danger">${err}</div>`);
        }
    })


})

// forgot Password
$("#otp").click(function(e){
    e.preventDefault()
    const email = $("#email").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $("#loader-overlay").show();

    $.ajax({
        url : "/account/forgot_password/",
        type : "POST",
        data : {
            email : email,
            csrfmiddlewaretoken : csrf_token
        },
        success : function(response){
            if(response.success){
                alert(response.message)
               setTimeout(()=>{
                    window.location.href = response.redirect_url
                },2000)
            }else{
                $("#loader-overlay").hide();
                $("#message").html(`<div class="alert alert-danger">${response.message}</div>`)
            }
        },
        error : function(err){
            $("#loader-overlay").hide();
            $("#message").html(`<div class="alert alert-danger">${err}</div>`)
        }
    })
})

// reset pasword
$("#reset_password").click(function(e){
    e.preventDefault()
    const otp = $("#otp").val()
    const new_password = $("#new_password").val()
    const confirm_new_password = $("#confirm_new_password").val()
    csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $("#loader-overlay").show();


    $.ajax({
        url : "/account/reset_password/",
        type : "POST",
        data :{
            otp : otp,
            new_password : new_password,
            confirm_new_password : confirm_new_password,
            csrfmiddlewaretoken : csrf_token
        },
        success : function(response){
            if(response.success){
                alert(response.message)
               setTimeout(()=>{
                    window.location.href = response.redirect_url
                },2000)
            }
            else{
                $("#loader-overlay").hide();
                $("#message").html(`<div class="alert alert-danger">${response.message}</div>`)
            }
        },
        error : function(err){
            $("#loader-overlay").hide();
            $("#message").html(`<div class="alert alert-danger">${err}</div>`)
        }
    })
})

// student review
$("#review").click(function(e){
    e.preventDefault()
    const comment = $("#comment").val()
    const slug = $(this).data("slug"); 
    csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url : `/course/get_single_course/${slug}/`,
        type : "POST",
        data : {
            comment : comment,
            csrfmiddlewaretoken : csrf_token
        },
        success : function(response){
            if(response.success){
                $("#message").html(`<div class="alert alert-success">${response.message}</div>`);
                setTimeout(()=>{
                    window.location.href = response.redirect_url
                },3000)
            }else{
                $("#message").html(`<div class="alert alert-alert">${response.message}</div>`);
            }

            setTimeout(function(){
                $("#message").fadeOut("slow", function(){
                    $(this).html("").show(); 
                });
            }, 2000)
        },
        error : function(err){
            $("#message").html(`<div class="alert alert-success">${err}</div>`);
        }
    })
})

// send message
$("#sendMessage").click(function(e){
    const name = $("#name").val()
    const email = $("#email").val()
    const message = $("#message").val()
    csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url : "/contact_us/",
        type : "POST",
        data : {
            name : name,
            email : email,
            message : message,
            csrfmiddlewaretoken : csrf_token
        },
        success : function(response){
            if(response.success){
                $("#store").html(`<div class="alert alert-success">${response.message}</div>`);
            }else{
                $("#store").html(`<div class="alert alert-alert">${response.message}</div>`);
            }

            setTimeout(function(){
                $("#store").fadeOut("slow", function(){
                    $(this).html("").show(); 
                });
            }, 2000)
        },
        error : function(err){
            $("#message").html(`<div class="alert alert-alert">${err}</div>`);
        }
    })
})

// admin registration
$("#admin_reg").click(function(e){
    e.preventDefault()
    const username = $("#username").val()
    const name = $("#name").val()
    const email = $("#email").val()
    const password = $("#password").val()
    const confirm_password = $("#confirm_password").val()
    const csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $("#loader-overlay").show();

    $.ajax({
        url : "/account/signup/lms_admin/",
        type : "POST",
        data : {
            username:username,
            name : name,
            email : email,
            password : password,
            confirm_password : confirm_password,
            csrfmiddlewaretoken : csrf_token
        },

        success : function(response){
            if(response.success){
                $("#message").html(
                    `<div class="alert alert-success" id="alert-box">${response.message}</div>`
                ) 
            }
            else{
                $("#loader-overlay").hide();
                $("#message").html(
                    `<div class="alert alert-danger" id="alert-box">${response.message}</div>`
                )
            }

            setTimeout(function() {
                $("#alert-box").fadeOut("slow", function() {
                    $(this).remove();
                });
            }, 5000);

        },

        error : function(err){
            $("#message").html(
                `<div class="alert alert-danger" id="alert-box">${err}</div>`
            )
            setTimeout(function() {
                $("#alert-box").fadeOut("slow", function() {
                    $(this).remove();
                });
            }, 5000);
        }
    })

})


// delete course
$(document).on("click", ".event-delete-btn", function () {
    const course_slug = $(this).data("slug");

    if (!confirm("Are you sure you want to delete this course?")) {
        return;
    }

    $.ajax({
        url: `/account/delete_course/${course_slug}/`,
        type: "POST",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            $("#post_response").html(`<div class="alert alert-success">${response.message}</div>`)
            .fadeIn().delay(2000).fadeOut();

            setTimeout(function() {
                window.location.href = response.redirect_url;
            }, 2000);
        },
        error: function (xhr) {
            let error = xhr.responseJSON?.error || "Something went wrong.";
            $('#post_response').html('<div class="alert alert-danger">' + error + '</div>');
            }
    });
});

// edit course
$(document).on("click", ".event-edit-btn", function (){
    const courseId = $(this).data("id");
    const title = $(this).data("title");
    const category = $(this).data("category");
    const teacher = $(this).data("teacher");
    const description = $(this).data("description");
    const slug = $(this).data("slug");
    const price = $(this).data("price");
    const course_slug = $(this).data("course_slug");

    $("#course_name").val(title);
    $("#category").val(category);
    $("#teacher").val(teacher);
    $("#description").val(description);
    $("#slug").val(slug);
    $("#price").val(price);
    $("#course_slug").val(course_slug); 

})

// edit course video
$(document).on("click", ".event-edit-video", function(){
    const video_id = $(this).data("video_id")
    const title = $(this).data("title")
    const course_id = $(this).data("course")

    $("#video_id").val(video_id)
    $("#title").val(title)
    $("#course").val(course_id)
})



});
// end line of document




