# Collection Downloader
> Download [**Unsplash**](https://unsplash.com) collections with ease

## 💾 Installation
- Clone this repo

## How to use

#### Scripting
- Install `requests`
- Open [`main.py`](main.py) and edit the collections array

```python
  # Collections to download
  collections = ["3644553"]
  
  # Creates a folder with the name of the collection (suggested: true)
  collection_folder = True

  qualities = ["raw", "full", "regular", "small", "thumb"]
  
  # Select picture quality (suggested: "full" (1) or "regular" (2) for non heavy files and good resolution)
  quality = qualities[3]
  
  # You're all set
```

- Run [`main.py`](main.py)


#### CLI
run `cli.py` with argument `download <collection_id>`

```sh

  $ python cli.py download 3644553
  
```

You're all set! Let's download houndred of stunning photos


## About the author
- [Website](https://rawnly.com)
