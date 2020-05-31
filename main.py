from api_wrap import ApiWrapper
from garch import MyGARCH

def print_movers(companies):
    """
    Print obtained companies symbols with responding values to choose
    :param companies: list of companies symbols
    """
    print("\n------------------- List of companies symbols -------------------\n")
    for i, m in enumerate(companies):
        print(str(i+1) + ' - ' + m)


def get_char_from_user(ask_garch=False):
    letters = {'S', 'Q'}
    while True:
        print("\nTo continue, choose an option below:")
        if ask_garch:
            letters.add('G')
            print('G - to get volatility prediction from GARCH modeling')
        print('S - to choose another stock')
        print('Q - to quit')
        y = input("\nEnter a character: ").upper()
        if y in letters:
            return y
        else:
            print("You entered the wrong value ", y)


def get_number_from_user():
    """ None -> (int)

    Get a symbol by index from the user's input.
    """
    movers = ApiWrapper.get_movers()
    while True:
        print("To choose a company, enter a responding integer from the list below")
        print_movers(movers)
        y = input("Enter the number of company: ")
        if y.isdigit() and 0 < int(y) <= len(movers):
            return movers[int(y)-1]
        else:
            print("You entered the wrong value ", y)


if __name__ == "__main__":
    s = ''
    print('\n--------------- Welcome to GARCH world!---------------\n')
    while True:
        if s == 'Q':
            print('\nThank you for using!')
            break
        symbol = get_number_from_user()
        stock = ApiWrapper.get_company_info(symbol)
        s = get_char_from_user(ask_garch=True)
        if s == 'G':
            garch = MyGARCH(stock.rets, stock.get_indices())
            garch.predict_volatility()
            s = get_char_from_user()
        elif s == 'C':
            continue
