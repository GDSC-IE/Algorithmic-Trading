from AlgorithmImports import *

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2020, 1, 1)    #Set Start Date
        self.SetEndDate(2023, 1, 1)      #Set End Date
        self.SetCash(100000)             #Set Strategy Cash
        # Find more symbols here: http://quantconnect.com/data
        self.AddEquity("SPY")

        # create a 15 day exponential moving average
        self.fast = self.EMA("SPY", 15, Resolution.Daily)

        # create a 30 day exponential moving average
        self.slow = self.EMA("SPY", 30, Resolution.Daily)

        self.previous = None

        # Create a plot for stock price, fast EMA, and slow EMA on the same chart
        # self.Plot("Data", "Fast EMA", self.fast)
        # self.Plot("Data", "Slow EMA", self.slow)


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # a couple things to notice in this method:
        #  1. We never need to 'update' our indicators with the data, the engine takes care of this for us
        #  2. We can use indicators directly in math expressions
        #  3. We can easily plot many indicators at the same time

        # wait for our slow ema to fully initialize
        if not self.slow.IsReady:
            return

        # only once per day
        if self.previous is not None and self.previous.date() == self.Time.date():
            return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.00015

        holdings = self.Portfolio["SPY"].Quantity

        # we only want to go long if we're currently short or flat
        if holdings <= 0:
            # if the fast is greater than the slow, we'll go long
            if self.fast.Current.Value > self.slow.Current.Value *(1 + tolerance):
                self.Log("BUY  >> {0}".format(self.Securities["SPY"].Price))
                self.SetHoldings("SPY", 1.0)

        # we only want to liquidate if we're currently long
        # if the fast is less than the slow we'll liquidate our long
        if holdings > 0 and self.fast.Current.Value < self.slow.Current.Value:
            self.Log("SELL >> {0}".format(self.Securities["SPY"].Price))
            self.Liquidate("SPY")

        self.previous = self.Time
