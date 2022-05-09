import time

from src.classifier import Classifier

if __name__ == '__main__':
    tic = time.perf_counter()

    cl = Classifier(3)
    print("Started training")
    cl.train()
    print("Saving")
    cl.save_model('trainedModel')

    toc = time.perf_counter()

    print(f"Trained model in {toc - tic:0.4f} seconds")
