class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.balance = 0.0

  def __str__(self):
    """
    When the budget object is printed it should display:

    - A title line of 30 characters where the name of the category is centered in a line 
    of * characters.
    
    - A list of the items in the ledger. Each line should show the description and amount.
    The first 23 characters of the description should be displayed, then the amount. 
    The amount should be right aligned, contain two decimal places, and display a maximum
    of 7 characters.
    
    - A line displaying the category total.

    """
    header = self.name.center(30, '*') + '\n'
    body = ''
    for item in self.ledger:
      des = item['description']
      amo = item['amount']
      body += des if len(des) <=23 else des[:23]
      body += ' ' * (24 -(len(des) if len(des) <= 23 else 23))
      body += f'{amo:.2f}'
      body += '\n'

    total = 'Total: ' + str(self.balance)

    return header + body + total
    
  def deposit(self, amount, description=''):
    """
    A deposit method that accepts an amount and description. If no description is given,
    it should default to an empty string. The method should append an object to the ledger
    list in the form of {"amount": amount, "description": description}.
    """

    self.ledger.append({'amount': float(amount), 'description': description})
    self.balance += amount
    
  def withdraw(self, amount, description=''):
    """
    A withdraw method that is similar to the deposit method, but the amount passed in
    should be stored in the ledger as a negative number. If there are not enough funds,
    nothing should be added to the ledger. This method should return True if the
    withdrawal took place, and False otherwise.
    """
    if amount > self.balance:
      return False
    self.ledger.append({'amount': -float(amount), 'description': description})
    self.balance -= amount
    return True
    
  def get_balance(self):
    """
    A get_balance method that returns the current balance of the budget category based on
    the deposits and withdrawals that have occurred.
    """
    return self.balance

  def transfer(self, amount, category):
    """ 
    A transfer method that accepts an amount and another budget category as arguments. 
    The method should add a withdrawal with the amount and the description "Transfer to
    [Destination Budget Category]". The method should then add a deposit to the other
    budget category with the amount and the description "Transfer from [Source Budget 
    Category]". If there are not enough funds, nothing should be fadded to either ledgers.
    This method should return True if the transfer took place, and False otherwise.
    """
    if amount > self.balance:
      return False
      
    self.withdraw(amount=amount, description=f'Transfer to {category.name}')
    category.deposit(amount=amount, description=f'Transfer from {self.name}')
    return True
    
  def check_funds(self, amount):
    """
    A check_funds method that accepts an amount as an argument. It returns False if the
    amount is greater than the balance of the budget category and returns True otherwise.
    This method should be used by both the withdraw method and transfer method.
    """
    if amount > self.balance:
      return False
    return True
  
def create_spend_chart(categories):
  """
  The chart should show the percentage spent in each category passed in to the function.
  The percentage spent should be calculated only with withdrawals and not with deposits.
  Down the left side of the chart should be labels 0 - 100. The "bars" in the bar chart
  should be made out of the "o" character. The height of each bar should be rounded down
  to the nearest 10. The horizontal line below the bars should go two spaces past the 
  final bar. Each category name should be written vertically below the bar. There should
  be a title at the top that says "Percentage spent by category".
  """
  # vars
  names = []
  spend = []

  # string
  data = 'Percentage spent by category\n'

  # parse data from categories
  for cat in categories:
    # name
    names.append(cat.name) 
    # spend per cat
    spend_tmp = 0.0
    for item in cat.ledger:
      if item['amount'] < 0:
        spend_tmp += item['amount']
    spend.append(spend_tmp)

  # calc % per cat by total
  # rounding done with int so allways down
  total = sum(spend)
  for idx, i in enumerate(spend):
    spend[idx] = int((i / total * 10)) * 10

  
  # span matrix and fill with data  
  for i in range(100, -10, -10):
    data += f'{i:>3}|'
    for ii in spend:
      data += ' o ' if i <= ii else '   '
    data += ' \n'
    
    
  data += '    '
  data += '---' * len(categories) + '-\n'

  for i in range(len(max(names, key=len))):
    data += '    '
    for ii in names:
      data += f' {ii[i]} ' if len(ii) > i else '   '
    data += ' \n'

  data = data[:-1]
  return data # to remove the last \n