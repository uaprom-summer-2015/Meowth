var CKEDITOR = require("ckeditor");

document.addEventListener("DOMContentLoaded", function(event) {
    CKEDITOR.replace('html', {
        autoParagraph: false,
        enterMode : CKEDITOR.ENTER_BR
    });
});
