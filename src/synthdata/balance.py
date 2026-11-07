"""Meeting 1: the two classical ways to add Egyptian Mau training examples.

Both functions are yours to write; `uv run synth-train --method oversample` or
`--method augment` uses them.
"""

import random

from PIL import Image
from torchvision import transforms


def oversample(
    minority_photos: list[str], budget: int, rng: random.Random
) -> list[str]:

    if not minority_photos:
        if budget == 0:
            return []
        raise ValueError("No minority photos available")

    if budget < 0:
        raise ValueError("Budget cannot be negative")

    repeats, remainder = divmod(budget, len(minority_photos))

    result = minority_photos * repeats

    extra = rng.sample(minority_photos, remainder)
    result.extend(extra)

    rng.shuffle(result)

    return result


def augment(image: Image.Image) -> Image.Image:

    transformation = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.1
        )
    ])

    return transformation(image.copy())

# def augment(image: Image.Image) -> Image.Image:
#
#     transformation = transforms.Compose([
#         transforms.RandomHorizontalFlip(p=0.5),
#         transforms.RandomRotation(degrees=20),
#         transforms.ColorJitter(
#             brightness=0.3,
#             contrast=0.3,
#             saturation=0.2
#         )
#     ])
#
#     return transformation(image.copy())