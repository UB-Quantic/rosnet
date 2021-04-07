from dislib_tensor.tensor import Tensor
import argparse


def main():
    parser = argparse.ArgumentParser(description='Tensor.transpose test')
    parser.add_argument('n', metavar='n', type=int,
                        nargs=1, help='Tensor rank')
    args = parser.parse_args()
    n = args.n[0]

    shape = [4] * n
    block_shape = [2] * (n//2) + [1] * (n//2)
    t = Tensor.zeros(shape, block_shape)
    t.sync()
    print(
        f'Created tensor with rank={t.rank}, shape={t.shape}, block_shape={t.block_shape}, grid={t.grid}')


if __name__ == '__main__':
    main()
