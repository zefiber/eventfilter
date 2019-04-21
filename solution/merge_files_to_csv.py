from pandas import DataFrame
from pathlib import Path
from datetime import datetime
from pytz import timezone
import pandas as pd
import xml.etree.ElementTree as ET

xml_file_path = Path(__file__).parent.parent/'reports.xml'
csv_file_path = Path(__file__).parent.parent/'reports.csv'
json_file_path = Path(__file__).parent.parent/'reports.json'
summary_file_path = Path(__file__).parent/'summary.csv'


def parse_xml_file_to_csv():
    tree = ET.parse(xml_file_path)
    records = tree.getroot()
    record_element = {}
    records_list = []
    for report in records:
        for element in report:
            record_element[element.tag] = element.text
    if record_element['packets-serviced'] != '0':
        records_list.append(dict(record_element))

    return records_list

def merge_report_files_to_csv():
    records_list_from_xml = parse_xml_file_to_csv()
    df_xml = DataFrame.from_records(records_list_from_xml)
    df_csv = pd.read_csv(csv_file_path)
    df_json=pd.read_json(json_file_path)

    # convert epoch time to time string of timezone 'Canada/Atlantic'
    df_json['request-time'] = df_json['request-time'].apply(
        lambda d: datetime.fromtimestamp(int(d/1000)).astimezone(timezone('Canada/Atlantic'))
            .strftime('%Y-%m-%d %H:%M:%S %Z'))

    df = pd.concat((df_csv, df_xml, df_json), sort=False, ignore_index=True)

    # filter out the records with packets-serviced 0 and sort the data by request-time
    df = df[df['packets-serviced'].astype(int) != 0]
    df = df.sort_values('request-time', ascending=True)

    # print out the summary file
    summary = df.groupby('service-guid').size()
    df_summary = DataFrame(summary, columns=['number of records'])
    df_summary.to_csv(summary_file_path, index=True)

    return df

