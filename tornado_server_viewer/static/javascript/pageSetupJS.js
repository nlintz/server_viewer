jQuery(function($){

	var requestToken;
	var appId;

	setTimeout(
		function(){
			$('body').removeClass('hidden')
		}, 50)

	$('.dropbox-login-target').click(function(){
		$.ajax({
			url: "/oauth_request_token",
			// success: window.open(, "Dropbox Login")
			success: function(data){
				window.open(data.split(' ')[0]);
				request_token = data.split(' ')[1];
				app_info = data.split(' ')[2];

				

			}
		})

	})

	$('.dropbox-access-target').click(function() {
		$.ajax({

					url: "/oauth_access_token",
					data: {"request_token":request_token, "app_info":app_info}
				})
	})

	// filterByRegex('^Waka')





})