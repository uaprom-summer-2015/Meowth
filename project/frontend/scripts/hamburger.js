"use strict";

function toggle_nav(nav) {
    if (nav.style.maxHeight === "0px") {
        nav.style.maxHeight = "400px";
    } else {
        nav.style.maxHeight = "0px";
    }
}

document.addEventListener("DOMContentLoaded", function (event) {
    var nav = document.getElementById('nav-collapsable');
    nav.style.maxHeight = "0px";

    var hamburger = document.getElementById('hamburger');
    hamburger.addEventListener("click", function (e) {
        e.preventDefault();
        if (this.classList.contains("is-active") === true) {
            this.classList.remove("is-active");
        } else {
            this.classList.add("is-active");
        }
        toggle_nav(nav);
    });
});
