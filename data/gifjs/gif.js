  var Gif = function (option) {
    this.url = option.url || '';
    this.width = option.width;
    this.height = option.height;
    this.img = '';
    this.el = option.el || document.body;
    this.canvas = '';
    this.flag = false;

    this.createModel();
  }

  Gif.prototype.createModel = function createModel() {
    var _this = this;
    var img = new Image();
    img.src = this.url;

    img.onload = function () {
      img.width = _this.width ? _this.width : img.width;
      img.height = _this.height ? _this.height : img.height;
      img.style.display = 'none';
      _this.img = _this.el.appendChild(img);

      var canvas = document.createElement('canvas');
      canvas.width = _this.width || img.width;
      canvas.height = _this.heigth || img.height;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      var stop = new Image();
      stop.src = './stop.png';
      stop.onload = function () {
        ctx.drawImage(stop, canvas.width/2-15, canvas.height/2-15, 30, 30);
      }

      _this.canvas = _this.el.appendChild(canvas);

      _this.el.onclick = function () {
        _this.flag = !_this.flag;
        if (_this.flag) {
          _this.canvas.style.display = 'none';
          _this.img.style.display = 'block';
        } else {
          _this.canvas.style.display = 'block';
          _this.img.style.display = 'none';
        }
      }
    }
  }