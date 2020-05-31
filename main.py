from api_wrap import ApiWrapper


def print_movers(companies):
    """
    Print obtained companies symbols with responding values to choose
    :param companies: list of companies symbols
    """
    print("\n------------------- List of companies symbols -------------------\n")
    for i, m in enumerate(companies):
        print(str(i+1) + ' - ' + m)


def get_number_from_user():
    """

    None -> (int)

    Get a symbol by index from the user's input.
    """
    movers = ApiWrapper.get_movers()
    while True:
        print_movers(movers)
        y = input("Enter the number of company: ")
        if y.isdigit() and 0 < int(y) <= len(movers):
            return movers[int(y)-1]
        else:
            print("You entered the wrong value ", y)


if __name__ == "__main__":
    symbol = get_number_from_user()
    ApiWrapper.get_company_info(symbol)
    ApiWrapper.load_prices_json(symbol)
