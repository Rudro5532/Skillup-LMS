$(document).ready(function () {
    console.log("Jquery ready")
    $('input[name="role"]').change(function () {
      let role = $('input[name="role"]:checked').val();
      if (role === "student") {
        $("#studentFields").show();
        $("#instructorFields").hide();
      } else {
        $("#studentFields").hide();
        $("#instructorFields").show();
      }
    });
});

