
# Laboratory 1 - Can a model learn to recognize less frequently represented cat breeds more accurately?

## 1. What is this project about?

The aim of this project is to train a model to recognize different cat breeds from photographs. To do this, we use training datasets containing photographs of each breed.

A problem arises when one breed has far fewer photographs than the others. This creates a situation in which the model's picture of the “world” is distorted.

That is exactly the situation in our project. We have 70 photographs for each of seven breeds, but only 15 for the eighth breed — Egyptian Mau. This means the model is likely to learn to recognize the seven well-represented breeds much better than Egyptian Mau. As a result, Egyptian Mau cats may be classified as belonging to other breeds.

In this project, we investigate how to improve recognition of Egyptian Mau without having to obtain new photographs.

We compare two ways of addressing the problem:

- **Oversampling** — reusing the same photographs multiple times (the dataset is brought up to 70 Egyptian Mau examples by repeating the original 15 photographs).
- **Data augmentation** — creating slightly modified versions of existing photographs (the dataset is brought up to 70 Egyptian Mau examples using modified versions of the original 15 photographs).

We then check which method produces better results.

## 2. What is the problem?

Artificial intelligence systems learn to recognize objects from examples.

If we want to teach such a system to recognize a particular cat breed, we show it photographs of that breed and tell it what they depict (which specific breed it is).

Over time, the system learns to identify characteristic features that distinguish one breed from another.

The problem arises when some categories have significantly fewer examples than others.

In our case, the model receives:

| Cat breed | Number of training photographs |
|---|---:|
| Abyssinian | 70 |
| Bengal | 70 |
| Birman | 70 |
| Bombay | 70 |
| Egyptian Mau | **15** |
| Ragdoll | 70 |
| Russian Blue | 70 |
| Siamese | 70 |

This situation is called an **imbalanced dataset**.

It may cause the system to recognize breeds with many training photographs accurately while making more mistakes on the breed represented by only a small number of examples.

## 3. How did we try to solve this problem?

We conducted three types of experiments.

### Experiment 1 — no additional photographs

First, we trained the model to recognize cat breeds using the original data (only 15 photographs of Egyptian Mau).

This experiment provides a baseline against which we can assess whether the other methods actually help.

### Experiment 2 — repeating existing photographs

In the second experiment, we used a method called *oversampling*.

Because we had only 15 photographs of Egyptian Mau, compared with 70 for each other breed, we added 55 repetitions of existing photographs to the training process.

This gave the model a total of 70 Egyptian Mau examples, although 55 of them were repeated copies of the 15 original photographs.

We distributed the repetitions as evenly as possible among the photographs.

**Details of the `oversample()` method:** The function takes a list of Egyptian Mau photographs, the number of additional examples required (`budget` — 55 photographs), and a pseudorandom number generator (`rng`). We divide 55 by 15, giving three complete repetitions of each photograph (45 examples, ensuring an even distribution) and a remainder of 10. We then randomly select 10 distinct photographs for one further repetition and shuffle the complete list. As a result, 10 photographs appear four times each and the remaining five appear three times each among the additional examples.

**Important:** This method does not create new photographs. It simply makes the model encounter examples of the underrepresented breed more often during training.

### Experiment 3 — modifying existing photographs

In the third experiment, we applied *data augmentation*.

Instead of repeating identical photographs, we created modified versions of them.

The photographs could be:

- flipped horizontally,
- rotated slightly,
- brightened or darkened,
- adjusted in contrast and color saturation.

**Exact settings for standard augmentation (`augment()`):** A horizontal flip with probability 0.5 (50%); a random rotation between −10° and +10°; random brightness variation of 0.2; contrast variation of 0.2; and color saturation variation of 0.1. Under the standard interpretation of these settings, the brightness and contrast factors range from 0.8 to 1.2, while the saturation factor ranges from 0.9 to 1.1, where a value of 1 means no change. The function returns a modified copy of the image; the original remains unchanged.

This allowed the model to see the same cat under slightly different conditions.

We wanted to find out whether this variety would help it recognize the breed's characteristic features more accurately.

We also compared two augmentation variants: milder and stronger modifications.

**Parameter comparison (standard → stronger augmentation):** Horizontal flip probability: 0.5 → 0.5; maximum rotation: ±10° → ±20°; brightness variation: 0.2 → 0.3; contrast variation: 0.2 → 0.3; saturation variation: 0.1 → 0.2. In the second variant, we changed only the transformation ranges. After the experiment, we restored the standard augmentation settings in the code.

## 4. How did we evaluate performance?

We used the Oxford-IIIT Pet dataset, which contains photographs of different cat breeds.

The photographs were divided into three groups:

| Dataset | Number of photographs | Purpose |
|---|---:|---|
| Training | 505 | The model learns to recognize breeds (7 breeds × 70 photographs + 15 Egyptian Mau photographs) |
| Validation | 160 | We compare the three methods (original dataset with 15 Egyptian Mau photographs, oversampling, and augmentation) and identify which produces the best results |
| Test | 240 | We assess the final performance on photographs not used for training or for selecting settings |

