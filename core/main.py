from flask import Flask, request, Response, jsonify
from flask.views import MethodView, View
from qrcode import QRCode
from datetime import datetime
from io import BytesIO
from .bot import telebot, bot, BOT_TOKEN

app = Flask(
    __name__,
)


class MakeQrcode(MethodView):
    init_every_request = True

    def __init__(self):
        getArg = lambda key, default: request.args.get(key, default)
        self.data = getArg("data", "")
        fit_param = getArg("fit", True)
        self.fit = False if fit_param in ("0", "false") else True
        self.version = getArg("version", 1)
        self.box_size = getArg("box_size", 10)
        self.border = getArg("border", 5)
        self.fill_color = getArg("fill_color", "black")
        self.back_color = getArg("back_color", "white")
        self.current_time = datetime.utcnow()

    def get(self):
        try:
            assert self.data, "Data parameter cannot be null"
            qr = QRCode(
                version=self.version,
                box_size=self.box_size,
                border=self.border,
            )

            qr.add_data(self.data)
            qr.make(fit=self.fit)
            img = qr.make_image(
                fill_color=self.fill_color,
                back_color=self.back_color,
            )

        except Exception as e:
            return (
                jsonify(
                    {
                        "message": f"Error occurred",
                        "error": f"{e.args[1] if len(e.args) > 1 else e}",
                    }
                ),
                400,
            )

        else:
            img_stream = BytesIO()
            img.save(img_stream)
            resp = Response(img_stream.getvalue())
            resp.headers["Content-Type"] = "image/png"
            resp.headers[
                "Content-Disposition"
            ] = f"inline; filename={self.data if len(self.data) < 20 else self.data[:20]}.png"
            resp.headers["Last-Modified"] = self.current_time.strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            )

            return resp


class BotWebhookView(View):
    methods = ["POST"]
    init_every_request = False

    def dispatch_request(
        self,
    ):
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "", 200


app.add_url_rule(
    rule="/v1",
    view_func=MakeQrcode.as_view("v1"),
)
app.add_url_rule(rule=f"/{BOT_TOKEN}", view_func=BotWebhookView.as_view("bot"))
