import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def collect_files_contents(source_dir, destination_filename) -> None:
    '''
    Считывает контент всех .PY файлов в папке и сохраняет в один файл .TXT
    '''
    files = os.listdir(source_dir)
    files = [
        source_dir / filename for filename in files if filename.endswith('.py')
    ]
    files.remove(Path(__file__).resolve())

    with open(
        source_dir / 'all_diles_contents.txt', mode='w', encoding='utf-8'
    ) as destination:
        for file_name in files:
            print('открываю файл', file_name)
            with open(
                source_dir / file_name, mode='r', encoding='utf-8'
            ) as source:
                destination.write(
                    f'# Folowing code is {file_name} content:\n\n'
                )
                lines = source.readlines()
                destination.writelines(lines)
                destination.write(f'\n# End of {file_name} content:\n\n')

    print(
        'содержимое всех файлов сохранено в', source_dir / destination_filename
    )


if __name__ == '__main__':
    collect_files_contents(BASE_DIR, 'all_files_contents.txt')
