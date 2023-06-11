const translateButtonList = document.querySelectorAll('.translate-button');
translateButtonList.forEach((translateButton) => {
    translateButton.addEventListener('click', (event) => {
        const button = event.currentTarget
        const postBody = button.parentElement.parentElement.querySelector('.post-body');
        translate(
            `#${postBody.id}`,
            `#${button.parentElement.id}`,
            button.dataset.postLanguage,
            button.dataset.userLanguage,
        );
    })
})

function translate(sourceElem, destElem, sourceLang, destLang) {
    $(destElem).html('<img src="./static/loading.gif">');
    $.post('/translate', {
        text: $(sourceElem).text(),
        source_language: sourceLang,
        dest_language: destLang
    }).done(function(response) {
        $(destElem).text(response['text'])
    }).fail(function() {
        $(destElem).text("{{ _('Error: Could not contact server.') }}");
    });
}

$(function addHoverEvent() {
    $('.user_popup').hover(
        function(event) {
            var elem = $(event.currentTarget);
            timer = setTimeout(function() {
                timer = null;
                xhr = $.ajax(
                    '/user/' + elem.first().text().trim() + '/popup').done(
                        function(data) {
                            xhr = null
                            elem.popover({
                                trigger: 'manual',
                                html: true,
                                animation: false,
                                container: elem,
                                content: data
                            }).popover('show');
                            flask_moment_render_all();
                        }
                );
            }, 1000);
        },
        function(event) {
            var elem = $(event.currentTarget);
            if (timer){
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xhr = null;
            }
            else {
                elem.popover('destroy');
            };
        }
    )
})

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