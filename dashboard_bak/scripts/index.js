// Updating Row func

$(document).ready(function() {
	$('.rowSubmit').bind('submit', function(e) {
		var formId = $(this).attr('id')
		var data = $(document.getElementById(formId)).serialize();
		console.log("Submitting... "+formId)
		$.ajax({
			type: "POST",
			url: 'api/updateAuditScore.php',
			data: data,
			success: function(data) {
				location.reload();
			}
		});
		e.preventDefault();
	})
});

// $("#rowSubmit").submit(function(e) {

//     var url = "api/updateAuditScore.php"; // the script where you handle the form input.

//     $.ajax({
//            type: "GET",
//            url: url,
//            data: $("#rowSubmit").serialize(), // serializes the form's elements.
//            success: function(data) {
//        			//location.reload();
//            }
//          });

//     e.preventDefault(); // avoid to execute the actual submit of the form.
//});