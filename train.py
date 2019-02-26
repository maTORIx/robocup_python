import dqn
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Train robocup')
    parser.add_argument('memory_path', type=str, nargs='*')
    parser.add_argument('--epochs', type=int, default=3)
    parser.add_argument('--batch_size', type=int, default=30)
    parser.add_argument('--model_path', type=str, default='robo.pt')
    return parser.parse_args()

def train(estimater, args):
    datasets = join_datasets(args)
    print(datasets.shape)
    estimater.set_episode(datasets)
    for i in range(args.epochs):
        print('epochs: {}'.format(i + 1))
        estimater.train()
    estimater.save()
        
def join_datasets(args):
    result = []
    for path in args.memory_path:
        result.append(np.load(path))
    return np.concatenate(result, axis=0)
        

def main():
    args = parse_args()
    estimater = dqn.Estimater(1, 'l', save_path=args.model_path, batch_size=args.batch_size)
    train(estimater, args)
    


if __name__ == '__main__':
    main()