from solution.merge_files_to_csv import Path
from solution.merge_files_to_csv import merge_report_files_to_csv

result_file_path = Path(__file__).parent / 'result.csv'

def main():
    df = merge_report_files_to_csv()
    df.to_csv(result_file_path, index=False)


if __name__ == '__main__':
    main()
