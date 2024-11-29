import json
import argparse

# Функция для преобразования данных из JSON в формат конфигурационного файла
def convert_to_cfg(data):
    lines = []
    
    # Обработка однострочных комментариев
    for comment in data.get('single_line_comments', []):
        lines.append(f"# {comment}")
    
    # Обработка многострочных комментариев
    for comment in data.get('multi_line_comments', []):
        lines.append("=begin")
        for line in comment.split('\n'):
            lines.append(f"\t {line}")
        lines.append("=cut")
    
    # Обработка массивов
    for array in data.get('arrays', []):
        values = ", ".join(map(str, array))
        lines.append(f"list({values})")
    
    # Обработка словарей
    for dictionary in data.get('dictionaries', []):
        pairs = ", ".join([f"{key} -> {value}" for key, value in dictionary.items()])
        lines.append(f"{{{pairs}}}")
    
    # Обработка констант
    constants = data.get('constants', {})
    for name, value in constants.items():
        lines.append(f"let {name} = {value};")
        if name in constants:
            lines.append(f"![{name}]")
    return lines


# Основная функция для обработки командной строки
def main():
    parser = argparse.ArgumentParser(description='Инструмент для преобразования JSON в конфигурационный файл')
    parser.add_argument('input_file', help='Входной файл в формате JSON')
    parser.add_argument('output_file', help='Выходной файл в формате конфигурационного файла')
    
    args = parser.parse_args()
    
    # Чтение данных из JSON файла
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Преобразование данных в формат конфигурационного файла
    lines = convert_to_cfg(data)
    
    # Запись данных в выходной файл
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

if __name__ == '__main__':
    main()

#python dz3.py input.json output.cfg