We repeated each experimental variant five times because training results can vary slightly depending on random initial settings.

We used the EfficientNet-B0 image classification model, which had already been pretrained to analyze photographs. We adapted it to recognize eight cat breeds.

**Training parameters:** We used EfficientNet-B0 pretrained on ImageNet (*transfer learning*). Each training run lasted 8 epochs, with a batch size of 64. Each variant was run five times using random seeds 0, 1, 2, 3, and 4. An *epoch* means one pass through the training data, while *batch size* is the number of photographs processed in one batch.

### How do we measure performance?

We were mainly interested in two metrics:

**Recall for Egyptian Mau** — measures the proportion of photographs actually showing this breed that the model correctly identified.

**Formula:**

\[
\mathrm{Recall}=\frac{TP}{TP+FN}
\]

Here, **TP** (*true positives*) is the number of Egyptian Mau photographs correctly identified, and **FN** (*false negatives*) is the number of Egyptian Mau photographs incorrectly assigned to other breeds.

For example, if the model correctly identifies 15 out of 20 Egyptian Mau photographs, recall is 75%.

**Macro-F1** — evaluates recognition quality across all eight breeds, giving each breed equal weight.

**Formula:**

\[
\mathrm{Macro\text{-}F1}=\frac{F1_1+F1_2+\cdots+F1_8}{8}
\]

Here, **F1₁, F1₂, …, F1₈** are the F1 scores for the eight cat breeds. Thus, all eight breeds have equal weight.

This allows us to check whether improving recognition of Egyptian Mau comes at the cost of poorer results for the other breeds.

## 5. What results did we obtain?

First, we compared the methods on the validation dataset.

| Method | Mean Egyptian Mau recall |
|---|---:|
| No data balancing | 50% |
| Repeating photographs (oversampling) | 69% |
| Modifying photographs (augmentation) | **72%** |
| Stronger augmentation | **72%** |

Both methods produced a clear improvement.

Stronger augmentation did not improve mean recall compared with standard augmentation. We therefore decided to keep the milder transformations.

### Final results

After selecting the method (augmentation), we evaluated performance on a separate test dataset.

| Method | Mean Egyptian Mau recall | Mean macro-F1 |
|---|---:|---:|
| No data balancing | 51.3% | 0.855 |
| Oversampling | 69.3% | 0.878 |
| Augmentation | **74.0%** | **0.882** |

The best result was achieved with augmentation.

Compared with the initial experiment, the proportion of Egyptian Mau photographs correctly recognized increased by approximately **22.7 percentage points**.

At the same time, macro-F1 improved, indicating that better recognition of Egyptian Mau was accompanied by an improvement in overall classification quality in our experiment.

## 6. What did we learn from the experiment?

The results suggest that it is possible to improve an image recognition system without obtaining new photographs.

Simply reusing existing photographs more frequently produced a noticeable improvement.

We obtained even better results when the model also learned from modified versions of those photographs.

This does not mean that augmentation will always be the best solution. We worked with one specific dataset, one type of model, and five repetitions of each experiment.

Results may differ in another task.

**Main conclusion:** The way training data is prepared can have a significant impact on how well an artificial intelligence system recognizes underrepresented categories.

## 7. Technical information and project code

This project was based on a template provided for the *Synthetic Data* course.

As part of the assignment, we independently implemented two functions in `src/synthdata/balance.py`:

- `oversample()` — selects photographs to be reused.
- `augment()` — creates randomly modified versions of photographs.

The remaining components of the template make it possible to download the data, train the model, and calculate the results.

A detailed description of the experiments, the results of all five repetitions, the commands used, and the charts can be found in **[EXPERIMENTS.md](EXPERIMENTS.md)**.

The code and experiment results are available in the `src/`, `runs/`, and `evidence/` directories.


## Laboratory 2 - Can AI-generated images improve cat breed recognition?

### 1. Why did we conduct another experiment?

In the first laboratory, we investigated whether recognition of the Egyptian Mau breed could be improved by repeatedly using the same photographs (*oversampling*) or by creating modified versions of existing photographs (*data augmentation*).

Both methods improved the classifier's performance. Data augmentation was particularly effective, increasing the proportion of correctly recognized Egyptian Mau cats on the test dataset from 51.3% to 74.0%.

However, both methods have a limitation: they rely entirely on information contained in the original 15 photographs. Rotating a photograph or adjusting its brightness does not allow the model to see a completely different cat.

We therefore decided to test a new approach: **generate synthetic photographs of Egyptian Mau cats and investigate whether they improve the classifier's recognition performance.**

### 2. How can we generate synthetic photographs of Egyptian Mau cats?

We used **Stable Diffusion 1.5** to generate the photographs.

