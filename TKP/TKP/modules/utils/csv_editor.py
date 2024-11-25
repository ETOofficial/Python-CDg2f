import csv
def read_csv(path):
    """
    读取csv文件

    Args:
        path: csv文件路径

    Returns:
        列名，数据
    """
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append(row)  # 每一行是一个字典，键是列名
        return reader.fieldnames, rows
def write_csv(path, headers, rows):
    """
    Args:
        path: csv文件路径
        headers: 列名，例如 ['姓名', '年龄', '城市']
        rows: 数据行，例如 [{'姓名': '张三', '年龄': '28', '城市': '北京'}, {'姓名': '李四', '年龄': '22', '城市': '上海'}]
    """
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()  # 写入列名
        writer.writerows(rows)  # 写入数据行

if __name__ == '__main__':
    headers, rows = read_csv('../../../docs/names.csv')
    print(headers)
    print(rows)
    # write_csv('../outputs/relationship.csv', headers, rows)