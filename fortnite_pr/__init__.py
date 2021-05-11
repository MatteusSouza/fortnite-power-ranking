import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import json

class PowerRanking():

    """
    get_power_ranking()

    You can pass 3 parameter: platform and region as a string and quantity as an int.
    Platforms values: pc, console, mobile, global || global is default
    Regions: NAE, NAW, EU, OCE, BR, ASIA, ME, global || global is default
    Quantity: How much as you need. || 5 is default.

    With no parameter:
    get_power_ranking()
    You will receive with default settings
    platform='global', region='global', quantity=5

    With parameter:
    get_power_ranking('PC', 'BR', 10)
    #=#=#=#=#=#=#=#=#=#=#=#=


    create_json_file()

    This method have the parameters: dataframe, filename, orient.
    By default, the parameters are: filename='power_ranking.json' and orient='records'.
    To create a json file you need to pass the dataframe.

    from scraping_pr import PowerRanking
    pr = PowerRanking()
    top5 = pr.get_power_ranking(quantity=5) #return a dataframe
    pr.create_json_file(top5)

    The orient are the same as 'pandas to_json'
    allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.
    read more: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html
    example:
    
    To convert to a dictionary:

    pr = PowerRanking()
    Top5_global = pr.get_power_ranking(quantity= 5)
    Top5_global.to_dict()
        
    Pandas documentation:
    https://pandas.pydata.org/docs/reference/frame.html#serialization-io-conversion

    """

    def __init__(self):
        pass


    def __requisition(self, platform, region, page_number = 1):
        '''
        Platforms: pc, console, mobile || global is default
        Regions: NAE, NAW, EU, OCE, BR, ASIA, ME || global is default 
        '''

        url = ('https://fortnitetracker.com/events/powerrankings?page=' 
        + str(page_number) + '&platform=' + platform + '&region=' + region
        )

        content_html = None

        try:
            response = requests.get(url)
            status_code = response.status_code
            response.raise_for_status()

            return response

        except HTTPError:
            print(f"Request failed. Status code: {status_code}")
            raise


    def __extract_data_frame(self, html, quantity: int):
        content_html = BeautifulSoup(html, 'html.parser')
        table = content_html.find(name='table')

        df_raw = pd.read_html(str(table))[0].head(quantity)
        df = df_raw.drop(columns=['Unnamed: 5']) #delete the columm

        ''' The "Points" column contains two pieces of information that must
        be separated into two separate columns.'''

        points = df.Points.str.split(expand=True,) #split the columns
        points.columns = ['Points', 'Top' ,'Percentile' ] #rename the titles columns
        points['Top'] = points['Top'].map({'Top':'Top '}, na_action=None) #Rename the "Top" value with space at the end.
        points["Percentile"] = points["Top"] + points["Percentile"] #merge the columns
        points = points.drop(columns=['Top'])

        df = df.drop(columns=['Points'])
        df.insert(2, "Points", points['Points'], allow_duplicates=False)
        df.insert(3, "Percentile", points['Percentile'], allow_duplicates=False)

        return df


    def create_json_file(self, dataframe, filename='power_ranking.json', orient='records'):
        """
        The method "create_json_file()" have the parameters: dataframe, filename, orient.
        By default, the parameters are: filename='power_ranking.json' and orient='records'.
        To create a json file you need to pass the dataframe.

        pr = PowerRanking()
        top5 = pr.get_power_ranking(quantity=5) #return a dataframe
        pr.create_json_file(top5)
        """
        valid_values = ["split", "records", "index", "columns", "values", "table"]
        try:
            self._validation(orient, valid_values, 'orient')
            dataframe.to_json(filename, orient, indent=2, force_ascii=False)
        except Exception as error:
            print(error)
            raise
    



    def _validation(self, validate_item, itens_list, 
        parameter_name = 'parameter' #To print paramter name in the message error.
        ):
        
        is_string: bool = type(validate_item) == str
        valid_string: bool = False
        itens_list = [item.upper() for item in itens_list]


        if is_string == True:
            valid_string = validate_item.upper() in itens_list,
            if valid_string is False: 
                e_message = (f"{parameter_name} '{validate_item}' not understood. Try the valid values: {itens_list}")
                raise ValueError(e_message)
            return {
                'is_string': is_string, 
                'valid_string': valid_string
                }
        else:
            e_message = "The parameter value is not a string"
            raise AttributeError(e_message)
            return {
                'is_string': False,
                'valid_string': valid_string
            }


    def __cont_page(self, quantity: int):
        """ Algorithm to count how many pages will be needed to search for the number of players.
        Each page has 100 players. """
        value = quantity/100
        
        s1 = float(value)
        s2 = str(s1).split('.')
        if int(s2[1]) == 0:
            return int(s2[0])
        else:
            return int(s2[0]) + 1


    def get_power_ranking(
        self, 
        platform: str = 'global', 
        region: str = 'global', 
        quantity: int = 5
        ):
        """
        get_power_ranking()

        You can pass 3 parameter: platform and region as a string and quantity as an int.
        Platforms values: pc, console, mobile, global || global is default
        Regions: NAE, NAW, EU, OCE, BR, ASIA, ME, global || global is default
        Quantity: How much as you need. || 5 is default.

        With no parameter:
        pr.get_power_ranking()
        You will receive with default settings
        platform='global', region='global', quantity=5
    
        With parameter:
        pr.get_power_ranking('PC', 'BR', 10)
        """

    
        platforms = ["PC", "CONSOLE", "MOBILE", "GLOBAL"]
        regions = ["NAE", "NAW", "EU", "OCE", "BR", "ASIA", "ME", "GLOBAL"]

        valid_platform = self._validation(platform, platforms, 'platform')
        valid_region = self._validation(region, regions, 'region')

        nun_players = quantity
        nun_pages = self.__cont_page(nun_players)
        remainder = (nun_players % 100) #remainder of division | Amount remaining on the last page.

        dataframe = pd.DataFrame(columns=[
            'Rank',
            'Player',
            'Points',
            'Percentile',
            'Earnings',
            'Events',
        ])

        if nun_players <= 100:
            # print('players <= 100')

            response = self.__requisition(platform, region)
            raw_html = response.content
            
            try:
                df = self.__extract_data_frame(raw_html, quantity)
                dataframe = df
                return dataframe
            except Exception as error:
                print(
                    'Condicion: Players <= 100\n'
                    'Algo deu errado\n'
                    f'{error}')
            else: return dataframe
            
        else: # if num_players > 100
            if (remainder) == 0 :
                # print('remainder == 0')

                for j in range(nun_pages):
                    page = j + 1
                    response = self.__requisition(platform, region, page_number=page)
                    raw_html = response.content
                    
                    try:
                        df = self.__extract_data_frame(raw_html, quantity)
                        df = pd.concat([dataframe, df], ignore_index=True)
                        dataframe = df
                    except Exception as error:
                        print(
                            'Something went wrong\nCondition: remainder == 0\n'
                            f'{error}'
                        )
                        break

                return dataframe

            else: #if remainder > 0
                # print('remainder > 0')

                for j in range(nun_pages - 1):
                    page = j + 1
                    response = self.__requisition(platform, region, page_number=page)
                    raw_html = response.content

                    try:
                        df = self.__extract_data_frame(raw_html, quantity)
                        # df_original = dataframe
                        df = pd.concat([dataframe, df], ignore_index=True)
                        dataframe = df
                    except Exception as error:
                        print(
                            'Something went wrong\n'
                            'Condition: remainder > 0\n'
                            f'{error}'
                        )
                        break

                response = self.__requisition(platform, region, page_number=nun_pages)
                raw_html = response.content
                try:
                    df = self.__extract_data_frame(raw_html, quantity=remainder)
                    # df_original = dataframe
                    df = pd.concat([dataframe, df], ignore_index=True)
                    dataframe = df
                except Exception as error:
                        print(
                            'Something went wrong\n'
                            'Condition: remainder > 0\n'
                            'remainder on last page.\n'
                            f'{error}'
                        )
                    
                return dataframe


if __name__ == '__main__':
    pr = PowerRanking()
    space = '\n===========================\n'

    print(space,"With no parameter:",space)
    print(pr.get_power_ranking())
    
    print(space, "With parameter:", space)
    print(pr.get_power_ranking('pc', 'BR', 10))

    top200 = pr.get_power_ranking('pc', 'br', 200)
    pr.create_json_file(top200,"fortnite_top200.json" )