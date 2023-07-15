export const base64ToImage = (base64img, callback) => {
    var img = new Image();
    img.onload = function() {
        img.base64 = base64img;
        img.width = this.width;
        img.height = this.height;
        callback(img);
    };
    img.src = "data:image/jpeg;base64," + base64img;

}

