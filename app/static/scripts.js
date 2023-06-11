const translateButtonList = document.querySelectorAll('.translate-button');
translateButtonList.forEach((translateButton) => {
    translateButton.addEventListener('click', (event)=>{
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