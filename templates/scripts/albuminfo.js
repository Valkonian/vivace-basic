let followed = false;

function hover(element) {
        element.setAttribute("src", "images/starHalf.svg");
}

function unhover(element) {
    if (followed == false) {
        element.setAttribute("src", "images/starWhite.svg");
    }
    else {
        element.setAttribute("src", "images/starBlack.svg");
    }
}

function change(element) {
    if (followed == false) {
        element.setAttribute("src", "images/starBlack.svg");
        followed = true;
    } else if (followed == true) {
        element.setAttribute("src", "images/starWhite.svg");
        followed = false;
    }
}