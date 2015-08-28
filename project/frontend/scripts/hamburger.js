$(document).on("DOMContentLoaded", function () {
    "use strict";
    var nav = document.getElementById('nav-collapsable');
    nav.style.maxHeight = "0px";

    function toggle_nav() {
        if (nav.style.maxHeight === "0px") {
            nav.style.maxHeight = "400px";
        } else {
            nav.style.maxHeight = "0px";
        }
    }

    var hamburger = document.getElementById('hamburger');
    hamburger.addEventListener("click", function (e) {
        e.preventDefault();
        if (this.classList.contains("is-active") === true) {
            this.classList.remove("is-active");
        } else {
            this.classList.add("is-active");
        }
        toggle_nav();
    });
});