from render import main_activity, show_image
import argparse

HEIGHT = 512
WEIGHT = 512


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-obj', required=True)
    parser.add_argument('-tga', required=True)
    return parser


if __name__ == "__main__":
    args = create_parser().parse_args()
    show_image(main_activity(WEIGHT, HEIGHT, args.obj, args.tga))
