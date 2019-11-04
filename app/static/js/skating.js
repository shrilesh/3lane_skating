var socket = io.connect('http://'+ document.domain + ':' + location.port + '/display');

socket.on('connect', function() {
    console.log("connected");
})

socket.on('message', function(data) {
    console.log(data);
    data = JSON.parse(data);
    if (data.message_type == "timings"){
        if (data.result == "start"){
            startTimer(data.lane_no);
        }else{
            stopTimer(data.lane_no);
        }
    }
})

$(document).ready(function(){
	$('#align_btn').show();
    $('#initialize_btn').hide();
    $('#reset_btn').hide();

    $('#l1_start_correct').hide();
    $('#l2_start_correct').hide();
    $('#l3_start_correct').hide();

    $('#l1_stop_correct').hide();
    $('#l2_stop_correct').hide();
    $('#l3_stop_correct').hide();

});

// global object
T = {
    "1" : {}, 
    "2" : {}, 
    "3" : {}
};


function displayTimer(lane_no) {
	// initilized all local variables:
	var hours='00', minutes='00',
	miliseconds=0, seconds='00',
	time = '',
	timeNow = new Date().getTime(); // timestamp (miliseconds)

	T[lane_no].difference = timeNow - T[lane_no].timerStarted;

	// milliseconds
	if(T[lane_no].difference > 10) {
		miliseconds = Math.floor(T[lane_no].difference % 1000);
		if(miliseconds < 10) {
			miliseconds = '00'+String(miliseconds);
		}
		else if (miliseconds < 100) {
			miliseconds = '0'+String(miliseconds);
		};
	}
	// seconds
	if(T[lane_no].difference > 1000) {
		seconds = Math.floor(T[lane_no].difference / 1000);
		if (seconds >= 60) {
			seconds = seconds % 60;
		}
		if(seconds < 10) {
			seconds = '0'+String(seconds);
		}
	}

	// minutes
	if(T[lane_no].difference > 60000) {
		minutes = Math.floor(T[lane_no].difference/60000);
		if (minutes > 60) {
			minutes = minutes % 60;
		}
		if(minutes < 10) {
			minutes = '0'+String(minutes);
		}
	}

	// hours
	if(T[lane_no].difference > 3600000) {
		hours = Math.floor(T[lane_no].difference/3600000);
		// if (hours > 24) {
		//  hours = hours % 24;
		// }
		if(hours < 10) {
			hours = '0'+String(hours);
		}
	}

	// time  =  hours   + ':'
	time += minutes + ':'
	time += seconds + ':'
    time += miliseconds;
    
    var lane_div = '#lane_'+lane_no+'_time'
	$(lane_div).text(time);

	T[lane_no].lastTime = timeNow;
}

function startTimer(lane_no) {
	// save start time
	T[lane_no].timerStarted = new Date().getTime()
	console.log('T.timerStarted: '+T[lane_no].timerStarted)

	if (T[lane_no].difference > 0) {
		T[lane_no].timerStarted = T[lane_no].timerStarted - T[lane_no].difference
	}
	// update timer periodically
	T[lane_no].timerInterval = setInterval(function() {
		displayTimer(lane_no)
	}, 0);

}

function stopTimer(lane_no) {
	clearInterval(T[lane_no].timerInterval); // reset updating the timer
}


$("#align_btn").click(function() {
    url_name = 'http://'+ document.domain + ':' + location.port + '/device/align'
	$.ajax({
		url: url_name,
		type: 'GET',
		success: function(response) {	

			if(response.status == "success")
			{

                for (var key in response) {
                    if (key != "status"){
                        $('#'+ key.toString() + '_correct').show()
                        $('#'+ key.toString() + '_incorrect').hide()
                    }
                }
                
				$('#align_btn').hide();
                $('#initialize_btn').show();
                
			}else{

                $('#align_btn').show();
                $('#initialize_btn').hide();

                for (var key in response) {
                    if (key != "status"){
                        if (response[key] == 1){
                            $('#'+ key.toString() + '_correct').show()
                            $('#'+ key.toString() + '_incorrect').hide()
                        }else{
                            $('#'+ key.toString() + '_correct').hide()
                            $('#'+ key.toString() + '_incorrect').show()
                        }
                    }
                }
            }
		},
		failure: function(response) {
			console.log("Inside Failure");
			console.log(response);
			
		},
		error: function(response) {
			console.log("Inside Error");
			console.log(response);
			
		}
	});
});

$("#initialize_btn").click(function() {
    url_name = 'http://'+ document.domain + ':' + location.port + '/device/initialize'
    $.ajax({
		url: url_name,
		type: 'GET',
		success: function(response) {	
			if(response.status == "success")
			{
                $('#initialize_btn').hide();
                $('#reset_btn').show();
			}
		},
		failure: function(response) {
			console.log("Inside Failure");
			console.log(response);
			
		},
		error: function(response) {
			console.log("Inside Error");
			console.log(response);
			
		}
    });

});

$("#reset_btn").click(function(){
    url_name = 'http://'+ document.domain + ':' + location.port + '/device/reset'
	$.ajax({
		url: url_name,
		type: 'GET',
		success: function(response) {	

			if(response.status == "success")
			{
				result = '00:00:000';
				$("#lane_1_time").text(result);
				$("#lane_2_time").text(result);
				$("#lane_3_time").text(result);
                $('#reset_btn').hide();
                $('#align_btn').show();
            }
		},
		failure: function(response) {
			console.log("Inside Failure");
			console.log(response);
			
		},
		error: function(response) {
			console.log("Inside Error");
			console.log(response);
			
		}
	});
})