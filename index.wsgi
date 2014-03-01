import sae

from wechat_pomodoro import app

application = sae.create_wsgi_app(app)
