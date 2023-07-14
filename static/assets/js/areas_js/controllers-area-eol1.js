$(document).ready(function () {
    function fetchAndCreateCards() {
        $.ajax({
            url: '/card_details_eol1',
            method: 'GET',
            success: function (data) {
                // Loop through the data and create a card element for each item
                $.each(data, function (index, item) {
                    console.log("🚀 ~ file: controllers-area-eol1.js:9 ~ item:", item)
                    var main_status = item.STATUS;
                    var status = '';
                    var stat = '';
                    var mo = item.MO || '--';
                    var opr_id_no = item.EMP_NO || '--';
                    var qtyToProccessStatus = item.RUNNING_QTY || '--';
                    var effciencyStatus = '';
                    var startTimeStatus = item.MACHINE_START_DATE || '--';
                    var totalRunningTime = '';
                    var idleTime = item.IDLE_TIME || '--';
                    var ooeStatus = '';
                    var totalRunningTime = '--';
                    var fit_start_date = item.START_TIME || '--';

                    var machine_name = item.MACHINE_NAME ? item.MACHINE_NAME : '--'

                    if (main_status === 'CONNECTED') {
                        if (mo === '--') {
                            status = 'ACTIVE NO RUNNING';
                            stat = 'active-no-running';
                        } else {
                            status = 'ACTIVE MO RUNNING';
                            stat = 'active-running';
                        }
                    } else if (main_status === 'DISCONNECTED') {
                        main_status = 'DISCONNECTED';
                        status = 'DISCONNECTED';
                        stat = 'disconnected';
                    } else {
                        main_status = 'IDLE';
                        status = 'IDLE';
                        stat = 'idle';

                    }

                    var body = '<div class="carbon-example ' + stat + '">'
                        + '<span>Status: ' + status + ' </span><br>'
                        + '<span id="machine">Machine Name: ' + machine_name + '</span><br>'
                        + '<hr>'
                        + '<div class="oee-div">'
                        + '<span>EFFECTIVENESS: ' + effciencyStatus + '</span>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="inner-wrapper ">'
                        + '<div class="details">'
                        + '<div>'
                        + '<dl>'
                        + '<dt style="font-weight:bold">MO#</dt>'
                        + '<dd>' + mo + '</dd>'
                        + '<dt style="font-weight:bold">OPR ID No.</dt>'
                        + '<dd>' + opr_id_no + '</dd>'
                        + '<dt style="font-weight:bold">Qty to Process</dt>'
                        + '<dd>' + qtyToProccessStatus + '</dd>'
                        + '</dl>'
                        + '</div>'
                        + '<div class="vl"></div>'
                        + '<div>'
                        + '<dl>'
                        + '<dt style="font-weight:bold">Start time:</dt>'
                        + '<dd>' + startTimeStatus + '</dd>'
                        + '<dt style="font-weight:bold">Total Running Time:</dt>'
                        + '<dd>' + totalRunningTime + '</dd>'
                        + '<dt style="font-weight:bold">Idle time:</dt>'
                        + '<dd>' + (main_status === 'DISCONNECTED' ? "--" : main_status === 'CONNECTED' ? "--" : idleTime) + '</dd>'
                        + '</dl>'
                        + '</div>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="oee-div">'
                        + '<span>OEE: ' + ooeStatus + '</span>'
                        + '</div>'
                        + '<hr>'
                        + '<div class="oee-details">'
                        + '<span style="font-weight:bold">Machine Start time : ' + fit_start_date + '</span>'
                        + '<br>'
                        + '<span style="font-weight:bold">Total Proccesed Quantity:</span>'
                        + '<br>'
                        + '<span style="font-weight:bold">Total Uptime:</span>'
                        + '<br>'
                        + '<span style="font-weight:bold">Total Idletime:</span>'
                        + '<br>'
                        + '<span style="font-weight:bold">Total Dowtime:</span>'
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

                    // Apply the appropriate status class
                    $('.carbon-example:last').addClass(main_status.toLowerCase());
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
