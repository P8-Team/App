import time

from src.classifier import Classifier
from src.config_loader import load_config_file

if __name__ == '__main__':
    tic = time.perf_counter()

    cl = Classifier(load_config_file('config.yml'))
    print("Started training")
    cl.train()
    print("Saving")
    cl.save_model('trainedModel')

    toc = time.perf_counter()

    print(f"Trained model in {toc - tic:0.4f} seconds")
