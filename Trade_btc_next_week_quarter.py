from ultron import Ultron
from hawk import Hawk

##
ultron = Ultron(symbol1="btc_usd", symbol2="btc_usd", contract1="next_week", contract2="quarter",
                history_period=800, history_longer=30, std_bands=0.5)

##
ultron.start()

##
hawk = Hawk(ultron)

##
hawk.start()