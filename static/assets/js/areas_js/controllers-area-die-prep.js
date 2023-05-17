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
                    var moStatus = '';
                    var effciencyStatus = '';
                    var ooeStatus = '';
                    var operatorStatus = '';
                    var qtyToProccessStatus = '';
                    var startTimeStatus = '';
                    var totalRunningTime = '';
                    var idleTime = '';
                    var currentDate = new Date();
                    var currentYear = currentDate.getFullYear(); // Get the current year (e.g., 2023)
                    var currentMonth = currentDate.getMonth(); // Get the current month (0-11, where 0 represents January)
                    var currentDay = currentDate.getDate(); // Get the current day of the month (1-31)
                    var currentHours = currentDate.getHours(); // Get the current hour (0-23)
                    var currentMinutes = currentDate.getMinutes(); // Get the current minute (0-59)
                    var currentSeconds = currentDate.getSeconds(); // Get the current second (0-59)

                    var formattedDateTime = currentYear + '-' + (currentMonth + 1) + '-' + currentDay + ' ' + currentHours + ':' + currentMinutes + ':' + currentSeconds;


                    if (machine_status == "CONNECTED") {
                        stat = 'active-no-running';
                        text_color = 'success'
                        moStatus = '--';
                        effciencyStatus = '--';
                        ooeStatus = '--';
                        operatorStatus = '--';
                        qtyToProccessStatus = '--';
                        startTimeStatus = '--';
                        totalRunningTime = '--';
                        idleTime = '--';
                    }else if (machine_status == "DISCONNECTED") {
                        stat = 'disconnected';
                        text_color = 'success'
                        moStatus = '--';
                        effciencyStatus = '--';
                        ooeStatus = '--';
                        operatorStatus = '--';
                        qtyToProccessStatus = '--';
                        startTimeStatus = '--';
                        totalRunningTime = '--';
                        idleTime = '--';
                    } else if (machine_status == 'DOWN') {
                        stat = 'down';
                        text_color = 'danger'
                        moStatus = '--';
                        effciencyStatus = '--';
                        ooeStatus = '--';
                        operatorStatus = '--';
                        qtyToProccessStatus = '--';
                        startTimeStatus = '--';
                        totalRunningTime = '--';
                        idleTime = '--';
                    } else if (machine_status == 'ACTIVE_RUNNING') {
                        stat = 'active-running';
                        text_color = 'danger'
                        moStatus = 'MO-0003';
                        effciencyStatus = '40%';
                        ooeStatus = '50%';
                        operatorStatus = '10450';
                        qtyToProccessStatus = '600pcs';
                        startTimeStatus = formattedDateTime;
                        totalRunningTime = currentHours + ' Hours';
                        idleTime = '--';
                    } else if (machine_status == 'ACTIVE_MO_RUNNING') {
                        stat = 'idle-active-mo';
                        text_color = 'danger'
                        moStatus = 'MO-0006';
                        effciencyStatus = '80%';
                        ooeStatus = '30%';
                        operatorStatus = '10421';
                        qtyToProccessStatus = '100pcs';
                        startTimeStatus = formattedDateTime;
                        totalRunningTime = (currentHours - 1) + ' Hours';
                        idleTime = '--';
                    } else if (machine_status == 'IDLE') {
                        stat = 'idle'
                        text_color = 'primary'
                        moStatus = '--';
                        effciencyStatus = '--';
                        ooeStatus = '--';
                        operatorStatus = '--';
                        qtyToProccessStatus = '--';
                        startTimeStatus = '--';
                        totalRunningTime = '--';
                        idleTime = (currentMinutes + 1) + ' Minutes';
                    } else {
                        stat = ''
                    }
                    body += '<div class="carbon-example ' + stat + '">'
                        + '<span>Status: ' + item.status + '</span><br>'
                        + '<span>Machine Name: ' + item.machine + '</span><br><br>'
                        + '<hr>'
                        + '<div class="oee-div">'
                        + '<span>Efficiency: '+ effciencyStatus +'</span>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="inner-wrapper ">'
                        + '<div class="details">'
                        + '<div>'
                        + '<dl>'
                        + '<dt style="font-weight:bold">MO#</dt>'
                        + '<dd>'+ moStatus +'</dd>'
                        + '<dt style="font-weight:bold">OPR ID No.</dt>'
                        + '<dd>'+ operatorStatus +'</dd>'
                        + '<dt style="font-weight:bold">Qty to Process</dt>'
                        + '<dd>'+ qtyToProccessStatus +'</dd>'
                        + '</dl>'
                        + '</div>'
                        + '<div class="vl"></div>'
                        + '<div>'
                        + '<dl>'
                        + '<dt style="font-weight:bold">Start time:</dt>'
                        + '<dd>'+ startTimeStatus +'</dd>'
                        + '<dt style="font-weight:bold">Total Running Time</dt>'
                        + '<dd>'+ totalRunningTime +'</dd>'
                        + '<dt style="font-weight:bold">Idle time</dt>'
                        + '<dd>'+ idleTime +'</dd>'
                        + '</dl>'
                        + '</div>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="oee-div">'
                        + '<span>OEE: '+ ooeStatus +'</span>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="oee-details">'
                        + '<span>Machine Start time:</span>'
                        + '<br>'
                        + '<span>Total Proccesed Quantity:</span>'
                        + '<br>'
                        + '<span>Total Uptime:</span>'
                        + '<br>'
                        + '<span>Total Idletime:</span>'
                        + '<br>'
                        + '<span>Total Dowtime:</span>'
                        + '</div>'
                        + '<p class="fine-print">ID: ' + item.id + '</p>'
                        + '</div>';

                    // Add the card to the container element
                    var row = Math.floor(index / 2); // Calculate the row index
                    var column = index % 2; // Calculate the column index (values: 0, 1, 2, 3)

                    // Create a new row if necessary
                    if ($('.row .card-group').eq(row).length === 0) {
                        $('.row').append('<div class="card-group"></div>');
                    }

                    // Append the card to the corresponding row and column
                    $('.row .card-group').eq(row).append('<div class="column-' + column + '">' + body + '</div>');
                });
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log('Error fetching data from PostgreSQL');
            }
        });
    }

    fetchAndCreateCards();
    setTimeout(function () {
        window.location.reload();
    }, 100000);
});
