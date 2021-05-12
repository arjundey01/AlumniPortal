var user_input
var search_icon 
var  accounts_div 
const endpoint = '/accounts/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			console.log("acs")
			// fade out the accounts_div, then:
			accounts_div.fadeTo('slow', 0).promise().then(() => {
				// replace the HTML contents
				accounts_div.html(response['html_from_view'])
				// fade-in the div with new contents
				accounts_div.fadeTo('slow', 1)
				// stop animating search icon
				search_icon.removeClass('blink')
			})
		})
}
$(document).ready(function() {
	 user_input = $("#user-input")
	 search_icon = $('#search-icon')
	 accounts_div = $('#replaceable-content')
	user_input.on('keyup', function () {
		console.log("fsdf")
	
		const request_parameters = {
			q: $(this).val() // value of user_input: the HTML element with ID user-input
		}
	
		// start animating the search icon with the CSS class
		search_icon.addClass('blink')
	
		// if scheduled_function is NOT false, cancel the execution of the function
		if (scheduled_function) {
			clearTimeout(scheduled_function)
		}
	
		// setTimeout returns the ID of the function to be executed
		scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
	})
    
});


