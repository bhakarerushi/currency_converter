
import requests
import json
import pdb
import xmltodict
import pandas as pd





def get_exchange_rate(source,target):
    """
        this def will get the currency counversion data for 
        given source target currencies
    """
    try:
        api_url = f"https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.{source}.{target}.SP00.A?detail=dataonly"

        response = requests.get(url=api_url)
        # pdb.set_trace()
        if response.status_code == 200:
            dict_data = xmltodict.parse(response.content)
            obs_list = dict_data['message:GenericData']['message:DataSet']['generic:Series']['generic:Obs']      
            row_generator = get_row_generator(obs_list)
            df = pd.DataFrame(row_generator,columns=['TIME_PERIOD','OBS_VALUE'])
            # pdb.set_trace()
            return df
        else:
            if response.status_code == 404:
                return 'Not Found'
    except Exception as ex:
        print(ex)



def get_row_generator(obs_list):
    """ 
        def use to generate row for an data frame
    """
    for obj in obs_list:
        # print(obj['generic:ObsDimension']['@value'], obj['generic:ObsValue']['@value'])
        yield obj['generic:ObsDimension']['@value'], float(obj['generic:ObsValue']['@value'])


# get_exchange_rate('GBP','EUR')

    

def get_raw_data(identifier):
    """
        return df for data from api based on given identifier
    """
    api_url = f"https://sdwwsrest.ecb.europa.eu/service/data/BP6/{identifier}?detail=dataonly"
    # print("url",api_url)
    # response = requests.get(url=api_url)
    # Source API is not working properly, have to get from file to test it out.
    if True:
        with open("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "r") as f:
            # pdb.set_trace()
            dict_data = xmltodict.parse(f.read())
            obs_list = dict_data['message:GenericData']['message:DataSet']['generic:Series']['generic:Obs']
            row_generator = get_row_generator(obs_list)
            df = pd.DataFrame(row_generator,columns=['TIME_PERIOD','OBS_VALUE'])
            # print(df)
            return df
    else:
        return "Not Found"



# get_raw_data('M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N')


def get_source_currency(identifier):
    """
        returns source_currency from given identifier
    """
    identifier_list = identifier.split('.')
    return identifier_list[12]



def resultant_row_generator(conversion_df,raw_data_df):
    raw_data_df.set_index("TIME_PERIOD", inplace = True)
  
    for i,row in conversion_df.iterrows():
        try:
            result = raw_data_df.loc[row['TIME_PERIOD']]
        except KeyError:
            continue
        res = row['OBS_VALUE'] * result['OBS_VALUE']
        yield row['TIME_PERIOD'],res
       


def get_data(identifier,target_currency=None):
    """
        depending upon target data , convert identifier based data frame into conversion based df.
    """
    raw_data_df = get_raw_data(identifier)
    if target_currency:
        source_currency = get_source_currency(identifier)
        conversion_df = get_exchange_rate(source_currency,target_currency)
        if type(conversion_df) == str:
            # print("No Records Found")
            return "No Records Found"  
        row_generator = resultant_row_generator(conversion_df,raw_data_df)
        df = pd.DataFrame(row_generator,columns=['TIME_PERIOD','OBS_VALUE'])
        # print(df)
        return df

    else:
        return raw_data_df



# get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.GBP._T.T.N", "EUR")

if __name__ == '__main__':
    menu_str = """
                Hello,
                1. currency converated df based on given valid identifier.
                2.exit

        """
    print(menu_str)
    while True:
        try:
            choice = int(input("Enter your Choice: "))
        except ValueError:
            print("enter valid choice from above")

        if choice == 1:
            while True:
                identifier = input("Enter valid identifier: ")
                ch = input("want target currency based data.y/n/exit  ")
                # pdb.set_trace
                if ch.lower() == 'y':
                    target_currency = input("Enter valid target_currency: ")
                elif ch.lower() == 'n':
                    target_currency = None
                elif ch.lower() == 'exit':
                    break
                else:
                    print("Enter valid Choice")
                    continue
                df = get_data(identifier,target_currency)
                print(df)
                break
        elif choice == 2:
            break
        else:
            print("enter valid choice")
         



