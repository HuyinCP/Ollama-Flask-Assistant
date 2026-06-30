---
task_categories:
- text-classification
language:
- vi
---
## Dataset Card for ViSFD

### 1. Dataset Summary

**UIT‑ViSFD** is a Vietnamese smartphone‐feedback corpus for **aspect‐based sentiment analysis**. It contains **11,122** human‐annotated comments collected from a major e‑commerce platform, with **10 aspect** categories and **3 sentiment polarities** per comment (positive/neutral/negative). In this unified version, train/dev/test splits have been merged into one CSV with a `type` column indicating the split.

### 2. Supported Tasks and Metrics

* **Primary Task**: Multi‐aspect sentiment classification
* **Metrics**:

  * **Accuracy** (per‐aspect and overall)
  * **Macro‑averaged F1** (per‐aspect and overall)


### 3. Languages

* Vietnamese

### 4. Dataset Structure

| Column      | Type   | Description                                                                                     |
| ----------- | ------ | ----------------------------------------------------------------------------------------------- |
| `comment`   | string | The raw user feedback text (Vietnamese).                                                        |
| `n_star`    | int    | Number of stars given by the user (1–5).                                                        |
| `data_time` | string | Timestamp when the comment was posted.                                                          |
| `label`     | string | JSON‐encoded mapping from each of the **10 aspects** to one of `{negative, neutral, positive}`. |
| `type`      | string | Split: `train` / `validation` / `test`.                                                         |
| `dataset`   | string | Always `ViSFD` (for provenance).                                                                |

### 5. Data Fields

* **comment** (`str`): The raw consumer feedback.
* **n\_star** (`int`): User rating (1–5).
* **data\_time** (`str`): Posting date/time of the comment.
* **label** (`str`): A JSON object mapping each aspect to its polarity label.
* **type** (`str`): Which split the sample belongs to.
* **dataset** (`str`): Always `ViSFD`.


### 6. Usage

```python
from datasets import load_dataset
import json

ds = load_dataset("visolex/visfd")

# Separate splits
train = ds.filter(lambda ex: ex["type"] == "train")
val   = ds.filter(lambda ex: ex["type"] == "dev")
test  = ds.filter(lambda ex: ex["type"] == "test")

# Inspect one example
example = train[0]
labels = json.loads(example["label"])
print("Comment:", example["comment"])
print("Aspects ▶️", labels)
```


### 7. Source & Links

* **Original GitHub (data & code)**
  [https://github.com/LuongPhan/UIT-ViSFD](https://github.com/LuongPhan/UIT-ViSFD) 
* **Conference Paper**
  Phan et al. (2021), “SA2SL: From Aspect‑Based Sentiment Analysis to Social Listening System for Business Intelligence” 

---

### 8. Contact Information

* **Author**: Luong Luc Phan et al.
* **Institute**: University of Information Technology – VNUHCM, Vietnam
* **Email**: [18521073@gm.uit.edu.vn](mailto:18521073@gm.uit.edu.vn)

> If any organization intends to use this dataset for commercial purposes, please contact us at [18521073@gm.uit.edu.vn](mailto:18521073@gm.uit.edu.vn).

---

### 10. Licensing and Citation

#### License

Refer to the original repository’s LICENSE. If unspecified, assume **CC BY 4.0**.

#### How to Cite

**Conference Paper**

```bibtex
@InProceedings{10.1007/978-3-030-82147-0_53,
  author    = {Luc Phan, Luong and Pham, Phuc and Nguyen, Kim Thi-Thanh and Huynh, Sieu Khai
               and Nguyen, Tham Thi and Nguyen, Luan Thanh and Huynh, Tin Van and Nguyen, Kiet Van},
  title     = {SA2SL: From Aspect-Based Sentiment Analysis to Social Listening System for Business Intelligence},
  booktitle = {Knowledge Science, Engineering and Management},
  year      = {2021},
  publisher = {Springer International Publishing},
  pages     = {647--658},
  isbn      = {978-3-030-82147-0}
}
```