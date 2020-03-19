import requests
import datetime
from dateutil.relativedelta import relativedelta


def get_indices(url):
    url = url + '/_cat/indices'
    indices_list = []
    indices = requests.get(url)
    for index in indices.text.splitlines():
        # если поверх установлена Kibana
        # if 'kibana' not in index.split()[2]:
        #    indices_list.append(index)
        indices_list.append(index)
    return indices_list


def indices_data_filter(indices_list, months):
    filtered_indices_list = []
    for index in indices_list:
        index_date = index.split()[2].split('_')[-1].split('.')
        index_date = datetime.datetime(int(index_date[0]), int(index_date[1]), int(index_date[2]))
        if index_date > datetime.datetime.now() - relativedelta(months=months):
            filtered_indices_list.append(index)
    return filtered_indices_list


def indices_size(indices_list):
    size = [0, 0, 0]
    for index in indices_list:
        index_size = index.split()[9]
        if index_size[-2:] == 'gb':
            size[0] = size[0] + float(index_size[:-2])
        elif index_size[-2:] == 'mb':
            size[1] = size[1] + float(index_size[:-2])
        else:
            size[2] = size[2] + float(index_size[:-2])
    size = size[0] + size[1] / 1024 + size[2] / (1024.0 * 1024.0)
    # Возвращает вес в Gb
    return round(size, 1)


def main(url='http://localhost:9200'):
    indices_list = get_indices(url)
    filtered_indices = indices_data_filter(indices_list, months=1)
    size = indices_size(filtered_indices)
    print(size, ' Gb')


if __name__ == '__main__':
    main()
