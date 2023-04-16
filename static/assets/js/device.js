$(document).ready(function () {
    function fetchAndCreateCards() {
    $.ajax({
        url: '/card_details',
        method: 'GET',
        success: function (data) {
            // Loop through the data and create a card element for each item
            $.each(data, function (index, item) {
                var machine_status = item.status;
                var body = '';

                if (machine_status == 'IN PRODUCTION' || machine_status == "STARTED") {
                    stat = 'bg-success';
                    text_color = 'success'
                } else if (machine_status == 'STOP DOWNTIME' || machine_status == 'MACHINE DOWNTIME') {
                    stat = 'bg-danger';
                    text_color = 'danger'
                } else if (machine_status == 'IDLE' || machine_status == 'MACHINE DOWNTIME'){
                    stat = 'bg-primary'
                    text_color = 'primary'
                }else{
                    stat = ''
                }
                body += '<div class="col-lg-4"><div class="card card-margin ' + stat + '">'
                    + '<div class="card-header no-border">'
                    + '<h5 class="card-title text-dark" style="text-transform:uppercase;" >' + item.current_path + '</h5>'
                    + '</div>'
                    + '<div class="card-body pt-0">'
                    + '<div class="widget-49">'
                    + '<div class="widget-49-title-wrapper">'
                    + '<div class="widget-49-date-primary">'
                    + '<span class="widget-49-date-day text-'+ text_color +'"">' + item.id + '</span>'
                    + '</div>'
                    + '<div class="widget-49-meeting-info">'
                    + '<span class="widget-49-pro-title text-dark">' + item.date_time + '</span>'
                    + '<span class="widget-49-meeting-time text-dark">' + item.status + '</span>'
                    + '</div>'
                    + '</div>'
                    + '<ul class="widget-49-meeting-points">'
                    + '<li class="widget-49-meeting-item text-dark">'
                    + '<span class="text-dark">Expand module is removed</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item text-dark">'
                    + '<span class="text-dark">Data migration is in scope</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item text-dark">'
                    + '<span class="text-dark">Session timeout increase to 30 minutes</span>'
                    + '</li>'
                    + '<li class="widget-49-meeting-item text-dark">'
                    + '<span class="text-dark">Session timeout increase to 30 minutes</span>'
                    + '</li>'
                    + '</ul>'
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

}
fetchAndCreateCards();

function autoRefresh() {
    location.reload();
}

// Set an interval to call the autoRefresh function every 60,000 milliseconds (1 minute)
setInterval(autoRefresh, 30000);

});

