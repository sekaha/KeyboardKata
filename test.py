from optimizer import Optimizer
from keyboard import Keyboard

# .,'-;/=
# ioea ntsr
o = Optimizer(Keyboard(["qwd.kyuflp", "ioeaghntsr", "zxcvbjm,'-"]))

print(o.find_optima(10000))
