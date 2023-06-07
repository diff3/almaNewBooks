#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import xmltodict
import yaml

from libraries.databases.newBookManager import connect, addBooksToAlmaDB
from libraries.utils.Logger import Logger

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

backend = config['backend']

"""
TODO:
    - Add database so you don't need run program more then once per day
    - Add ddc filters for all 
"""

def renameListDictionaryKeys(original_list): 
    """
    Given a list of dictionaries with specific keys, this function renames the keys of each dictionary
    to a new set of key names, and returns a new list of the renamed dictionaries.
    
    Args:
    - original_list: A list of dictionaries, each dictionary having the same set of original keys.
    
    Returns:
    - renamed_list: A list of dictionaries, each dictionary having the same set of keys as the original
                    dictionaries, but with new key names as follows:
                    - 'author' for the original key 'Column1'
                    - 'ddc' for the original key 'Column2'
                    - 'isbn' for the original key 'Column3'
                    - 'released' for the original key 'Column4'
                    - 'title' for the original key 'Column5'"""
        
    renamed_list = list()

    for original_dict in original_list:
        renamed_dict = dict()

        renamed_dict['author'] = original_dict.pop('Column1', None)
        renamed_dict['ddc'] = original_dict.pop('Column2', None)
        renamed_dict['isbn'] = original_dict.pop('Column3', None)
        renamed_dict['released'] = original_dict.pop('Column4', None)
        renamed_dict['title'] = original_dict.pop('Column5', None)

        renamed_list.append(renamed_dict)

    return renamed_list


def getNewBookList():
    """
    Retrieves a new book list from the backend and parses it to an ordered dictionary.

    Returns:
        An ordered dictionary representing the parsed response from the backend."""
    
    url = f"{backend['base']}&limit={backend['limit']}&apikey={backend['apikey']}"
    Logger.debug(url)

    response = requests.get(url) 
    return xmltodict.parse(response.text)

def checkValidList(original_list):
    """
    Given an original list, this function attempts to extract a subset of the list, rename its keys, and return it. 
    If the original list does not contain the expected keys, it returns False. 

    :param original_list: A dictionary containing a report and its query results.
    :type original_list: dict

    :return: A dictionary containing the renamed keys of the given original list, or False if the original list does 
    not contain the expected keys.
    :rtype: dict or bool """
        
    try:
        original_list = original_list['report']['QueryResult']['ResultXml']['rowset']['Row']
        renamed_list = renameListDictionaryKeys(original_list) 

    except KeyError:
        print("Did not return any new book in configured timespan")
        return False
    
    return renamed_list

def applySearchFilters(renamed_list, patterns):
    """
    Applies the given search filters to the renamed_list and returns a new list
    with all items that match the given patterns.

    :param renamed_list: A list of items to apply the search filters on.
    :type renamed_list: list
    :param patterns: A list of regex patterns to match against the 'ddc' field in each item.
    :type patterns: list
    :return: A new list with all items that match the given patterns.
    :rtype: list"""
    
    new_list = list()

    for item in renamed_list:
        ddc_value = item.get('ddc', '')

        for pattern in patterns:
            if ddc_value and re.search(pattern, ddc_value):
                if item not in new_list:
                    new_list.append(item)
                    Logger.debug(f"Added item: {item})")

    return new_list


def main():
    """
    Runs the main function of the program which retrieves the new book list, 
    checks for any invalid book names, applies a set of filters to the list, 
    and prints the number of items in the filtered list."""


    Logger.debug('Starting almaNewBooks')

    patterns = [
        r'372.*',
        r'900.*'
    ]

    original_list = getNewBookList()
    renamed_list = checkValidList(original_list)
    filtered_list = applySearchFilters(renamed_list, patterns)

    print(f"{len(filtered_list)} items in new_list.")

    addBooksToAlmaDB()


if __name__ == "__main__":
    main()