Stable Diffusion is an artificial intelligence model that can create images from text descriptions, an approach known as *text-to-image generation*. For example, we can ask it to generate a realistic photograph of a silver Egyptian Mau cat with green eyes and distinctive spots.

Its operation is based on a technique called **diffusion**.

During the training of diffusion models, Gaussian noise is gradually added to images. Initially, the original photograph remains recognizable, but after many steps of adding noise, the image becomes completely unrecognizable and consists almost entirely of random noise.

During training, the model learns to predict the noise added to an image. During generation, these predictions can be used to gradually remove noise. The process starts with random noise, which is transformed step by step into an image corresponding to the text description.

In Stable Diffusion, these operations are performed not directly on image pixels, but on a compressed representation of the image. Only at the end is the resulting representation converted into a visible image.

The text description guides the model toward generating an image with the requested features.

**Important:** We did not train Stable Diffusion during this experiment. Instead, we used an already pretrained model to generate new images based on a description of the Egyptian Mau breed.

### 3. How did we prepare the synthetic images?

We generated four pools of Egyptian Mau photographs. Each pool contained **110 images** with a resolution of 512 × 512 pixels.

We used the same text prompt in every case:

> A realistic photograph of an Egyptian Mau cat, silver spotted coat, green eyes, short hair, natural lighting

We also used a *negative prompt*, which specifies elements that the model should avoid generating. These included illustrations, text, watermarks, extra limbs, and multiple cats in one photograph.

Our goal was to obtain images that resembled real photographs of cats as closely as possible.

However, we did not assume that every generated image would be correct. A generative model may produce a cat with an unnatural appearance, incorrect anatomy, or coat patterns characteristic of another breed.

For this reason, in addition to evaluating the classifier's performance, we visually inspected samples of the generated images.

### 4. Why did we generate four different image pools?

We wanted to investigate whether the generator's settings affect the quality of synthetic images and, consequently, the classifier's performance.

We compared two Stable Diffusion parameters:

**Guidance** — determines how strongly the model follows the text description when generating an image.

With a low guidance value, the model has greater freedom when generating images. With a high value, it follows the text more strongly, but may exaggerate certain features, such as coat patterns or eye color.

**Steps** — the number of steps used to gradually transform noise into an image.

More steps mean additional stages of image generation and generally higher computational cost. However, increasing the number of steps does not guarantee that an image will be better or more useful for training the classifier.

We used the following settings:

| Pool | Guidance | Steps | Purpose |
|---|---:|---:|---|
| `m2-base` | 7.5 | 30 | Baseline settings |
| `m2-guidance2` | 2.0 | 30 | Effect of low guidance |
| `m2-guidance15` | 15.0 | 30 | Effect of high guidance |
| `m2-steps10` | 7.5 | 10 | Effect of reducing generation steps |

In each alternative configuration, **only one parameter was changed relative to the baseline settings**.

This allowed us to compare the effects of individual parameters rather than changing several settings simultaneously.

### 5. How did we use the generated images?

In the first laboratory, our training dataset contained 505 photographs:

- 490 photographs of seven well-represented breeds,
- 15 photographs of Egyptian Mau cats.

In the second laboratory, we added **55 generated Egyptian Mau images** to the same dataset. These were randomly selected from the corresponding pool of 110 images.

As a result, each training dataset contained 560 examples, including 70 Egyptian Mau examples: 15 real photographs and 55 synthetic images.

Why did we generate 110 images if we only needed 55?

We wanted to have a larger pool from which we could randomly select images for individual training runs. This meant that we did not have to use exactly the same synthetic photographs every time.

Each of the four configurations was evaluated in five training runs using different random seeds.

In total, we performed **20 classifier training runs**.

We continued to use EfficientNet-B0 so that the new results could be compared with those obtained in the first laboratory.

### 6. How did we evaluate the effectiveness of synthetic images?

We used the same two evaluation metrics as in the previous laboratory:

**Egyptian Mau recall** — measures the proportion of real Egyptian Mau photographs that the classifier correctly recognizes.

**Macro-F1** — measures classification performance across all eight breeds, giving each breed equal importance.

This is important because we want to improve Egyptian Mau recognition without significantly reducing performance on the other breeds.

We evaluated the classifier using **only real photographs**, not images generated by Stable Diffusion.

First, we compared all four configurations on the validation dataset. After selecting the best-performing configuration, we evaluated it on a separate test dataset.

This procedure helps reduce the risk of choosing settings that perform particularly well on the test photographs by chance.

### 7. What results did we obtain?

The table below presents the average validation results across five training runs.

| Pool | Egyptian Mau recall | Macro-F1 |
|---|---:|---:|
| `m2-base` | **80.0%** | **0.910** |
| `m2-guidance2` | 79.0% | 0.892 |
| `m2-guidance15` | 73.0% | 0.895 |
| `m2-steps10` | 79.0% | 0.903 |

The best results were obtained using