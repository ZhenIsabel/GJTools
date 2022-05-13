import csv
import os
import time

import cfg

csv_rows = []


def load_gold_symbols_record():
    csv_rows.clear()

    file_name = 'gold_report/gold_symbols.csv'
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) >= 3:
                csv_rows.append([bool(row[0]), int(row[1]), bool(row[2])])

    while len(csv_rows) < len(cfg.region_list) * 10:
        csv_rows.append([False, 0, False])


def save_gold_symbols_record():
    file_name = 'gold_report/gold_symbols.csv'
    create_time = time.strftime('%Y%m%d%H%M%S', time.localtime(os.path.getmtime(file_name)))
    os.rename(file_name, 'gold_report/gold_symbols_' + create_time + '.csv')
    with open(file_name, 'w+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in csv_rows:
            csv_writer.writerow(row)


def set_gold_symbols(regional, role, has_gold_symbols, open_time, dig_result):
    csv_rows[regional * 10 + role] = [has_gold_symbols, open_time, dig_result]


def get_gold_symbols(regional, role):
    return csv_rows[regional * 10 + role]


def get_last_gold_symbols_time():
    last_time = 0
    for row in csv_rows:
        if row[1] > last_time:
            last_time = row[1]
    return last_time

