$(document).ready(function () {
    function fetchAndCreateCards() {
        $.ajax({
            url: '/card_details_die_prep',
            method: 'GET',
            success: function (data) {
                // Loop through the data and create a card element for each item
                $.each(data, function (index, item) {
                    var machine_status = item.status;
                    var body = '';
                    var text_color = '';
                    if (machine_status == "CONNECTED") {
                        stat = 'bg-success';
                        text_color = 'success'
                    } else if (machine_status == 'DISCONNECTED') {
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
                    console.log(item.operator, item.port, )
                    // var machine_id = item.id
                    // var date_here = item.end_time;
                    // var duration = item.duration;

                    // Retrieve start time and elapsed time from local storage if available
                    // var storedData = JSON.parse(localStorage.getItem(timerID));
                    // var startTime = storedData ? storedData.startTime : null;
                    // var elapsedTime = storedData ? storedData.elapsedTime : 0;

                    body += '<div class="col-lg-4"><div class="card card-margin ' + stat + '">'
                        + '<div class="card-header no-border" style="font-weight:bold;">'
                        + '<span class="card-title text-dark" style="text-transform:uppercase; margin-right:220px;">' + item.port + '</span>'
                        + '&nbsp; &nbsp;  &nbsp;'
                        + '<span class="card-title text-dark" style="text-transform:uppercase;" >' + item.controller_name + '</span>'
                        + '</div>'
                        + '<div class="card-body pt-0">'
                        + '<div class="widget-49">'
                        + '<div class="widget-49-title-wrapper">'
                        + '<div class="widget-49-date-primary">'
                        + '<span class="widget-49-date-day text-' + text_color + '">' + item.item_id + '</span>'
                        + '</div>'
                        + '<div class="widget-49-meeting-info">'
                        + '<span class="widget-49-pro-title text-dark">' + item.operation_code + '</span>'
                        + '<span class="widget-49-meeting-time text-dark">' + item.status + '</span>'
                        + '</div>'
                        + '</div>'
                        + '<div class="radial-timer">'
                        + '<div class="radial-timer-bar"></div>'
                        + '<div class="radial-timer-inner">'
                        + '<div class="radial-timer-seconds text-' + text_color + '" id="' + timerID + '">00</div>'
                        + '<div class="radial-timer-label text-' + text_color + '" id="sec">Seconds</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '<dl class="widget-49-pro-title text-dark">'
                        + '<dt>OPERATOR</dt>'
                        + '<dd>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-' + item.operator + '</dd>'
                        + '<dt>ASSIGNED GL</dt>'
                        + '<dd>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-' + item.assigned_gl + '</dd>'
                        + '<dt>AREA</dt>'
                        + '<dd>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-' + item.area + '</dd>'
                        + '<dt>OPERATION</dt>'
                        + '<dd>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-' + item.operation + '</dd>'
                        + '</dl>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>'
                        + '</div>';

                    // Add the card to the container element
                    $('.device_row').append(body);

                    // Start the timer if the status is 'STARTED'
                    if (machine_status == 'STOP') {
                        // var timer = startTimer(timerID, duration, startTime, elapsedTime);
                        // pauseTimer(timerID, timer)
                    }
                    if (machine_status == 'IDLE') {
                        // do nothing
                    }
                    else if (machine_status == 'STOP') {

                    } else if (machine_status == 'PAUSE') {
                        // pauseTimer(timerID, timer)
                    }
                });
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log('Error fetching data from PostgreSQL');
            }
        });
    }


    // // Other initialization code
    fetchAndCreateCards();
    setTimeout(function () {
        window.location.reload();
    }, 100000);

    // var timer = null;
    // var startTime = null;
    // var captures = [];
    // var elapsedTime = 0;
    // var duration = null;

    // // Load saved data from storage
    // var savedData = JSON.parse(localStorage.getItem("stopwatchData"));
    // if (savedData) {
    //     captures = savedData.captures;
    //     elapsedTime = savedData.elapsedTime;
    //     duration = savedData.duration;
    // }

    // function saveData() {
    //     // Save data to storage
    //     localStorage.setItem("stopwatchData", JSON.stringify({
    //         captures: captures,
    //         elapsedTime: elapsedTime,
    //         duration: duration
    //     }));   
    // }

    // function formatTime(time) {
    //     var hours = Math.floor(time / 3600);
    //     var minutes = Math.floor((time % 3600) / 60);
    //     var seconds = Math.floor(time % 60);
    //     return (hours < 10 ? "0" : "") + hours + ":" +
    //         (minutes < 10 ? "0" : "") + minutes + ":" +
    //         (seconds < 10 ? "0" : "") + seconds;
    // }

    // function updateTimer() {
    //     var currentTime = Date.now();
    //     elapsedTime += currentTime - startTime;
    //     startTime = currentTime;
    //     var formattedTime = formatTime(Math.floor(elapsedTime / 1000));
    //     $("#timer").text(formattedTime);
    //     if (duration && elapsedTime >= duration * 1000) {
    //         clearInterval(timer);
    //         timer = null;
    //         $("#message").text("Time's up!");
    //     }
    //     saveData(); // Save data after each update
    // }

    // function startTimer(timerID, duration) {
    //     var startTime = Date.now();
    //     console.log('duration', duration)
    //     var timer = setInterval(function () {
    //         var elapsedTime = Math.floor((Date.now() - startTime) / 1000);

    //         var seconds = elapsedTime % 60;
    //         var minutes = Math.floor(elapsedTime / 60) % 60;
    //         var hours = Math.floor(elapsedTime / 3600);
    //         var formattedTime =
    //             (minutes < 10 ? "0" + minutes : minutes) + ":" +
    //             (seconds < 10 ? "0" + seconds : seconds);
    //         $("#" + timerID).text(formattedTime);
    //         if (duration && elapsedTime >= duration) {
    //             // clearInterval(timer);
    //             // $("#" + timerID).text("Times UP!");
    //             // $("#sec").text("");
    //         }
    //         if (duration && elapsedTime == duration) {
    //             console.log('Reached', duration)
    //             saveData(); // Save data after each tick
    //         }

    //     }, 1000);
    //     console.log(timer)
    //     return timer;
    // }

    // function pauseTimer(timerID, timer) {
    //     // clearInterval(timer);
    //     var capturedTime = $("#" + timerID).text();
    //     captures.push(capturedTime);
    //     console.log(capturedTime)
    //     $("#captures").append("<div>" + capturedTime + "</div>");
    //     saveData(); // Save data after each capture
    // }

    // function stopTimer(timerID, timer) {
    //     clearInterval(timer);
    //     var capturedTime = $("#" + timerID).text();
    //     captures.push(capturedTime);
    //     $("#" + timerID).text("00:00");
    //     $("#captures").append("<div>" + capturedTime + "</div>");
    //     saveData(); // Save data after stopping
    // }

    // function resetTimer() {
    //     duration = null;
    //     elapsedTime = 0;
    //     $("#" + timerID).text("00:00");
    //     $("#duration").val("");
    //     $("#captures").empty();
    //     $("#message").text("");
    // }


    // function pad(num, size) {
    //     var s = "" + num;
    //     return s.substr(s.length - size);
    // }
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


// }



