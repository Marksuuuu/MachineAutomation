$(document).ready(function () {
    $.ajax({
        url: '/card_details',
        method: 'GET',
        success: function (data) {
            // Loop through the data and create a card element for each item
            $.each(data, function (index, item) {
                var machine_status = item.status;
                var body = '';

                if (machine_status == 'stopped') {
                    stat = 'bg-danger';
                } else if (machine_status == 'running') {
                    stat = 'bg-success'
                } else {
                    stat = ''
                }
                body += '<div class="col-lg-4"><div class="card card-margin ' + stat + '">'
                    + '<div class="card-header no-border">'
                    + '<h5 class="card-title">' + item.name + '</h5>'
                    + '</div>'
                    + '<div class="card-body pt-0">'
                    + '<div class="widget-49">'
                    + '<div class="widget-49-title-wrapper">'
                    + '<div class="widget-49-date-primary">'
                    + '<span class="widget-49-date-day">09</span>'
                    + '<span class="widget-49-date-month">apr</span>'
                    + '</div>'
                    + '<div class="widget-49-meeting-info">'
                    + '<span class="widget-49-pro-title">' + item.path + '</span>'
                    + '<span class="widget-49-meeting-time">12:00 to 13.30 Hrs</span>'
                    + '</div>'
                    + '</div>'
                    + '<ol class="widget-49-meeting-points">'
                    + '<li class="widget-49-meeting-item">'
                    + '<span>Expand module is removed</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item">'
                    + '<span>Data migration is in scope</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item">'
                    + '<span>Session timeout increase to 30 minutes</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item">'
                    + '<span>Session timeout increase to 30 minutes</span>'
                    + '</li>'
                    + '</ol>'
                    + '</div>'
                    + '</div>'
                    + '</div>'
                    + '</div>'

                // Add the card to the container element
                $('.device_row').append(body);
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log('Error fetching data from PostgreSQL');
        }
    });
});
