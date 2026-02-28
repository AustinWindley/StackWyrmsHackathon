
class Calulator:
    AVG_HOURS_PER_DAY = 8
    AVG_DAYS_PER_WEEK = 5
    AVG_WEEKS_WORKED_PER_YEAR = 48



    # income after taxes

    def Income_After_Taxes(yearly_income, hours_per_week):
        if yearly_income <= 49400:
            return yearly_income * 1-.0335
        elif yearly_income <= 119700:
            return yearly_income * 1-.0660
        elif yearly_income <= 249700:
            return yearly_income * 1-.0760
        else:
            return yearly_income * 1-.0875

    # income per month (given per hour)

    def Monthly_Income(hourly_income):
        return hourly_income * self.AVG_HOURS_PER_DAY * self.AVG_DAYS_PER_WEEK * self.AVG_WEEKS_PER_MONTH
    
    # income per month (given per hour and hours per week)
    def Monthly_Income(hourly_income, hours_per_week):
        return hourly_income * hours_per_week * 4

    # income per year (given per hour)

    def Income_Per_Year(hourly_income):
        return hourly_income * self.AVG_HOURS_PER_DAY * self.AVG_DAYS_PER_WEEK * self.AVG_WEEKS_WORKED_PER_YEAR

    # make pychart out of everything

    def Pie_Chart(rent, groceries, utilities, transportation, entertainment, subscriptions, other):
        data = [
            {"Rent", self.Check_Exist(rent)},
            {"Groceries", self.Check_Exist(groceries)},
            {"Utilities", self.Check_Exist(utilities)},
            {"Transportation", self.Check_Exist(transportation)},
            {"Entertainment", self.Check_Exist(entertainment)},
            {"Subscriptions", self.Check_Exist(subscriptions)},
            {"Other", self.Check_Exist(other)}]
        
        return data
        
    def Check_Exist(a):
        try:
            a
        except NameError:
            return 0
        return a