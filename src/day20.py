#!/usr/bin/env python3
import itertools

from aocd import data, submit

# --- Day 20: Trench map ---

flatten = itertools.chain.from_iterable

Pixel: int = 1 | 0
EnhancementAlgorithm = list[Pixel]
Image = list[list[Pixel]]


def main():
    ex1 = enhance(example, 2)
    assert ex1 == 35, f"expected 35, but got {ex1}"
    answer1 = enhance(data, 2)
    assert answer1 == 5573, f"expected 5573, but got {answer1}"
    ex2 = enhance(example, 50)
    assert ex2 == 3351, f"expected 3351, but got {ex2}"
    answer2 = enhance(data, 50)
    assert answer2 == 20097, f"expected 20097, but got {answer2}"
    print(answer1)
    print(answer2)


def enhance(inputs: str, repeats: int) -> int:
    parts = inputs.split('\n\n')
    image_enhancement_algorithm: EnhancementAlgorithm = [1 if x == "#" else 0 for x in parts[0]]
    assert len(image_enhancement_algorithm) == 512, f"The image enhancement algorithm should be 512 Pixels long"
    image = create_image(parts[1], repeats+1)
    default_pixel = 0
    display(image)
    for i in range(repeats):
        print(i)
        image = enhance_image(image, image_enhancement_algorithm, default_pixel)
        if default_pixel == 0 and image_enhancement_algorithm[0] == 1:
            default_pixel = 1
        elif default_pixel == 1 and image_enhancement_algorithm[-1] == 0:
            default_pixel = 0
        display(image)
    return sum(flatten(image))


def create_image(inputs: str, padding: int) -> Image:
    image: Image = [[0] * padding + [1 if x == "#" else 0 for x in line] + padding * [0] for line in inputs.split()]
    for i in range(padding):
        image.insert(0, len(image[0]) * [0])
    for j in range(padding):
        image.append(len(image[0]) * [0])
    return image


def enhance_image(image: Image, image_enhancement_algorithm: EnhancementAlgorithm, default_pixel: Pixel) -> Image:
    enhanced_image = [[0 for r in range(len(image))] for c in range(len(image[0]))]
    for i, row in enumerate(enhanced_image):
        for j, _ in enumerate(row):
            surrounding = get_surrounding_pixels(i, j, image, default_pixel)
            idx = int("".join([str(c) for c in surrounding]), 2)
            if image_enhancement_algorithm[idx] == 1:
                enhanced_image[i][j] = 1
    return enhanced_image


def get_surrounding_pixels(i: int, j: int, image: Image, d: Pixel) -> list[Pixel]:
    return [get_pixel(i - 1, j - 1, image, d), get_pixel(i - 1, j, image, d), get_pixel(i - 1, j + 1, image, d),
            get_pixel(i, j - 1, image, d), get_pixel(i, j, image, d), get_pixel(i, j + 1, image, d),
            get_pixel(i + 1, j - 1, image, d), get_pixel(i + 1, j, image, d), get_pixel(i + 1, j + 1, image, d)]


def get_pixel(i: int, j: int, image: Image, default_pixel: Pixel) -> Pixel:
    if 0 <= i < len(image) and 0 <= j < len(image[0]):
        return image[i][j]
    else:
        return default_pixel


def display(image: Image):
    for line in image:
        print("".join(["#" if x == 1 else "." for x in line]))
    print()


example = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip()

if __name__ == "__main__":
    main()
