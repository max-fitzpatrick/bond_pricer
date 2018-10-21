import time
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

class fixed_bond:

	def __init__(self,issue_date,settlement_date,maturity_date,coupon_rate,reoffer_yield,coupon_frequency):
		#setting initial attributes for the fixed bond class
		self.issue_date = issue_date
		self.settlement_date = settlement_date
		self.maturity_date = maturity_date
		self.coupon_rate = coupon_rate
		self.reoffer_yield = reoffer_yield
		self.coupon_frequency = coupon_frequency

		# computing future cash flow dates
		if self.coupon_frequency == "annual":
			coupon_frequency_modifier = 1
		elif self.coupon_frequency == "semi-annual":
			coupon_frequency_modifier = 2
		else:
			coupon_frequency_modifier = 4
		
		time_modifier = int(12/coupon_frequency_modifier)
		cash_flow_date = settlement_date + relativedelta(months=time_modifier)
		cash_flow_dates = [cash_flow_date]
		self.number_of_periods = 1

		while cash_flow_date < maturity_date:

			cash_flow_date += relativedelta(months=time_modifier)
			cash_flow_dates.append(cash_flow_date)
			self.number_of_periods += 1

		self.cash_flow_dates = cash_flow_dates

		#computing cash flow periods
		cash_flow_periods = []
		for i in range(self.number_of_periods):
			cash_flow_periods.append(i + 1)
		self.cash_flow_periods = cash_flow_periods

		# computing future cash flows per date (in base 100 and assuming 100% redemption rate)
		coupon_payment = ((coupon_rate/coupon_frequency_modifier)/100) * 100
		cash_flow_amounts = []
		for i in range(self.number_of_periods):
			if i == self.number_of_periods - 1:
				cash_flow = 100 + coupon_payment
			else:
				cash_flow = coupon_payment

			cash_flow_amounts.append(cash_flow)
		self.cash_flow_amounts = cash_flow_amounts


		# computing discount rate
		self.discount_rate = ((self.reoffer_yield/coupon_frequency_modifier)/100) + 1
		discount_rates = []
		for i in range(self.number_of_periods):
			discount_rates.append(self.discount_rate)
		self.discount_rates = discount_rates

		#genrating a cash flow table and calculating reoffer cash price
		df = pd.DataFrame(np.column_stack([self.cash_flow_dates, self.cash_flow_periods, discount_rates,self.cash_flow_amounts]), 
                               columns=['coupon_date', 'discount_period', 'discount_rate', 'cash_flow'])
		df['npv'] = (df.cash_flow / (df.discount_rate**df.discount_period))

		self.cash_flow_table = df
		self.reoffer_price = self.cash_flow_table.npv.sum()