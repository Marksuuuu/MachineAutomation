$(function() {
    var startTime;
    var intervalId;

    $.ajax({
        url: '/get_start_time',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            startTime = new Date(data.start_time);
            startTimer();
        }
    });

    $('.radial-timer-pause').click(function() {
        pauseTimer();
    });

    function startTimer() {
        intervalId = setInterval(updateTimer, 1000);

        $('.radial-timer-bar').click(function() {
            stopTimer();
        });
    }

    function pauseTimer() {
        clearInterval(intervalId);

        $.ajax({
            url: '/pause_timer',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({ pause_time: new Date() }),
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                alert('Timer paused');
            }
        });
    }

    function stopTimer() {
        clearInterval(intervalId);

        $.ajax({
            url: '/stop_timer',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({ stop_time: new Date() }),
            contentType: 'application/json; charset=utf-8',
            success: function(data) {
                alert('Timer stopped');
            },
            error: function() {
                alert('Error stopping timer');
            }
        });
    }

    function updateTimer() {
        $.ajax({
            url: '/get_time_elapsed',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                startTime = new Date(data.start_time);
                var pauseTime = new Date(data.pause_time);
                var now = new Date();
                var difference = now.getTime() - startTime.getTime();
                var pauseDuration = pauseTime.getTime() - startTime.getTime();
                var elapsed = difference - pauseDuration;
                var seconds = Math.floor(elapsed / 1000);
                $('.radial-timer-seconds').text(seconds);

                var percentage = Math.min(100, (seconds / 60) * 100);
                $('.radial-timer-bar').css('height', percentage + '%');
            }
        });
    }
});