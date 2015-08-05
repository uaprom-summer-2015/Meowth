from blinker import Namespace

my_signals = Namespace()
model_update = my_signals.signal('model_update')

def update(sender, **kwargs):
    from project.models import MailTemplate
    if isinstance(sender, MailTemplate):
        sender.bl.who_update()

model_update.connect(update)