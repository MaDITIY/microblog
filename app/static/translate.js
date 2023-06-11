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

function translate(sourceElemSelector, destElemSelector, sourceLang, destLang) {
    $(destElemSelector).html('<img src="./static/loading.gif">');
    $.post('/translate', {
        text: $(sourceElemSelector).text(),
        source_language: sourceLang,
        dest_language: destLang
    }).done(function(response) {
        $(destElemSelector).text(response['text'])
    }).fail(function() {
        $(destElemSelector).text("Error: Could not contact server");
    });
}