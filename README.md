# playground

## Front

Add ```"vue-cli-service build --watch"``` into your `package.json`

```
"scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint",
    "watch": "vue-cli-service build --watch"  # Add this line.
  },
```

Run ```npm run watch``` to produce production-ready JS/CSS/HTML in the `./dist` directory.

## Server

Make sure that your environment contains these packages.
- `Flask`
- `Flask-Cors`
- `gunicorn`
- `numpy`
- `opencv-python`
- `Pillow`
- `torch`
- `torchvision`

Run ```python server/app.py``` to activate develop server.

Finally, you can see your web page [your web page: http://127.0.0.1:5000/](http://127.0.0.1:5000/)