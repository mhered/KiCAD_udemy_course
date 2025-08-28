# README.md

This repository contains [my course notes](./notes/KiCAD_notes.md) from the Udemy course [KiCAD like a Pro](https://www.udemy.com/course/kicad-like-a-pro-3e/) by Dr Peter Dalmaris, as well as several beginner friendly KiCAD projects (some of which are inspired in the course)

### ⚠️ Libraries included

This repository follows (mostly) [these recommendations](./notes/recommended_libraries_setup_in_KiCAD_repo.md) to facilitate that everything needed to replicate these projects travels with the repo 

### ⚠️ Git LFS Required

This repository uses [Git Large File Storage (Git LFS)](https://git-lfs.com/) to handle large files (mainly for CAD models, and zipped gerber files).

If you clone the repo without Git LFS, large files will appear as tiny pointer files instead of the real content.

### Setup
1. Install Git LFS on your system:

   ```bash
   sudo apt install git-lfs
   ```

2. Run once on your machine to set it up for your user account:
   ```bash
   git lfs install
   ```

3. Clone the repository as usual:

   ```bash
   git clone https://github.com/mhered/KiCAD_udemy_course.git
   ```
