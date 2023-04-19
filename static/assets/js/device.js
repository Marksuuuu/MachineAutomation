$(document).ready(function () {
    var timerInterval;
    function fetchAndCreateCards() {
        $.ajax({
            url: '/card_details',
            method: 'GET',
            success: function (data) {
                // Loop through the data and create a card element for each item
                $.each(data, function (index, item) {
                    var machine_status = item.status;
                    var body = '';
                    var text_color = '';

                    if (machine_status == "STARTED") {
                        stat = 'bg-success';
                        text_color = 'success'
                    } else if (machine_status == 'STOP') {
                        stat = 'bg-danger';
                        text_color = 'danger'
                    } else if (machine_status == 'IDLE') {
                        stat = 'bg-primary'
                        text_color = 'primary'
                    } else {
                        stat = ''
                    }

                    // Create a unique ID for the timer based on the item ID
                    var timerID = 'timer-' + item.id;
                    var date_here = item.end_time;

                    body += '<div class="col-lg-4"><div class="card card-margin ' + stat + '">'
                        + '<div class="card-header no-border">'
                        + '<h5 class="card-title text-dark" style="text-transform:uppercase;" >' + item.current_path + '</h5>'
                        + '</div>'
                        + '<div class="card-body pt-0">'
                        + '<div class="widget-49">'
                        + '<div class="widget-49-title-wrapper">'
                        + '<div class="widget-49-date-primary">'
                        + '<span class="widget-49-date-day text-' + text_color + '">' + item.id + '</span>'
                        + '</div>'
                        + '<div class="widget-49-meeting-info">'
                        + '<span class="widget-49-pro-title text-dark">' + item.date_time + '</span>'
                        + '<span class="widget-49-meeting-time text-dark">' + item.status + '</span>'
                        + '</div>'
                        + '</div>'
                        + '<div class="radial-timer">'
                        + '<div class="radial-timer-bar"></div>'
                        + '<div class="radial-timer-inner">'
                        + '<div class="radial-timer-seconds text-' + text_color + '" id="' + timerID + '">00</div>'
                        + '<div class="radial-timer-label text-' + text_color + '">Seconds</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>';

                    // Add the card to the container element
                    $('.device_row').append(body);

                    // Start the timer if the status is 'STARTED'
                    if (machine_status == 'IDLE') {
                        startTimer(timerID, item.end_time, date_here);
                    }
                    else if(machine_status == 'STOP'){
                        pauseTimer();
                    }else{

                    }
                });
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log('Error fetching data from PostgreSQL');
            }
        });
    }

    fetchAndCreateCards();
    function startTimer(timerID, startTime, date_here) {
        var timerElement = $('#' + timerID);
        // var startTime = /*$('#endDate').val();*/ '2023-04-19 12:30:21'
        
        var endDate = new Date(date_here);
        console.log(endDate)
        var dateObject = new Date(endDate);
        var countDownDate = new Date(dateObject).getTime();
        var timerInterval = setInterval(function () {
            var now = new Date().getTime();

            // Find the distance between now and the count down date
            var distance = countDownDate - now;

            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            timerElement.find('.radial-timer-seconds').text(pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2));
            var percentage = distance * 100 / 3600; // calculate the percentage of elapsed time
            timerElement.siblings('.radial-timer-bar').css('transform', 'rotate(' + percentage + 'deg)'); // update the radial-timer-bar
            timerElement.html(pad(pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2)))
            console.log(pad(pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2)))
        }, 1000);
        console.log(timerInterval)
    }
    function pauseTimer(timerID) {
        clearInterval(timerInterval);
  
        // get the elapsed time
        var timerElement = $('#' + timerID);
        var timerValue = timerElement.text();
        var elapsedSeconds = (parseInt(timerValue.slice(0, 2)) * 60 * 60) + (parseInt(timerValue.slice(3, 5)) * 60) + parseInt(timerValue.slice(6, 8));
        var elapsedTime = elapsedSeconds * 1000;
  
        // update the database with the paused time and elapsed time
        var pauseTime = new Date().toISOString().slice(0, 19).replace('T', ' ');
        // CODE TO SAVE PAUSE TIME AND ELAPSED TIME TO DATABASE
        console.log('pause',timerInterval)
  
    }
    function pad(num, size) {
        var s = "" + num;
        return s.substr(s.length - size);
    }
})

// import json
// from flask import Flask, request

// app = Flask(__name__)

// @app.route('/save_pause', methods=['POST'])
// def save_pause():
//     data = json.loads(request.data)
//     timerID = data['timerID']
//     pauseTime = data['pauseTime']
//     elapsedTime = data['elapsedTime']

//     # establish connection to database
//     conn = psycopg2.connect(database="your_database_name", user="your_username", password="your_password", host="your_host", port="your_port")
//     cur = conn.cursor()

//     # insert data into database
//     cur.execute("INSERT INTO paused_time (timer_id, pause_time, elapsed_time) VALUES (%s, %s, %s)", (timerID, pauseTime, elapsedTime))
//     conn.commit()

//     # close connection to database
//     cur.close()
//     conn.close()

//     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

// function pauseTimer(timerID) {
//     clearInterval(timerInterval);

//     // get the elapsed time
//     var timerElement = $('#' + timerID);
//     var timerValue = timerElement.text();
//     var elapsedSeconds = (parseInt(timerValue.slice(0, 2)) * 60 * 60) + (parseInt(timerValue.slice(3, 5)) * 60) + parseInt(timerValue.slice(6, 8));
//     var elapsedTime = elapsedSeconds * 1000;

//     // update the database with the paused time and elapsed time
//     var pauseTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

//     // send AJAX request to Flask server to save data
//     $.ajax({
//         type: 'POST',
//         url: '/save_pause',
//         data: JSON.stringify({ 'timerID': timerID, 'pauseTime': pauseTime, 'elapsedTime': elapsedTime }),
//         contentType: 'application/json',
//         success: function (response) {
//             console.log(response);
//         },
//         error: function (error) {
//             console.log(error);
//         }
//     });
// }



