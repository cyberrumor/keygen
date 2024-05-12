# keygen

Keygen composes original music in the form of midi files.


# Usage

```bash
usage: keygen [-h] --tonic {c,cs,db,d,ds,eb,e,f,fs,gb,g,gs,ab,a,as,bb,b} --mode
              {ionian,dorian,phrygian,lydian,mixolydian,aeolian,locrian,major,minor}
              DEST

Generate midi

positional arguments:
  DEST                  the name of the output file

options:
  -h, --help            show this help message and exit
  --tonic {c,cs,db,d,ds,eb,e,f,fs,gb,g,gs,ab,a,as,bb,b}
                        the root note of the scale.
  --mode {ionian,dorian,phrygian,lydian,mixolydian,aeolian,locrian,major,minor}
                        the mode of the scale.
```


# Installation

```bash
# Use git to clone this repo then cd into the clone dir.
git clone https://github.com/cyberrumor/keygen
cd keygen

# Install pip if you don't already have it. This is python's package manager.
python -m ensurepip --user --break-system-packages --upgrade
python -m pip install --user --break-system-packages --upgrade pip

# Install build and run requirements.
pip3 install --user -r --break-system-packages requirements.txt

# Install keygen
pip3 install --user --break-system-packages .

# Add your python's user-local bin directory to your PATH, then restart your terminal.
# The method by which you achieve this depends on your operating system.
```

[Listen on YouTube](https://www.youtube.com/watch?v=z--FqXawZ2E)
