from ultron import Ultron
from hawk import Hawk

##
ultron = Ultron(symbol1="ltc_usd", symbol2="ltc_usd", contract1="this_week", contract2="next_week",
                history_period=2400, history_longer=30, std_bands=1)

##
ultron.start()

##
hawk = Hawk(ultron)

##
hawk.start()