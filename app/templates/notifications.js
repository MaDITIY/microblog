function set_message_count(n) {
    $('#message_count').text(n);
    $('#message_count').css('visibility', n ? 'visible' : 'hidden');
}

function set_task_progress(task_id, progress) {
    $('#' + task_id + '-progress').text(progress);
}

{% if current_user.is_authenticated %}
    $(function() {
        var since = 0;
        setInterval(function() {
            $.ajax('{{ url_for('main.notifications') }}?since=' + since).done(
                function(notifications) {
                    for (var i = 0; i < notifications.length; i++) {
                        switch (notifications[i].name) {
                            case 'unread_message_count':
                                set_message_count(notifications[i].data);
                                break;
                            case 'task_progress':
                                set_task_progress(
                                    notifications[i].data.task_id,
                                    notifications[i].data.progress);
                                break;
                        }
                        since = notifications[i].timestamp;
                    }
                }
            );
        }, 5000);
    });
{% endif %}