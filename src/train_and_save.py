from src.classifier import Classifier

import time

if __name__ == '__main__':
    tic = time.perf_counter()

    cl = Classifier(3)
    cl.train()
    cl.save_model('trainedModelStudieBærbar')
    
    toc = time.perf_counter()

    print(f"Trained model in {toc - tic:0.4f} seconds")

