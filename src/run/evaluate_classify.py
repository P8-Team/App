import pandas as pd

from src.device.device import Device
from src.oracle import Oracle

if __name__ == '__main__':
    # 1. Load csv file
    df = pd.read_csv('output_file')

    # 2. Drop all columns except the label and mac address
    # address,identification_transmit_power,identification_label,x,y,distance
    df = df.drop(columns=['x', 'y', 'distance'])

    # 3. Add a column with the correct label using oracle classifier

    device_address_dict = {
        "50:8a:06:3f:27:9b": [-23, "Littlelf Smart Home Camera"],
        "dc:29:19:94:b1:f8": [-23, "Nikkei CAM2"],
        "48:78:5e:bd:a9:44": [-7, "Blink Mini"],
    }
    oracle = Oracle(device_address_dict)

    # df['correct_label'] = df['address'].apply(
    #    lambda row: list(oracle.classify([Device(row['address'], [])]))[0].identification[1])
    df['correct_label'] = df['address'].map(
        lambda address: list(oracle.classify([Device(address, [])]))[0].identification[1])
    # 4. Evaluate the classifier for each label

    for label in df['correct_label'].unique():
        df_label = df[df['correct_label'] == label]
        df_not_label = df[df['correct_label'] != label]

        # true positive
        tp = len(df_label[df_label['identification_label'] == label])
        # false positive
        fp = len(df_label[df_label['identification_label'] != label])
        # true negative
        fn = len(df_not_label[df_not_label['identification_label'] != label])
        # false negative
        tn = len(df_not_label[df_not_label['identification_label'] == label])

        print(f"Label: {label}")
        print(f"True positive: {tp}")
        print(f"False positive: {fp}")
        print(f"True negative: {tn}")
        print(f"False negative: {fn}")
        print(f"Accuracy: {(tp + tn) / (tp + tn + fp + fn)}")
        print(f"Precision: {tp / (tp + fp) if (tp + fp) != 0 else 0}")
        print(f"Recall: {tp / (tp + fn) if (tp + fp) != 0 else 0}")
        print(f"F1 score: {2 * tp / (2 * tp + fp + fn)}")
        print()
