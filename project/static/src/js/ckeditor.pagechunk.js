document.addEventListener("DOMContentLoaded", function(event) {
    CKEDITOR.replace('text', {
        autoParagraph: false,
        enterMode : CKEDITOR.ENTER_BR
    });
});