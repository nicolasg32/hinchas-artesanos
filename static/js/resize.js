let img1 = document.getElementById("img");
let alreadyClicked = false;

function resize() {
    if (!alreadyClicked) {
        img1.style.width = "1280px";
        img1.style.height = "1024px";
        alreadyClicked = true;
    }
    else {
        img1.style.width = "640px";
        img1.style.height = "480px";
        alreadyClicked = false;
    }
}