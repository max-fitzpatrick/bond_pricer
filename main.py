from fixed_bond import fixed_bond
import datetime

def main():
	issue_date = datetime.date(2018,1,1)
	settlement_date = datetime.date(2018,1,1)
	maturity_date = datetime.date(2023,1,1)
	coupon_rate = 5
	reoffer_yield = 5.125
	coupon_frequency = "annual"

	test_bond = fixed_bond(issue_date,settlement_date,maturity_date,coupon_rate,reoffer_yield,coupon_frequency)

	print(test_bond.cash_flow_table)
	print(f"Reoffer cash price is: {round(test_bond.reoffer_price,3)}%")

if __name__== "__main__":
  main()