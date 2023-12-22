
<p align="center">
<img src="assets/logo.png" height="80px"width="80px"></img>
</p>


<h1 align="center">QRCode-maker</h1>

<p align="center">
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=MIT&color=Blue&message=MIT&label=License"/></a>
<a href="https://wakatime.com/badge/github/Simatwa/qrcode-maker"><img src="https://wakatime.com/badge/github/Simatwa/qrcode-maker.svg" alt="wakatime"></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=Development&message=Alpha&color=Orange&logo=progress" alt="Progress"/></a>
<a href="#"><img src="https://img.shields.io/static/v1?label=Code Style&message=Black&color=black&logo=Black" alt="Code-style"/></a>
</p>

> Generate [QR-code](https://en.wikipedia.org/wiki/QR_code) for whatever text in [.png](https://en.wikipedia.org/wiki/PNG) format.

## Installation

You need to have [Python>=3.9](python.org) installed.

```
git clone https://github.com/Simatwa/qrcode-maker.git
cd qrcode-maker
pip install -r requirements.txt
```

## Usage
Fire up the server:

- `python -m flask run -p 8000`

The v1 endpoint will be available at `http://localhost:8000/v1`

### Parameters 

- `data` - The text : ()
- `fit` - Ensures data fit more efficiently - `Boolean` *data type* : true
- `version` - QR code version  - *number of modules/dots*. : (1)
- `box_size` - Size of each box : (10)
- `border` - Number of modules/dots around QR Code. : (5)
- `fill_color` - Self explanatory : (black)
- `back_color` - background color : (white)

## Conclusion

Have some fun with the api available [here](https://qrcode.pythonanywhere.com/v1?data=hello)