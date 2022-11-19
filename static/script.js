function appear(id) {
    document.getElementById(id).classList.replace("hidden", "animation");
}

function appearSavedKeys() {
    if ("disappear" === document.getElementById("saved-keys").classList[0]) {
        document.getElementById("key-field").classList.replace("animation", "disappear");
        document.getElementById("saved-keys").classList.replace("disappear", "animation");
    }
    else {
        document.getElementById("saved-keys").classList.replace("animation", "disappear");
        document.getElementById("key-field").classList.replace("disappear", "animation");
    }

}

function hidePopup() {
    // hide the popup
    document.getElementById("popup").hidden = true;
}

function showPopup() {
    document.getElementById("popup").classList.remove("disappear");
}
