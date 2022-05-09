from gym_trading.envs import MarketMaker
from gym_trading.utils import LimitOrder
from agent_new.qn import Agent
'''
for day in range (1,32,1):
    print("THE DAY IS NOW" + str(day))
    if day < 10:
        data = "0" + str(day)
    else:
        data = str(day)
    fitting_file = "January/January/XBTUSD_2020-01-" + data + ".csv"
    if day != 14:
        agent = Agent(number_of_training_steps = 1000, fitting_file = fitting_file, testing_file = "archive/XBTUSD_2020-02-01.csv.xz", action_repeats = 300)
        agent.train = False
        agent.start()
'''
agent = Agent(number_of_training_steps = 1000, fitting_file = "archive/XBTUSD_2020-02-01.csv.xz", testing_file = "archive/XBTUSD_2020-02-02.csv.xz", action_repeats = 300)
agent.train = False
agent.start()
agent.env.plot_trade_history("test1")
agent.env.plot_observation_history("test2")


'''

env = MarketMaker(symbol="LTC-USD", fitting_file="archive/XBTUSD_2020-01-01.csv", testing_file="archive/XBTUSD_2020-01-02.csv")

num_assets = 10
H = 300

avg_rewards = []
bad = []

for level in range(1,15,1):

    avg_reward = 0

    for trial in range(30):

        env.seed(trial+10)

        #1. start with position = 1
        #2. step through 100 steps
        #3. try again with different SAL policy

        env.broker.long_inventory.order = LimitOrder(ccy=env.symbol,
                                side='long',
                                price=env.midpoint,
                                step=env.local_step_number,
                                queue_ahead=0)
        limit_pnl, long_filled, short_filled = env.broker.step_limit_order_pnl(
                        bid_price=0, #shouldn't allow any bids to go through, but forces a sale at the midpoint price
                        ask_price=env.midpoint,
                        buy_volume=0,
                        sell_volume=num_assets,
                        step=env.local_step_number)

        env.step()
        env.broker.long_inventory.cancel_limit_order()
        env.step(level) #action indicates which level of OB to place limit order at
        for t in range(H):
            env.step()
        env.broker.flatten_inventory(env.best_bid, env.best_ask)
        env.step()
        #if len(env.broker.long_inventory.positions) != 0: seems to never happen? which is dumb but i won't complain
        #    bad.append((level, trial, env.broker.long_inventory))
        avg_reward += env.episode_stats.reward

        env.reset()

        #while env.broker.long_inventory.position is not empty:
        #make market order of size inventory
        #compute PnL directly from the prices of executed trades
    
    avg_rewards.append(avg_reward)

print(avg_rewards)
print(bad)

'''
