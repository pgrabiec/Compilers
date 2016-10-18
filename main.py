#############################################################
# Usage: <program_file_name> <*.html files directory path>
#############################################################

import codecs
import os
import re
import sys


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()
    fp.close()

    print("Nazwa pliku: \t" + str(extract_filename(filepath)))
    print("Autor: \t\t\t" + str(extract_author(content)))
    print("Dział: \t\t\t" + str(extract_department(content)))
    print("Słowa kluczowe: " + str(extract_keywords(content)))
    print("Liczba zdań: \t" + str(count_sentences(content)))
    print("Liczba różnych skrotów: \t\t\t\t\t" + str(count_abbreviations(content)))
    print("Liczba różnych liczb całk. z zakresu int: \t" + str(count_integers(content)))
    print("Liczba różnych liczb zmiennoprzecinkowych: \t" + str(count_float_numbers(content)))
    print("Liczba różnych dat: \t\t\t\t\t\t" + str(count_dates(content)))
    print("Liczba różnych adresów email: \t\t\t\t" + str(count_emails(content)))
    print("\n")


################################################
# ------------- REGEX FUNCTIONS -------------- #
################################################


# +------+
# | META |
# +------+


def extract_filename(filepath):
    pattern = r'(\/*)(\w*.html)'
    compiled = re.compile(pattern)
    result = compiled.search(filepath)
    filename = result.group(2)
    return filename


def extract_author(content):
    pattern = r'<\s*META\s*NAME=\s*"\s*AUTOR\s*"\s*CONTENT\s*=\s*"(.*?)"\s*>'
    compiled = re.compile(pattern)
    results = compiled.search(string=content)
    author = results.group(1)
    return author


def extract_department(content):
    pattern = r'\w*<META NAME="DZIAL" CONTENT="\w*\/(.*?)">'
    compiled = re.compile(pattern)
    result = compiled.search(content)
    department = result.group(1)
    return department


def extract_keywords(content):
    pattern = r'\w*<META NAME="KLUCZOWE_\d?" CONTENT="(.*)">'
    compiled = re.compile(pattern)
    results_as_list = compiled.findall(content)
    results_as_strings = ", ".join(repr(e) for e in results_as_list if e != '')
    return results_as_strings


# +----------+
# | NOT-META |
# +----------+


def get_not_meta(content):
    pattern = r'<[P|p][\s\S]*?<(?:meta|META)'
    compiled = re.compile(pattern, re.MULTILINE)
    result = compiled.findall(content)
    # print(''.join(re.compile(r'<[P|p][\s\S]*?<(?:meta|META)', re.MULTILINE).findall(content)))
    result_as_list = ''.join(result)
    # result_as_string = ", ".join(repr(e) for e in result_as_list)
    return result_as_list


def count_sentences(content):
    pattern = r'.*?([a-zA-Z]{4}|\s+|\B\W)((\.|!|\?)+|( )+\n)'
    # (!) Warning: accepts any 4-letter words like 'proc.'='procent'
    # Because it's not specified exactly in homework

    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    count = 0
    for _ in my_iter:
        count += 1
        # print(element.span(), element.group(0))
        # print(element.start())

    return count


def count_abbreviations(content):
    pattern = r'\b([a-zA-Z]{1,3})\.'
    # (!) Warning: don't accept 'proc.' = 'procent' itp.
    # Because it's not specified exactly in homework

    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    dict = {}
    for e in my_iter:
        # print(_a.group(0))
        if e.group(0) not in dict:
            dict[e.group(0)] = 1
        else:
            dict[e.group(0)] += 1
    # for key, value in dict.items():
    #     print(" : " + key, value)

    return len(dict)


def count_integers(content):
    """
    Counts occurrences of integers between -32768 and 32767 (inclusive) in a given string
    :param content string to be processed
    :rtype int
    """
    pattern = r'(?<!\d|[.])(?:(?:-0*(?:(?:[1-3][0-2][0-9]{2}[0-8])|(?:[1-9][0-9]{,3})))|(?:0*(?:(?:[1-3][0-2][0-9]{2}[0-7])|(?:[1-9][0-9]{,3})))|0+)(?![.]|(?:[.]\d)|\d)'
    compiled = re.compile(pattern)
    results = re.findall(pattern=compiled, string=get_not_meta(content))
    if results is None:
        return 0
    results = set(results)
    length = len(results)
    if length < 1:
        return 0
    return length


def count_float_numbers(content):
    pattern = r'(?<!\w)[+-]?(?:(?:\d+[.]\d*)|(?:[.]\d+)|(?:\d+[.]\d+[e][+-]?\d+)|(?:\d+[e][+-]?\d+))(?!\w)'
    compiled = re.compile(pattern)
    results = re.findall(pattern=compiled, string=get_not_meta(content))
    if results is None:
        return 0
    results = set(results)
    length = len(results)
    if length < 1:
        return 0
    return length


def count_dates(content):
    """
    + dd-mm-rrrr
    + dd/mm/rrrr
    + dd.mm.rrrr
    + rrrr-dd-mm
    + rrrr/dd/mm
    + rrrr.dd.mm
    """
    pattern = r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02]))[.]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02]))[/]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:3[0-1]))[-](?:(?:0[13578])|(?:1[02]))[-]\d{4})|'  # 31 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11))[-]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11))[.]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11))[/]\d{4})|'  # 30 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[.](?:(?:02))[.]\d{4})|'  # 29 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[/](?:(?:02))[/]\d{4})|'  # 29 days
    r'(?:(?:(?:[0-1][0-9])|(?:2[1-9]))[-](?:(?:02))[-]\d{4})|'  # 29 days
    r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:3[0-1]))[-](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:3[0-1]))[/](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:3[0-1]))[.](?:(?:0[13578])|(?:1[02])))|'  # 31 days
    r'(?:\d{4}[-](?:(?:[0-2][0-9])|(?:30))[-](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[.](?:(?:[0-2][0-9])|(?:30))[.](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[/](?:(?:[0-2][0-9])|(?:30))[/](?:(?:0[469])|(?:11)))|'  # 30 days
    r'(?:\d{4}[-](?:(?:[0-1][0-9])|(?:2[0-9]))[-](?:(?:02)))|'  # 29 days
    r'(?:\d{4}[/](?:(?:[0-1][0-9])|(?:2[0-9]))[/](?:(?:02)))|'  # 29 days
    r'(?:\d{4}[.](?:(?:[0-1][0-9])|(?:2[0-9]))[.](?:(?:02)))'  # 29 days
    compiled = re.compile(pattern=pattern)
    results = re.findall(pattern=compiled, string=get_not_meta(content))
    # print(results)
    return len(set(results))


def count_emails(content):
    pattern = r'[\w+-]+(\.([a-zA-Z0-9])+)*@[\w-]+(\.([a-zA-Z0-9])+)+'
    compiled = re.compile(pattern, re.MULTILINE)

    my_iter = compiled.finditer(get_not_meta(content))
    # (!) Warning: in proposed examples it's ALWAYS 0
    # Because it's not specified exactly in homework

    dict = {}
    for e in my_iter:
        # print(e.group(0))
        if e.group(0) not in dict:
            dict[e.group(0)] = 1
        else:
            dict[e.group(0)] += 1
    # for key, value in dict.items():
    #     print(" : " + key, value)

    return len(dict)


################################################
# ----------------- MAIN CODE ---------------- #
################################################


try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)

tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)
