export const base64ToImage = (base64img, callback) => {
    var img = new Image();
    img.onload = function() {
        callback(img);
    };
    img.src = "data:image/jpeg;base64," + base64img;

}

