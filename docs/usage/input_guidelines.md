# Input guidelines

## Package structure requirements

As an author, you are required to upload a package of a following structure:

```
.
├── config.toml
├── bibliography.bib
├── part1.md
├── part2.md
├── images/
│   ├── img1.jpg
│   ├── img2.png
│   ├── img3.gif
│   └── some-img-name.tiff
├── videos/
│   └── video-name.mp4
└── csv/
    └── some-data.csv
```

For books and articles that include multiple images and/or other media files, it is recommended to group all images and other media files in a folder (directory). A common use case would be to use chapter names as a folder names for all of media files referenced in a given chapter.

```
.
├── config.toml
├── bibliography.bib
├── part1.md
├── part2.md
├── images/
│   ├── part1/
│   │   ├── img1.jpg
│   │   ├── img2.png
│   │   ├── img3.gif
│   │   └── some-img-name.tiff
│   └── part2/
│       └── img1.jpg
├── videos/
│   └── part2/
│       └── video-name.mp4
└── csv/
    └── part1/
        └── some-data.csv
```
